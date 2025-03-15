#!/bin/bash
cd "$(dirname "$0")"  # Change to the script's directory

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Start the FastAPI app with Uvicorn
exec uvicorn main:app --host 0.0.0.0 --port=${PORT:-7860}

