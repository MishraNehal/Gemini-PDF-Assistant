import os
import io
import uuid
import tempfile
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain + loaders + vectorstore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set. Put it in backend/.env")

# FastAPI
app = FastAPI(title="Chat with Multiple PDFs (Gemini 1.5 Flash)")

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory stores (demo only)
SESSIONS: Dict[str, Dict[str, Any]] = {}
# structure:
# {
#   session_id: {
#       "vectorstore": FAISS,
#       "history": List[tuple[str, str]]
#   }
# }

class AskBody(BaseModel):
    session_id: str
    question: str

class ResetBody(BaseModel):
    session_id: str

def _build_vectorstore_from_pdfs(files: List[UploadFile]) -> FAISS:
    # Load PDFs
    documents = []
    for uf in files:
        # Read into memory and feed to PyPDFLoader via temp file-like
        data = uf.file.read()
        bio = io.BytesIO(data)
        
        # Use tempfile module for cross-platform compatibility
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            tmp_file.write(bio.getbuffer())
        
        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            documents.extend(docs)
        finally:
            # Clean up temporary file
            try:
                os.remove(tmp_path)
            except Exception:
                pass

    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    splits = splitter.split_documents(documents)

    # Embeddings (Google)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )

    # Vectorstore
    vectorstore = FAISS.from_documents(splits, embedding=embeddings)
    return vectorstore

def _get_or_create_chain(session_id: str):
    sess = SESSIONS.get(session_id)
    if not sess:
        raise ValueError("Invalid session_id. Upload PDFs first.")
    vectorstore: FAISS = sess["vectorstore"]
    history: List = sess["history"]

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4},
    )

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )
    return chain, history

@app.post("/upload")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    if not files:
        return JSONResponse(status_code=400, content={"error": "No files uploaded"})

    try:
        vectorstore = _build_vectorstore_from_pdfs(files)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to process PDFs: {e}"})

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"vectorstore": vectorstore, "history": []}
    return {"session_id": session_id, "message": "PDFs indexed successfully."}

@app.post("/ask")
async def ask_question(body: AskBody):
    try:
        chain, history = _get_or_create_chain(body.session_id)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    # Prepare chat history as a list of tuples (user, ai)
    chat_history = [(u, a) for u, a in history]

    try:
        result = chain.invoke({"question": body.question, "chat_history": chat_history})
        answer = result["answer"]
        # Update history
        history.append((body.question, answer))

        # Return sources
        sources = []
        for d in result.get("source_documents", []):
            meta = d.metadata or {}
            sources.append({
                "source": meta.get("source"),
                "page": meta.get("page"),
                "snippet": d.page_content[:300]
            })

        return {"answer": answer, "sources": sources}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"LLM error: {e}"})

@app.post("/reset")
async def reset_session(body: ResetBody):
    if body.session_id in SESSIONS:
        SESSIONS[body.session_id]["history"] = []
        return {"message": "History cleared."}
    return JSONResponse(status_code=400, content={"error": "Invalid session_id"})


@app.get("/health")
async def health():
    return {"status": "ok"}
