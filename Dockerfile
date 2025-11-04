FROM python:3.11-slim

LABEL maintainer="AIKAILNOV4 Team <support@aikailnov4.com>"
LABEL description="AI-Powered Kali Linux Security System"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nmap \
    git \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs reports && \
    chmod +x scripts/*.sh scripts/*.py

# Initialize database
RUN python3 scripts/init_db.py

# Create non-root user
RUN useradd -m -u 1000 aikail && \
    chown -R aikail:aikail /app

USER aikail

# Expose API port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Default command
CMD ["python3", "src/core/aikail.py", "--help"]
