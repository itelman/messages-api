# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the app using Gunicorn with Uvicorn workers
CMD ["gunicorn", "-w", "4", "main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]

