import openai
import os
import logging
from fastapi import FastAPI, HTTPException

# Configure Logging
logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,   # Logging level (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Log API Key Check
if OPENAI_API_KEY:
    logging.info("✅ OPENAI API Key is set.")
else:
    logging.error("❌ ERROR: OPENAI_API_KEY is missing!")
    raise ValueError("ERROR: OPENAI API Key is not set in environment 
variables.")

# Initialize OpenAI with the key
openai.api_key = OPENAI_API_KEY

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    logging.info("🏠 Home endpoint accessed.")
    return {"message": "Welcome to Horse Trainer AI"}

@app.get("/debug")
def debug_api_key():
    """Returns the status of the OpenAI API key"""
    key_status = "SET" if OPENAI_API_KEY else "MISSING"
    logging.info(f"🔍 Debug API Key Check: {key_status}")
    return {"API_KEY_STATUS": key_status}

@app.get("/ask")
def horse_trainer_agent(question: str):
    """Handles questions related to horse training"""
    logging.info(f"📢 Received question: {question}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are an experienced 
horse trainer specializing in reining.
                Provide step-by-step guidance on reining techniques, 
stopping drills, and improving horse control."""},
                {"role": "user", "content": question}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        logging.info(f"✅ Generated Response: {answer[:50]}...")  # Log 
first 50 characters
        return {"response": answer}

    except Exception as e:
        logging.error(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing 
request.")

