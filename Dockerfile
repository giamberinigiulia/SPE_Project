FROM python:3.12.0-slim

RUN apt-get update && apt-get install -y \
    procps \
    psmisc \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose a volume for the figures
VOLUME [/app/data]

CMD ["/bin/bash"]
