---
title: CNN-RNN Mood Tracker
emoji: 🧠
colorFrom: blue
colorTo: pink
sdk: docker
pinned: false
app_port: 7860
---

# 🧠 CNN-ANN Emotion Recognition System (Gen Z Edition)

A real-time facial emotion recognition system powered by a hybrid **Convolutional Neural Network (CNN)** architecture. This application detects micro-expressions in milliseconds and classifies them into 7 core emotions (Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral) with a "Vibe Check" twist.

### 🔗 **[Click Here to Try the Live Demo](https://huggingface.co/spaces/ayushhgface25/CRNN_MoodTracker)**

![Demo Preview](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3R4cW55eHl5eHl5eHl5/giphy.gif)

---

## 📂 Dataset Information (Important!)

**Note:** The training dataset is **NOT** included in this repository due to its large size.

The model was trained on the **FER-2013 (Facial Emotion Recognition)** dataset. If you wish to retrain the model locally, please download the data from Kaggle and place it in a folder named `data/`.

🔗 **Download Dataset:** [Kaggle FER-2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)

### **Folder Structure for Training**
If you download the data, organize it like this:
```text
MoodTracker/
├── data/
│   ├── train/ (contains 7 subfolders: angry, happy, etc.)
│   └── test/  (contains 7 subfolders: angry, happy, etc.)
