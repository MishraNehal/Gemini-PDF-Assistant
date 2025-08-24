# Gemini PDF Assistant

A FastAPI-based application that enables intelligent conversations with PDF documents using Google's Gemini 1.5 Flash model.

[![GitHub](https://img.shields.io/github/license/MishraNehal/Gemini-PDF-Assistant)](https://github.com/MishraNehal/Gemini-PDF-Assistant/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/MishraNehal/Gemini-PDF-Assistant)](https://github.com/MishraNehal/Gemini-PDF-Assistant/stargazers)

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
git clone https://github.com/MishraNehal/Gemini-PDF-Assistant.git
cd Gemini-PDF-Assistant
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

## Running the Application

### Backend
1. Open a terminal and navigate to the backend folder:
   ```
   cd d:\Projects\chat-multi-pdf-gemini-flash\backend
   ```
2. Run the backend using uvicorn:
   ```
   uvicorn app:app --reload --port 8000
   ```

### Frontend
1. Open the frontend file in your browser:
   ```
   d:\Projects\chat-multi-pdf-gemini-flash\frontend\index.html
   ```
2. Use the UI to upload PDFs and ask questions. The frontend communicates with the backend at http://localhost:8000.

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

