from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os

# Get OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("ERROR: OPENAI_API_KEY is not set!")

# Initialize AI Model
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=api_key)

# Enable Memory
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Simple chat loop
print("\n🔹 AI Agent is ready! Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    response = conversation.predict(input=user_input)
    print("AI:", response)

