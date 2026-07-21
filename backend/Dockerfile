# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (required for easyocr and pymupdf)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code
COPY . .

# Expose the port (Railway typically uses PORT environment variable, which we will bind in uvicorn)
EXPOSE 8000

# Start Uvicorn, mapping to Railway's dynamic PORT or fallback to 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
