# Use an official Python runtime as a parent image
FROM python:3.12.0-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME=World

# Use a volume to persist data and source files
VOLUME ["/app"]

# Run the application with the specified command
CMD ["/bin/bash"]
