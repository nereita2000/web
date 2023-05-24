# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port that the application listens on
EXPOSE 80

# Set the entry point command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
