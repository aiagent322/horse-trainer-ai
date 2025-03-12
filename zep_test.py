from langchain.memory import ZepMemory
from langchain.chat_models import ChatOpenAI

# Zep API URL (Change if using Zep Cloud)
ZEP_API_URL = "http://localhost:8000"

# Connect to OpenAI
llm = ChatOpenAI(model_name="gpt-4", openai_api_key="YOUR_OPENAI_KEY")

# Connect Zep Memory
memory = ZepMemory(
    session_id="user-session",
    url=ZEP_API_URL
)

# Save a message in memory
memory.save_context(
    {"input": "Hello, how are you?"},
    {"output": "I'm doing well! How can I help you?"}
)

# Retrieve memory
print(memory.load_memory_variables({}))

