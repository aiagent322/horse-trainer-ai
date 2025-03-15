import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("API Key is missing!")

openai.api_key = OPENAI_API_KEY

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": "You are a horse trainer."},
              {"role": "user", "content": "How do I train a horse?"}]
)

print(response["choices"][0]["message"]["content"])

