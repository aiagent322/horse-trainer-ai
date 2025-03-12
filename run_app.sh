#!/bin/bash

# Exit on errors and unset variables
set -e
set -u

# Define required environment variables
REQUIRED_VARS=("OPENAI_API_KEY" "DB_URL" "AGENTOPS_API_KEY"
#!/bin/bash

# Exit on errors and unset variables
set -e
set -u

# Define required environment variables
REQUIRED_VARS=("OPENAI_API_KEY" "DB_URL" "AGENTOPS_API_KEY")

# Check if required environment variables are set
for var in "${REQUIRED_VARS[@]}"; do if [ -z "${!var:-}" ]; then
    echo "Error: $var is not set!"
    exit 1
  fi
done
  if [ -z "${!var:-}" ]; then
    echo "Error: $var is not set!"
    exit 1
  fi
done#!/bin/bash

# Exit on errors and unset variables
set -e
set -u

# Define required environment variables
REQUIRED_VARS=("OPENAI_API_KEY" "DB_URL" "AGENTOPS_API_KEY")

# Check if required environment variables are set
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var:-}" ]; then
    echo "Error: $var is not set!"
    exit 1
  fi
done

echo "All required environment variables are set."

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
  echo "Virtual environment activated."
else
  echo "Error: Virtual environment not found."
  exit 1
fi

# Run the application
echo "Starting application..."
python main.py || { echo "Error: Application encountered an issue"; exit 
1; }

echo "Application completed successfully."


echo "All required environment variables are set."

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
  echo "Virtual environment activated."
else
  echo "Error: Virtual environment not found."
  exit 1
fi

# Run the application
echo "Starting application..."
python main.py || { echo "Error: Application encountered an issue"; exit 
1; }

echo "Application completed successfully."

