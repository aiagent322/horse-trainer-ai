#!/bin/bash
set -e
set -u

REQUIRED_VARS=("OPENAI_API_KEY" "DB_URL" "AGENTOPS_API_KEY")

for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var:-}" ]; then
    echo "Error: $var is not set!"
    exit 1
  fi
done

echo "All required environment variables are set."

