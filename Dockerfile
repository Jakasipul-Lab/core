# Use Python 3.11 slim image for FastAPI
FROM python:3.11-slim

# Set the root working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies (Fixed file name case)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything inside your local app folder straight into /app
COPY app/ ./

# Create non-root user for security
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check (Hits your FastAPI health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application (Now perfectly matches the folder layout)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
