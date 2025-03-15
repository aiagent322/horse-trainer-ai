#!/bin/bash
cd /opt/render/project/src  # Navigate to correct Render directory
source venv/bin/activate    # Activate virtual environment
exec uvicorn main:app --host 0.0.0.0 --port $PORT



