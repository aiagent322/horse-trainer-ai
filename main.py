import os
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = 
os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("🚨 API Key is 
missing! Set OPENAI_API_KEY in .env 
file.")
openai.api_key = OPENAI_API_KEY

print(f"OPENAI_API_KEY is set: {True 
if OPENAI_API_KEY else False}")
