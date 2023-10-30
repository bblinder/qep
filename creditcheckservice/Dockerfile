FROM python:3.11-slim
# Set working directory
WORKDIR /app

# Copy requirements over
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Bootstrap Splunk Py Instrumentation
RUN splunk-py-trace-bootstrap

# Copy main app
COPY main.py .

# Set the entrypoint command to run the application
CMD ["splunk-py-trace", "python3", "main.py"]
