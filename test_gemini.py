import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key (first 10 chars): {api_key[:10]}...")

genai.configure(api_key=api_key)

# List available models
print("\nAvailable models:")
print("=" * 50)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")

# Try simple generation
print("\n" + "=" * 50)
print("Testing generation...")
print("=" * 50)

try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content("Say hello")
    print(f"✓ Success! Response: {response.text}")
except Exception as e:
    print(f"✗ Error with gemini-1.5-flash-latest: {e}")

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content("Say hello")
        print(f"✓ Success! Response: {response.text}")
    except Exception as e2:
        print(f"✗ Error with gemini-1.5-pro-latest: {e2}")