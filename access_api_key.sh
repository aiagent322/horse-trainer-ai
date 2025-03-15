#!/bin/bash

# Source the ~/.zshrc file to load environment variables
source ~/.zshrc

# Check if the OpenAI API key exists
if [[ -z "$OPENAI_API_KEY" ]]; then
  echo "❌ ERROR: OpenAI API Key not found in ~/.zshrc"
else
  echo "✅ OpenAI API Key Loaded: ${OPENAI_API_KEY:0:5}... [HIDDEN]"
fi

