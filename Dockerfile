# Use the official Python 3.8 image as the base image
FROM python:3.8-slim

# Install system dependencies required by mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set the command to run the application
CMD ["python", "main.py"]
