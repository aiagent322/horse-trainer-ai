import openai
import os
import logging
from fastapi import FastAPI, HTTPException
from horse_trainer_adapter import HorseTrainerAdapter

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PORT = int(os.getenv("APP_PORT", 10000))
HOST = os.getenv("HOST", "0.0.0.0")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logging.error("❌ ERROR: OPENAI_API_KEY is missing!")
    raise ValueError("ERROR: API Key is not set in environment variables.")

openai.api_key = OPENAI_API_KEY

# Initialize horse adapter
horse_adapter = HorseTrainerAdapter()

app = FastAPI()

@app.get("/")
def home():
    logging.info("🏠 Home endpoint accessed.")
    return {"message": "Welcome to Horse Trainer AI"}

@app.get("/debug")
def debug_api_key():
    key_status = "SET" if OPENAI_API_KEY else "MISSING"
    logging.info(f"🔍 Debug API Key Check: {key_status}")
    return {"API_KEY_STATUS": key_status, "API_KEY": OPENAI_API_KEY[:5] + "**********" if OPENAI_API_KEY else "MISSING"}

@app.get("/ask")
def horse_trainer_agent(question: str):
    logging.info(f"📢 Received question: {question}")
    try:
        # Check if this is a horse memory query first
        horse_response = horse_adapter.handle_query(question)
        if horse_response is not None:
            logging.info(f"🐴 Horse memory response: {horse_response}")
            return {"response": horse_response}
            
        # If not a horse memory query, use OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[
                {"role": "system", "content": "You are a horse trainer."}, 
                {"role": "user", "content": question}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        logging.info(f"✅ Response generated")
        return {"response": answer}
    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
