import openai, os, logging; from fastapi import FastAPI, HTTPException; 
logging.basicConfig(filename="app.log", level=logging.INFO, 
format="%(asctime)s - %(levelname)s - %(message)s"); PORT = 
int(os.getenv("APP_PORT", 10000)); HOST = os.getenv("HOST", "0.0.0.0"); 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY"); if not OPENAI_API_KEY: 
logging.error("❌ ERROR: OPENAI_API_KEY is missing!"); raise 
ValueError("ERROR: API Key is not set in environment variables."); 
openai.api_key = OPENAI_API_KEY; app = FastAPI(); @app.get("/") def 
home(): logging.info("🏠 Home endpoint accessed."); return {"message": 
"Welcome to Horse Trainer AI"}; @app.get("/debug") def debug_api_key(): 
key_status = "SET" if OPENAI_API_KEY else "MISSING"; logging.info(f"🔍 
Debug API Key Check: {key_status}"); return {"API_KEY_STATUS": key_status, 
"API_KEY": OPENAI_API_KEY[:5] + "**********" if OPENAI_API_KEY else 
"MISSING"}; @app.get("/ask") def horse_trainer_agent(question: str): 
logging.info(f"📢 Received question: {question}"); try: response = 
openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", 
"content": "You are a horse trainer."}, {"role": "user", "content": 
question}]); answer = response["choices"][0]["message"]["content"]; 
logging.info(f"✅ Response: {answer[:50]}..."); return {"response": 
answer}; except Exception as e: logging.error(f"❌ ERROR: {str(e)}"); 
raise HTTPException(status_code=500, detail="Error processing request.")

