# Dockerfile for Agrisensa Flask API
# -------------------------------------------------
# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for OpenCV and building wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create necessary directories and set permissions for HF Spaces (user 1000)
RUN mkdir -p uploads/pdfs uploads/temp_images logs output instance && \
    chmod -R 777 uploads logs output instance

# Expose the port (Railway/Render will inject PORT env var)
EXPOSE 7860

# Use gunicorn for production serving (Shell form to expand $PORT)
# Default to port 7860 if PORT is not set (Hugging Face default)
CMD gunicorn run:app -b 0.0.0.0:${PORT:-7860} --workers 2 --timeout 120
