from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables safely
try:
    load_dotenv()
    print("✅ .env file loaded successfully")
except ModuleNotFoundError:
    print("⚠️ Warning: python-dotenv module not found. Skipping 
environment loading")

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Horse Trainer AI is live!"}

# ✅ ADD THIS: API query route for testing
@app.get("/query")
def get_response(query: str):
    return {"response": f"You asked: {query}. Here’s the best training 
advice!"}

