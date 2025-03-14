import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Create FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Horse Trainer AI API!"}

@app.get("/ask")
def ask_horse_trainer(question: str):
    """
    Endpoint to ask a horse training question.
    Example usage: 
http://localhost:8000/ask?question=How%20do%20I%20train%20a%20young%20horse
    """
    system_message = """ 
    You are an experienced horse trainer specializing in reining, 
dressage, and horsemanship. 
    Provide clear and actionable training advice for riders of all levels. 
    Ensure responses are practical, safe, and easy to understand.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
        ]
    )

    return {"answer": response["choices"][0]["message"]["content"]}


