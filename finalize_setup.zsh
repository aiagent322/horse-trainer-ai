from setuptools import setup, find_packages

setup(
    name="horse-trainer-ai",
    version="0.1.0",
    description="AI system for personalized horse training recommendations",
    author="AI Agent",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
    ],
)
