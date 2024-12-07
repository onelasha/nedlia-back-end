FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better cache usage
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary application files
COPY main.py .
COPY sonar-project.properties .
COPY pytest.ini .
COPY README.md .

# Use non-root user for security
RUN useradd -m myuser
USER myuser

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-", "--worker-class", "uvloop"]
