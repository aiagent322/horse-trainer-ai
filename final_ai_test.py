import openai

# Set your OpenAI API key
openai.api_key = 
"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"

# Test request to OpenAI
try:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Hello, world!",
        max_tokens=10
    )
    print("Test successful:", response.choices[0].text.strip())
except Exception as e:
    print("Error:", e)
