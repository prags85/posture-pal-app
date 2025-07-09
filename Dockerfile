# Use Python 3.10 as base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Flask default is 5000)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
