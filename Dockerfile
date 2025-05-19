# Use an official Python image as the base
# python:3.12-slim is a good choice for smaller size
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

# Copy the rest of your application code into the container
COPY . .

# Expose the port your FastAPI application runs on (default is 8000 for Uvicorn)
EXPOSE 8000

# Command to run your application using Uvicorn
# Replace 'main:app' if your FastAPI app is in a different file or variable name
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
