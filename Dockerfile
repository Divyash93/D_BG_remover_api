FROM python:3.9-slim

WORKDIR /app

LABEL maintainer="D_BG_remover"
LABEL version="1.0.0"
LABEL description="Background removal API powered by rembg"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p static/uploads

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000
ENV API_NAME="D_BG_remover"

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 