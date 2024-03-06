# Use an explicit version of the Python slim image
FROM python:3.12.1-slim as base

# Set up environment variables
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1

WORKDIR $APP_HOME

# Install production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image
COPY . .

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Run the web service on container startup using Gunicorn
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 app:app
