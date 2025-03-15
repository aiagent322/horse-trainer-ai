import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Debugging: Print working directory and files to verify correct 
deployment
print("✅ Current Working Directory:", os.getcwd())
print("📂 Files in directory:", os.listdir(os.getcwd()))

# Load environment variables safely
try:
    load_dotenv()
    print("✅ .env file loaded successfully")
except ModuleNotFoundError:
    print("⚠️ Warning: python-dotenv module not found. Skipping 
environment loading")

# Initialize FastAPI app
app = FastAPI()

# Root Endpoint
@app.get("/")
def home():
    return {"message": "Horse Trainer AI is live!"}

# Test API Query Route
@app.get("/query")
def get_response(query: str):
    return {"response": f"You asked: '{query}'. Here’s the best training 
advice!"}

# Ensure the app runs with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

