import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

# Debugging: Print API token to check if it loads correctly
api_token = os.getenv("LANGFLOW_API_TOKEN")
print(f"Debug: Loaded API token: {api_token}")

# Stop execution if the API token is missing
if not api_token or api_token.strip() == "":
    raise ValueError("ERROR: LANGFLOW_API_TOKEN is missing. Check your .env file.")


# Define Langflow API URL (replace with actual endpoint)
url = "https://api.langflow.org/v1/your-endpoint"  
# AstraCS:zWGzWHfcfBRQMgjlPaIfxmui:31a8e0e32053d74bf9c52aed9de63e0bb4d8258dc3c

# Optional query parameters
params = {"stream": "false"}

# Correct headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"
}

# Debugging: Print headers to verify
print(f"Debug: Headers -> {headers}")

# Make a test request
try:
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("✅ Success:", response.json())
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")

