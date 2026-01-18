# Use a lightweight Python version
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# 1. Install System Dependencies
# FIX: Changed 'libgl1-mesa-glx' to 'libgl1' because the old package name is deprecated
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of your app code
COPY . .

# 4. The Start Command
CMD ["bash", "-c", "uvicorn app:app --host 127.0.0.1 --port 8000 > /dev/null 2>&1 & streamlit run app_ui.py --server.port 7860 --server.address 0.0.0.0"]