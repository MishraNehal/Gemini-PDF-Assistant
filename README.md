# Chat with Multiple PDFs using Gemini 1.5 Flash

A powerful FastAPI application that enables conversational interactions with multiple PDF documents using Google's Gemini 1.5 Flash model. The application implements RAG (Retrieval Augmented Generation) pattern to provide accurate, context-aware responses based on the content of uploaded PDFs.

## Architecture

- **FastAPI Backend**: High-performance async web framework
- **LangChain**: Orchestrates the document processing and LLM interaction
- **FAISS**: Facebook AI Similarity Search for efficient vector storage and retrieval
- **Google Gemini 1.5 Flash**: State-of-the-art language model for generating responses
- **PyPDF**: PDF document processing and text extraction

## Features

- Upload and process multiple PDF documents simultaneously
- Intelligent document chunking and embedding generation
- Vector similarity search for relevant context retrieval
- Session management for multiple parallel conversations
- Source attribution for generated responses
- Configurable CORS support
- Conversation history management
- Health check endpoint for monitoring

## Prerequisites

- Python 3.8+
- Google API key with access to Gemini API
- Sufficient storage for vector embeddings
- PDF documents for querying

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd chat-multi-pdf-gemini-flash
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with required configurations:
```
GOOGLE_API_KEY=your-api-key-here
CORS_ORIGINS=http://localhost:8000
```

5. Run the application:
```bash
uvicorn app:app --reload --port 8000
```

## API Documentation

### Upload PDFs
```http
POST /upload
Content-Type: multipart/form-data

files: [file1.pdf, file2.pdf, ...]
```
Response:
```json
{
    "session_id": "uuid",
    "message": "PDFs indexed successfully."
}
```

### Ask Questions
```http
POST /ask
Content-Type: application/json

{
    "session_id": "uuid",
    "question": "What does the document say about...?"
}
```
Response:
```json
{
    "answer": "Generated response...",
    "sources": [
        {
            "source": "document1.pdf",
            "page": 1,
            "snippet": "Relevant context..."
        }
    ]
}
```

### Reset Session
```http
POST /reset
Content-Type: application/json

{
    "session_id": "uuid"
}
```
Response:
```json
{
    "message": "History cleared."
}
```

### Health Check
```http
GET /health
```
Response:
```json
{
    "status": "ok"
}
```

## Technical Details

### Document Processing
- Chunks documents into 1200-character segments with 200-character overlap
- Uses RecursiveCharacterTextSplitter for intelligent document splitting
- Generates embeddings using Google's text-embedding-004 model
- Stores vectors in FAISS for efficient similarity search

### Question Answering
- Retrieves top 4 most relevant document chunks
- Uses Gemini 1.5 Flash with temperature 0.2 for balanced responses
- Maintains conversation history for context-aware answers
- Provides source attribution for transparency

## Error Handling

The API includes comprehensive error handling for:
- Invalid session IDs
- PDF processing failures
- LLM generation errors
- Missing or invalid API keys
- File upload issues

## Security Considerations

- API keys stored in environment variables
- CORS configuration for controlled access
- Session-based conversation management
- No permanent storage of uploaded documents
- Memory-based vector storage (for demo purposes)

## Limitations

- In-memory storage (not suitable for production)
- Limited by Gemini API quotas
- PDF processing may be memory-intensive
- Session data lost on server restart

## Future Improvements

- Persistent storage for vector embeddings
- Database integration for session management
- Support for more document formats
- Streaming responses
- Rate limiting
- Authentication/Authorization
- Docker containerization

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT

