# Use multi-stage build for smaller image
FROM python:3.13-slim as builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.13-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Cloud Run injects PORT env variable, default to 8080
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Run the application
# Use $PORT to read from environment variable
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}