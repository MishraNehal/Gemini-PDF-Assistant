import streamlit as st
import requests
import os
from typing import List
import tempfile
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Gemini PDF Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card styling */
    .stCard {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
    }
    
    /* Chat message styling */
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 12px;
        position: relative;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 3rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background: white;
        color: #333;
        margin-right: 3rem;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .message-avatar {
        position: absolute;
        top: -10px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .user-avatar {
        left: -50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .bot-avatar {
        right: -50px;
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
        color: white;
    }
    
    /* Source info styling */
    .source-info {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 0.8rem;
        margin-top: 0.8rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
        color: #1976d2;
    }
    
    /* Status indicators */
    .status-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-success {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* File upload styling */
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: #f8f9ff;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #4ECDC4;
        background: #f0f8ff;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #5a6fd8;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Constants
BACKEND_URLS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000", 
    "http://0.0.0.0:8000"
]

def get_backend_url():
    """Try to find a working backend URL"""
    for url in BACKEND_URLS:
        try:
            response = requests.get(f"{url}/docs", timeout=3)
            if response.status_code == 200:
                return url
        except:
            continue
    return BACKEND_URLS[0]

API_BASE = get_backend_url()

def main():
    # Professional header
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">📚 Gemini PDF Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Enterprise-grade AI-powered document analysis with Google Gemini 1.5 Flash</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: white; margin-bottom: 1rem;">🚀 Quick Start</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # File upload section
        st.markdown("### 📁 Document Upload")
        uploaded_files = st.file_uploader(
            "Choose PDF files to analyze",
            type=['pdf'],
            accept_multiple_files=True,
            help="Select one or more PDF files for AI analysis"
        )
        
        if uploaded_files:
            st.success(f"📄 {len(uploaded_files)} document(s) selected")
            
            # File details
            for i, file in enumerate(uploaded_files):
                file_size = len(file.getvalue()) / 1024  # KB
                st.info(f"**{file.name}** ({file_size:.1f} KB)")
            
            if st.button("🚀 Process Documents", type="primary", use_container_width=True, key="process_docs"):
                process_pdfs(uploaded_files)
        
        st.markdown("---")
        
        # How to use section
        st.markdown("### 💡 How to Use")
        st.markdown("""
        1. **Upload** your PDF documents
        2. **Process** them with AI indexing
        3. **Ask questions** about the content
        4. **Get instant answers** with sources
        """)
        
        st.markdown("---")
        
        # Settings section
        st.markdown("### ⚙️ Session Management")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset", use_container_width=True, key="sidebar_reset"):
                reset_session()
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True, key="sidebar_clear"):
                clear_chat()
                st.rerun()
        
        # System info
        st.markdown("---")
        st.markdown("### 🔧 System Info")
        st.markdown(f"**Backend**: {API_BASE}")
        st.markdown(f"**Version**: 2.0.0")
        st.markdown(f"**Status**: Active")

    # Main content area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("### 💬 AI Document Chat")
        
        # Initialize session state
        if 'session_id' not in st.session_state:
            st.session_state.session_id = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Chat container
        with st.container():
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            if not st.session_state.chat_history:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #666;">
                    <h3>🎯 Welcome to Gemini PDF Assistant!</h3>
                    <p>Upload your documents and start asking questions to get AI-powered insights.</p>
                    <p>✨ Features:</p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>Multi-PDF analysis</li>
                        <li>Intelligent Q&A</li>
                        <li>Source citations</li>
                        <li>Real-time processing</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display chat history with enhanced styling
                for i, message in enumerate(st.session_state.chat_history):
                    if message['type'] == 'user':
                        st.markdown(f"""
                        <div class="message user-message">
                            <div class="message-avatar user-avatar">👤</div>
                            <strong>You:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="message bot-message">
                            <div class="message-avatar bot-avatar">🤖</div>
                            <strong>Assistant:</strong> {message['content']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if 'sources' in message and message['sources']:
                            sources_text = " | ".join([
                                f"{src.get('source', 'PDF').split('/')[-1]} p.{src.get('page', 'N/A')}"
                                for src in message['sources']
                            ])
                            st.markdown(f'<div class="source-info">📚 Sources: {sources_text}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input section
        if st.session_state.session_id:
            st.markdown("### 💭 Ask a Question")
            question = st.text_input(
                "What would you like to know about your documents?",
                placeholder="e.g., What are the main topics discussed? Summarize the key points...",
                key="question_input"
            )
            
            col_ask, col_clear = st.columns([1, 1])
            with col_ask:
                if st.button("🤔 Ask AI", type="primary", use_container_width=True, key="main_ask"):
                    if question.strip():
                        ask_question(question.strip())
                        st.rerun()
            
            with col_clear:
                if st.button("🗑️ Clear Chat", use_container_width=True, key="main_clear"):
                    clear_chat()
                    st.rerun()
        else:
            st.warning("📤 Please upload and process documents first to start chatting!")
    
    with col2:
        st.markdown("### 📊 Status Dashboard")
        
        # Connection status
        if st.session_state.session_id:
            st.markdown('<div class="status-card status-success">', unsafe_allow_html=True)
            st.markdown("✅ **Documents Processed**")
            st.markdown(f"**Session ID**: {st.session_state.session_id[:8]}...")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-card status-warning">', unsafe_allow_html=True)
            st.markdown("⏳ **No Documents**")
            st.markdown("Upload PDFs to begin")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # API status
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        
        try:
            response = requests.get(f"{API_BASE}/docs", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
                st.markdown(f"**URL**: {API_BASE}")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Unreachable")
            st.info("Check if server is running")
        
        # Metrics
        st.markdown("---")
        st.markdown("### 📈 Metrics")
        
        if st.session_state.chat_history:
            total_messages = len(st.session_state.chat_history)
            user_messages = len([m for m in st.session_state.chat_history if m['type'] == 'user'])
            bot_messages = len([m for m in st.session_state.chat_history if m['type'] == 'bot'])
            
            st.metric("Total Messages", total_messages)
            st.metric("User Questions", user_messages)
            st.metric("AI Responses", bot_messages)
        else:
            st.info("No chat data yet")

def process_pdfs(files: List):
    """Process uploaded PDF files with enhanced UI"""
    try:
        with st.spinner("🔄 Processing documents with AI... This may take a moment."):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Prepare files for upload
            files_data = []
            for i, file in enumerate(files):
                files_data.append(('files', (file.name, file.getvalue(), 'application/pdf')))
                progress_bar.progress((i + 1) / len(files))
                status_text.text(f"Preparing {file.name}...")
            
            status_text.text("Uploading to AI backend...")
            
            # Upload to backend
            response = requests.post(f"{API_BASE}/upload", files=files_data)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.session_id = data['session_id']
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'content': f"✅ Successfully processed {len(files)} document(s)! I'm now ready to answer your questions about them. What would you like to know?",
                    'sources': []
                })
                
                progress_bar.progress(1.0)
                status_text.text("✅ Processing complete!")
                
                st.success(f"🎉 {len(files)} document(s) processed successfully!")
                st.balloons()
            else:
                st.error(f"❌ Error processing documents: {response.text}")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please check your backend connection and try again.")

def ask_question(question: str):
    """Ask a question about the processed PDFs with enhanced UI"""
    if not st.session_state.session_id:
        st.error("No active session. Please process documents first.")
        return
    
    try:
        # Add user message to chat
        st.session_state.chat_history.append({
            'type': 'user',
            'content': question,
            'sources': []
        })
        
        with st.spinner("🤔 Analyzing your question with AI..."):
            # Send question to backend
            response = requests.post(f"{API_BASE}/ask", json={
                'session_id': st.session_state.session_id,
                'question': question
            })
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'content': data.get('answer', 'No answer received'),
                    'sources': data.get('sources', [])
                })
            else:
                st.error(f"❌ Error getting answer: {response.text}")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def reset_session():
    """Reset the current session"""
    if st.session_state.session_id:
        try:
            response = requests.post(f"{API_BASE}/reset", json={
                'session_id': st.session_state.session_id
            })
            if response.status_code == 200:
                st.session_state.session_id = None
                st.session_state.chat_history = []
                st.success("🔄 Session reset successfully!")
            else:
                st.error("❌ Error resetting session")
        except:
            st.error("❌ Error resetting session")
    else:
        st.info("ℹ️ No active session to reset")

def clear_chat():
    """Clear chat history"""
    st.session_state.chat_history = []
    st.success("🗑️ Chat history cleared!")

if __name__ == "__main__":
    main()
