# Gemini PDF Assistant

A powerful AI-powered document analysis application that allows you to chat with your PDF documents using Google's Gemini 1.5 Flash model. Built with FastAPI backend and Streamlit frontend for a modern, professional user experience.

## Features

- Multi-PDF Support: Upload and analyze multiple PDF documents simultaneously
- AI-Powered Q&A: Ask questions about your documents and get intelligent answers
- Source Citations: Every answer includes page references and source information
- Professional UI: Beautiful Streamlit interface with modern design
- Real-time Processing: Live status updates and progress tracking
- Session Management: Maintain conversation context across multiple questions
- Cross-platform: Works on Windows, macOS, and Linux

## Architecture

- **Backend**: FastAPI with Python
- **Frontend**: Streamlit
- **AI Model**: Google Gemini 1.5 Flash
- **Vector Store**: FAISS for similarity search
- **Document Processing**: LangChain for PDF handling
- **Embeddings**: Google AI Embeddings API

## Quick Start

### Prerequisites

- Python 3.8+
- Google AI API Key
- Virtual environment (recommended)

### Installation

1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd chat-multi-pdf-gemini-flash
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

### Running the Application

#### Option 1: Use the Launcher Script (Recommended)
```bash
python run_app.py
```

#### Option 2: Manual Start

1. Start the FastAPI backend
   ```bash
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the Streamlit frontend (in a new terminal)
   ```bash
   cd frontend
   streamlit run streamlit_app.py --server.port 8501
   ```

3. Access the application
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## How to Use

1. Upload Documents: Use the sidebar to upload one or more PDF files
2. Process Documents: Click "Process Documents" to index them with AI
3. Ask Questions: Start asking questions about your documents
4. Get Answers: Receive AI-powered responses with source citations
5. Manage Sessions: Reset or clear chat history as needed

## Configuration

### Backend Configuration
- Port: Default 8000 (configurable in `backend/app.py`)
- Host: 0.0.0.0 for network access
- Model: Gemini 1.5 Flash (configurable)

### Frontend Configuration
- Port: Default 8501 (configurable)
- Theme: Professional design
- Responsive: Works on desktop and mobile

## Project Structure

```
chat-multi-pdf-gemini-flash/
├── backend/
│   └── app.py                 # FastAPI backend application
├── frontend/
│   └── streamlit_app.py       # Streamlit frontend application
├── venv/                      # Virtual environment
├── requirements.txt            # Python dependencies
├── run_app.py                 # Application launcher
├── .env                       # Environment variables
└── README.md                  # This file
```



## License

This project is licensed under the MIT License - see the LICENSE file for details.




