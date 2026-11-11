FROM python:3.11-slim

# Create a non-root user for security
RUN useradd -m -u 1000 sandboxuser

# Install common testing dependencies globally
RUN pip install --no-cache-dir pytest==8.2.2

WORKDIR /app
USER sandboxuser