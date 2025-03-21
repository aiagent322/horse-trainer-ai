from setuptools import setup, find_packages

setup(
    name="horse-trainer-ai",
    version="0.1.0",
    description="AI system for personalized horse training recommendations",
    author="AI Agent",
    author_email="aiagent322@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "fastapi>=0.75.0",
        "uvicorn>=0.17.0",
        "pydantic>=1.9.0",
        "python-dotenv>=0.19.0",
        "requests>=2.27.0",
        "joblib>=1.1.0",
    ],
    entry_points={
        "console_scripts": [
            "horse-trainer=src.main:main",
            "horse-trainer-api=src.api.endpoints:start",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
