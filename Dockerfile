FROM python:3.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip nmap && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the application code
COPY . /app/

# Copy .env file to the container
COPY .env /app/.env

# Create log directory
RUN mkdir -p /app/logs

# Expose the application port
EXPOSE ${HTTP_PORT}
