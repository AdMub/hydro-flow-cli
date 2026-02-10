# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . /app

# CRITICAL: Install dependencies with quotes to avoid shell errors
# We install the local package and specific versions in one go
RUN pip install --no-cache-dir . "numpy<2.0" scipy matplotlib pandas

# Set the Python Path so the container sees the internal modules
ENV PYTHONPATH=/app

# Define environment variable
ENV NAME=HydroFlow

# Run hydro when the container launches
ENTRYPOINT ["hydro"]
CMD ["--help"]