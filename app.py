from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
model = load_model('models/emotion_model.keras')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
EMOTIONS = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Sad', 5:'Surprise', 6:'Neutral'}

@app.get("/")
def home():
    return {"message": "Mood Tracker API Active"}

@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    image = np.array(image)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return {"emotion": "No Face", "confidence": 0.0}

    x, y, w, h = faces[0]
    roi = gray[y:y+h, x:x+w]
    roi = cv2.resize(roi, (48, 48))
    roi = roi.astype('float32') / 255.0
    roi = np.expand_dims(roi, axis=0)
    roi = np.expand_dims(roi, axis=-1)

    prediction = model.predict(roi, verbose=0)
    max_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction))
    
    return {"emotion": EMOTIONS[max_index], "confidence": round(confidence * 100, 2)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)