import os
from fastapi import FastAPI

# ✅ Initialize FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Horse Trainer AI is live!"}

# ✅ Add the missing `/query` endpoint
@app.get("/query")
def get_response(query: str):
    return {"response": f"You asked: {query}. Here's the best training 
advice!"}

# ✅ Debugging: Print Working Directory (One-Line Fix)
print(f"✅ Current Directory: {os.getcwd()}, 📂 Files: 
{os.listdir(os.getcwd())}")

