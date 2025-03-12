from fastapi import FastAPI
from crewai import Agent, Task, Crew

app = FastAPI()

# Define the Horse Trainer AI agent
trainer = Agent(
    role="Horse Trainer AI",
    goal="Assist users in improving horse training techniques",
    backstory="A expert horse trainer in western disciplines",

    verbose=True,
    llm="gpt-4-turbo"
)

# Define a training task
training_task = Task(
    description="Provide guidance on horse training techniques.",
    agent=trainer,
    expected_output="Detailed training tips on stopping, lead changes"
)

# Create a crew with the trainer and task
crew = Crew(agents=[trainer], tasks=[training_task])

@app.get("/")
def read_root():
    return {"message": "Horse Trainer AI is running!"}

@app.get("/ask/")
def ask_question(question: str):
    response = crew.kickoff(inputs=question)
    return {"question": question, "response": response}

