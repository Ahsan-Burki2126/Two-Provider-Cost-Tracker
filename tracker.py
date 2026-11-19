from dotenv import load_dotenv
import os


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key:
    print("read the key succesfully")
else:
    print("Gemini API key is missing.")    
