FROM python:3.12.0-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt


# Expose a volume for the figures
VOLUME /app/data


CMD ["python", "main.py", "run"]