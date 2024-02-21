FROM python:3.10-alpine

# Install dependencies for compiling TgCrypto
RUN apk add --no-cache gcc \
    g++

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
