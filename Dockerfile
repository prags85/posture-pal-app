# Use a slim Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend source code
COPY backend/ .

# Expose port
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
