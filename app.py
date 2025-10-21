import streamlit as st
import sys
import os
import time  # NEWLY ADDED

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rag_chatbot import RAGChatbot
# Import relevant functions from vector_store.py
from vector_store import build_vector_database  # NEWLY ADDED

# Page configuration
st.set_page_config(
    page_title="Turkish Health Tourism Chatbot",
    page_icon="🏥",
    layout="wide"
)

# --- (Custom CSS - No changes) ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- NEWLY ADDED: Database path ---
DB_DIRECTORY = "chroma_db"


# --- UPDATED: Chatbot loading function ---
@st.cache_resource
def load_chatbot():
    """
    Loads and caches the chatbot.
    If 'chroma_db' directory doesn't exist, it builds the database.
    """

    # Step 1: Check if the database exists and build if necessary
    if not os.path.exists(DB_DIRECTORY):
        st.info("First run: Building vector database... (This may take 1-2 minutes)")
        print("Streamlit Cloud: 'chroma_db' not found, calling build_vector_database()")

        start_time = time.time()

        # Call the function imported from vector_store.py
        build_vector_database()

        end_time = time.time()
        st.success(f"Database built successfully! ({end_time - start_time:.2f} seconds)")
        print(f"Streamlit Cloud: Database built. ({end_time - start_time:.2f} seconds)")
    else:
        print("Streamlit Cloud: Found and loaded existing 'chroma_db' database.")

    # Step 2: Load the chatbot after ensuring the database is ready
    chatbot = RAGChatbot()
    return chatbot


# Header
st.markdown('<div class="main-header">🏥 Turkish Health Tourism Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask me anything about health tourism in Turkey!</div>', unsafe_allow_html=True)

# --- (Sidebar - No changes) ---
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This AI-powered chatbot provides information about health tourism in Turkey using:
    - 📚 RAG (Retrieval Augmented Generation)
    - 🤖 Google Gemini AI
    - 🔍 Vector Database (Chroma)
    - 📄 Turkish Health Tourism Documents
    """)

    st.header("📋 Sample Questions")
    st.write("""
    - What is health tourism?
    - Why choose Turkey for medical treatment?
    - What types of health tourism services are available?
    - What are the advantages of Turkey for health tourism?
    - Tell me about thermal tourism in Turkey
    """)

    st.header("🔧 Technology Stack")
    st.write("""
    - Python
    - Streamlit
    - Google Gemini API
    - Chroma Vector DB
    - LangChain
    - Sentence Transformers
    """)

# --- (Main chat interface - No changes) ---
try:
    # This function now also checks/builds the database
    chatbot = load_chatbot()
    st.success("✅ Chatbot is ready!")  # Updated message
except Exception as e:
    st.error(f"❌ Critical error loading chatbot: {e}")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 View Sources"):
                st.write(", ".join(message["sources"]))

# Chat input
if prompt := st.chat_input("Ask your question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = chatbot.get_answer(prompt)

                # Display answer
                st.markdown(result['answer'])

                # Display sources
                with st.expander("📚 View Sources"):
                    st.write(", ".join(result['sources']))

                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result['answer'],
                    "sources": result['sources']
                })

            except Exception as e:
                st.error(f"Error generating answer: {e}")

# --- (Footer - No changes) ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>🎓 Built for Akbank GenAI Bootcamp | Powered by RAG & Gemini AI</p>
</div>
""", unsafe_allow_html=True)