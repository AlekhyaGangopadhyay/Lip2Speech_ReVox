FROM python:3.9-slim

# Install system dependencies (OpenCV needs OpenGL/GLib, pyttsx3 needs espeak on Linux)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    espeak \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install CPU-only PyTorch first (speeds up build dramatically by downloading ~250MB instead of ~3GB+ CUDA packages)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy requirements and install remaining dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the app files
COPY . .

# Flask runs on port 7860 on Hugging Face
EXPOSE 7860

# Start Flask on port 7860
CMD ["python", "app.py"]
