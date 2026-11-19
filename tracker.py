from dotenv import load_dotenv
import os
import sys

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_key:
    print("read the Gemini key successfully")
else:
    print("Gemini API key is missing.") 
    sys.exit(1)




groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key:
    print("read the Groq key successfully")
else:
    print("Groq API key is missing.")
    sys.exit(1)




#sys configuration 
if len(sys.argv) < 2:
    print("No Prompt Given , The program exited")
    sys.exit(1)
prompt = sys.argv[1]
print(prompt)