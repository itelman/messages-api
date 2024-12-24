# Use a lightweight Python image
FROM python:3.12-slim

# Install dependencies for virtual environment
RUN apt-get update && apt-get install -y python3-venv

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment in the /app directory
RUN python3 -m venv /app/venv

# Activate the virtual environment and install dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the desired port (e.g., 8000)
EXPOSE 8000

# Set the entrypoint to use the virtual environment’s Python and Gunicorn
CMD ["/app/venv/bin/gunicorn", "-w", "4", "main:app", "--bind", "0.0.0.0:8000", "--worker-class", "uvicorn.workers.UvicornWorker"]
