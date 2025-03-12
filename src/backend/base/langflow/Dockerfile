# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Google Cloud Run will use
EXPOSE 8080

# Use environment variable for port (required by Cloud Run)
CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "8080"]

