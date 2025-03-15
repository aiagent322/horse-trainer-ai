import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Horse Trainer AI is live!"}

# New API query route for testing
@app.get("/query")
def get_response(query: str):
    return {"response": f"You asked: {query}. Here’s the best training 
advice!"}

# Debugging: Print confirmation that the app is running
print("✅ FastAPI application has started successfully.")

