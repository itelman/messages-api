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
EXPOSE 10000

# Run the app using Uvicorn
CMD ["gunicorn", "-w", "1", "main:app", "--bind", "0.0.0.0:10000", "--worker-class", "uvicorn.workers.UvicornWorker"]
