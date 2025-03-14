import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def horse_trainer_agent(user_input):
    """
    AI-powered horse trainer that provides advice to students.
    """
    system_message = (
    "You are an experienced horse trainer specializing in reining, 
dressage, and horsemanship. "
    "Provide clear and actionable training advice for riders of all 
levels. "
    "Ensure responses are practical, safe, and easy to understand."
)


    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ]
    )

    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("Welcome to Horse Trainer AI! Ask for horse training advice.")
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit", "stop"]:
            print("Goodbye!")
            break
        response = horse_trainer_agent(user_query)
        print("Horse Trainer AI:", response)


