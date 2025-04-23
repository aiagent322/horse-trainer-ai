#!/usr/bin/env python3
from dotenv import load_dotenv  # Add this import
from openai import OpenAI
import os

# Load .env file from HOME directory
load_dotenv(os.path.expanduser('~/.env'))  # Critical fix

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Now will work

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    user_input = input("You: ")
    print("AI:", generate_response(user_input))
