# ============================================
# Echo Backend Dockerfile
# ============================================

# Base Image
FROM python:3.11-slim

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Linux Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set Working Directory
WORKDIR /app

# Copy Requirements
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python Packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project
COPY . .

# Expose FastAPI Port
EXPOSE 8000

# Start FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]