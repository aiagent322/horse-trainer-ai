#!/bin/bash
uvicorn trainer_ai:app --host ${HOST:-0.0.0.0} --port ${APP_PORT:-10000}

