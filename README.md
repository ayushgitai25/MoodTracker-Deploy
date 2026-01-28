---
title: Hybrid CNN-ANN Mood Tracker
emoji: 🧠
colorFrom: blue
colorTo: pink
sdk: docker
pinned: false
app_port: 7860
---

# 🧠 Hybrid CNN-ANN Emotion Recognition System

[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

> A real-time facial emotion recognition system powered by a custom **Hybrid CNN-ANN** architecture. It detects micro-expressions in milliseconds, translates them into 7 core emotions, and delivers a culturally relevant "Gen Z Vibe Check."

---

### 🎮 **[Click Here to Launch Live Demo](https://huggingface.co/spaces/ayushhgface25/CRNN_MoodTracker)**
*(Please allow approx. 30 seconds for the Docker container to spin up from sleep mode)*

---

## ✨ Project Overview

This application isn't just another generic emotion classifier. It's a full-stack engineered system designed for **speed, stability, and user experience**.

It uses a decoupled microservice architecture where a **FastAPI** backend handles heavy Deep Learning inference, and a **Streamlit** frontend provides a snappy, reactive UI.

![App UI Screenshot](https://via.placeholder.com/800x400.png?text=Insert+Your+App+UI+Screenshot+Here+(e.g.,+Face+with+Vibe+Check))
*Real-time inference showing emotion probability bars and the "Vibe Check" output.*

---

## 🚀 Key Technical Features

* **🧠 Hybrid CNN-ANN Model:** A custom-designed, lightweight (<5MB) architecture utilizing Global Average Pooling for efficient edge inference, achieving **52.4% accuracy** on FER-2013.
* **⚡ Real-Time Performance:** Optimized OpenCV preprocessing pipeline delivers consistent **30+ FPS** on standard CPU hardware.
* **🌊 Temporal Smoothing Algorithm:** Implemented a custom O(1) deque-based logic to analyze frame history, reducing prediction "jitter/flickering" by **~40%** for stable results.
* **🐳 Dockerized Microservices:** Fully containerized full-stack application separating the inference engine (FastAPI) from the UI (Streamlit) for scalable deployment.

---

## 🛠️ System Architecture

How do we get from raw pixels to a "Vibe Check"?

![Architecture Diagram](https://github.com/ayushgitai25/MoodTracker-Deploy/blob/main/cnn_ann_architecture.png)

1.  **Input:** Raw video frames are captured asynchronously.
2.  **Preprocessing (OpenCV):** Faces are detected using Haar Cascades, cropped (ROI), converted to grayscale, and normalized.
3.  **Inference (CNN-ANN):** The processed tensor is fed into the hybrid model to generate probability logits.
4.  **Temporal Smoothing:** Predictions are passed through a sliding-window buffer to stabilize emotions over time.
5.  **Output:** Final stabilized emotion is mapped to a "Gen Z Vibe Check" message and displayed on the UI.

---

## 📂 Local Setup & Training

**Important Data Policy:** The training dataset is **NOT** included in this repository due to licensing and size constraints.

To run training locally, you must download the **FER-2013** dataset separately.

### **1. Get the Data**
Download the dataset from Kaggle:
🔗 **[Kaggle FER-2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)**

### **2. Organize Folders**
Extract the data and ensure your project structure looks exactly like this:
```text
MoodTracker/
├── data/
│   ├── train/ (contains 7 subfolders: angry, happy, neutral, etc.)
│   └── test/  (contains 7 subfolders: angry, happy, neutral, etc.)
├── models/    (saved model weights will go here)
├── train.py
├── app.py
└── ...
