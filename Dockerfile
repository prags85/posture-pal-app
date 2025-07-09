FROM python:3.10

WORKDIR /app

COPY backend/ /app/

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
