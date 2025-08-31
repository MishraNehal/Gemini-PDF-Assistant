# 📚 Gemini PDF Assistant

A powerful AI-powered document analysis application that allows you to chat with your PDF documents using Google's Gemini 1.5 Flash model. Built with FastAPI backend and Streamlit frontend for a modern, professional user experience.

## ✨ Features

- **Multi-PDF Support**: Upload and analyze multiple PDF documents simultaneously
- **AI-Powered Q&A**: Ask questions about your documents and get intelligent answers
- **Source Citations**: Every answer includes page references and source information
- **Professional UI**: Beautiful Streamlit interface with gradient designs and animations
- **Real-time Processing**: Live status updates and progress tracking
- **Session Management**: Maintain conversation context across multiple questions
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🏗️ Architecture

- **Backend**: FastAPI with Python
- **Frontend**: Streamlit (converted from HTML/CSS/JS)
- **AI Model**: Google Gemini 1.5 Flash
- **Vector Store**: FAISS for similarity search
- **Document Processing**: LangChain for PDF handling
- **Embeddings**: Google AI Embeddings API

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google AI API Key
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chat-multi-pdf-gemini-flash
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

### Running the Application

#### Option 1: Use the Launcher Script (Recommended)
```bash
python run_app.py
```
This will automatically start both backend and frontend.

#### Option 2: Manual Start

1. **Start the FastAPI backend**
   ```bash
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   cd frontend
   streamlit run streamlit_app.py --server.port 8501
   ```

3. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📖 How to Use

1. **Upload Documents**: Use the sidebar to upload one or more PDF files
2. **Process Documents**: Click "Process Documents" to index them with AI
3. **Ask Questions**: Start asking questions about your documents
4. **Get Answers**: Receive AI-powered responses with source citations
5. **Manage Sessions**: Reset or clear chat history as needed

## 🔧 Configuration

### Backend Configuration
- **Port**: Default 8000 (configurable in `backend/app.py`)
- **Host**: 0.0.0.0 for network access
- **Model**: Gemini 1.5 Flash (configurable)

### Frontend Configuration
- **Port**: Default 8501 (configurable)
- **Theme**: Professional gradient design
- **Responsive**: Works on desktop and mobile

## 📁 Project Structure

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

## 🆕 Recent Updates

### Version 2.0.0 - Streamlit Frontend
- **Complete Frontend Overhaul**: Converted from HTML/CSS/JS to Streamlit
- **Professional UI Design**: Modern gradient backgrounds and animations
- **Enhanced User Experience**: Better chat interface with avatars
- **Improved Status Monitoring**: Real-time metrics and system status
- **Cross-platform Compatibility**: Fixed Windows-specific file path issues
- **Button ID Fixes**: Resolved Streamlit duplicate element issues

### Version 1.0.0 - Initial Release
- Basic FastAPI backend with Gemini integration
- HTML/CSS/JS frontend
- PDF processing and Q&A functionality

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure the backend is running on port 8000
   - Check if the virtual environment is activated
   - Verify your Google API key is set correctly

2. **PDF Processing Errors**
   - Ensure PDFs are not corrupted
   - Check file size limits
   - Verify backend is accessible

3. **Streamlit Button Errors**
   - All buttons now have unique keys
   - Refresh the browser if issues persist

### Performance Tips

- Use smaller PDF files for faster processing
- Close unnecessary browser tabs
- Ensure adequate system memory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.




