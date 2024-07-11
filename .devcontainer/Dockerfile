# Using Python image
FROM python:3.11.9-slim

# Set working directory
WORKDIR /workspace

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /workspace
COPY . .

