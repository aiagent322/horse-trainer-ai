import os
from fastapi import FastAPI

# Debugging: Print working directory and files to verify correct deployment
print("✅ Current Working Directory:", os.getcwd())
print("📂 Files in directory:", os.listdir(os.getcwd()))

# Load environment variables safely
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env file loaded successfully")
except ModuleNotFoundError:
    print("⚠️ Warning: python-dotenv module not found. Skipping environment loading")

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Horse Trainer AI is live!"}

# ✅ Correctly defined /query route
@app.get("/query")
def get_response(query: str):
    return {"response": f"You asked: {query}. Here’s the best training advice!"}

