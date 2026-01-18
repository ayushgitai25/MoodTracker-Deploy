FROM python:3.10-slim

# 1. Install System Dependencies as Root
# We combine your 'working' list (procps, curl) with the 'CV' list (libgl1)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    bash \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Create non-root user (Hugging Face Default is UID 1000)
# This prevents "Permission Denied" errors!
RUN useradd -m -u 1000 user

# 4. Set directory and Copy Files
WORKDIR /home/user/app
COPY --chown=user:user . .

# 5. Switch to the non-root user
USER user

# 6. The Start Command (Optimized)
# Note: I changed 'frontend_app.py' to 'app_ui.py' to match your actual filename!
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info & streamlit run app_ui.py --server.port=7860 --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false --server.enableXsrfProtection=false"]