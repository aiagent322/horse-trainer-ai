FROM python:3.11
WORKDIR /app
RUN pip install --no-cache-dir langflow
ENV PORT=8080
EXPOSE 8080
CMD ["python3", "-m", "langflow", "run", "--host=0.0.0.0", "--port=8080"]

