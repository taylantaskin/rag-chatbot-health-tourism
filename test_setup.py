import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*50)
print("SETUP VERIFICATION")
print("="*50)

# Check API keys
gemini_key = os.getenv("GEMINI_API_KEY")
print("\n✓ Gemini API Key:", "SET ✓" if gemini_key else "NOT SET ✗")

# Check PDF files
try:
    pdf_files = [f for f in os.listdir("data") if f.endswith(".pdf")]
    print(f"\n✓ PDF files found: {len(pdf_files)}")
    for pdf in pdf_files:
        print(f"  - {pdf}")
except FileNotFoundError:
    print("\n✗ 'data' folder not found!")

# Test libraries
print("\n" + "="*50)
print("LIBRARY CHECK")
print("="*50)

try:
    import google.generativeai as genai
    print("✓ Google Generative AI library installed")
except ImportError as e:
    print(f"✗ Google Generative AI library NOT INSTALLED: {e}")

try:
    import chromadb
    print("✓ Chroma library installed")
except ImportError as e:
    print(f"✗ Chroma library NOT INSTALLED: {e}")

try:
    import pypdf
    print("✓ PyPDF library installed")
except ImportError as e:
    print(f"✗ PyPDF library NOT INSTALLED: {e}")

try:
    import langchain
    print("✓ LangChain library installed")
except ImportError as e:
    print(f"✗ LangChain library NOT INSTALLED: {e}")

try:
    import streamlit
    print("✓ Streamlit library installed")
except ImportError as e:
    print(f"✗ Streamlit library NOT INSTALLED: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("✓ Sentence Transformers library installed")
except ImportError as e:
    print(f"✗ Sentence Transformers library NOT INSTALLED: {e}")

print("\n" + "="*50)
print("✓ Setup verification completed!")
print("="*50)