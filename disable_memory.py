from crewai import LLM

# Initialize the LLM with memory disabled
llm = LLM(
    model="gemini/gemini-pro",  # Replace with your model name
    api_key="YOUR_GEMINI_API_KEY",  # Replace with your API key
    memory=False  # Disable memory
)

print("Memory is disabled for the LLM configuration.")
# Define a prompt and get a response
prompt = "Explain the basics of horse training."
response = llm.run(prompt)

# Print the response
print("Response from the LLM:")
print(response)

