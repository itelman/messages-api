# Use a lightweight Python image
FROM python:3.12-slim

WORKDIR /

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Set the entrypoint to use the virtual environment’s Python and Gunicorn
CMD ["/app/venv/bin/gunicorn", "-w", "4", "main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]
