FROM python:3.12.0-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME=World

# Expose a volume for the figures
VOLUME /app/data


CMD ["python", "main.py", "run", "-s", "10", "-a", "5", "-u", "8", "10", "-t", "60", "-k", "4"]

