# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Langflow runs on
EXPOSE 7860

# Start Langflow when the container launches
CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "7860"]

