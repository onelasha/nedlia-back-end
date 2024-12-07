FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better cache usage
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Use non-root user for security
RUN useradd -m myuser
USER myuser

# Expose the port
EXPOSE 8080

# Command to run the application
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8080", "--workers", "4", "--access-logfile", "-", "--worker-class", "uvloop"]
