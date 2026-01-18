import streamlit as st
import requests
import os
from PIL import Image

import random

def get_genz_vibe(emotion):
    """
    Translates boring emotions into Gen Z slang.
    """
    vibes = {
        "happy": [
            "Bestie is GLOWING! Main character energy fr. ✨",
            "W Rizz. Absolutely slaying the day. 💅",
            "No cap, you lookin' fresh. 🧢🚫"
        ],
        "sad": [
            "Down bad? Go touch grass or get a sweet treat. 🍩",
            "It's giving... moody aesthetic. Alexa play Lana Del Rey. 🎻",
            "Big oof. Emotional damage. 💀"
        ],
        "angry": [
            "Who hurt you? You woke up and chose violence. 🔪",
            "Lowkey salty. Take a chill pill fam. 🧂",
            "Pressed. Extremely pressed. 😤"
        ],
        "surprise": [
            "GAGGED. Shooketh. I was not ready. 🤯",
            "Bombastic side eye... what did you just see? 👀",
            "Real life plot twist just dropped. 🎬"
        ],
        "fear": [
            "Spooky szn came early? 👻",
            "Ngl you look terrified. Blink twice if you need help. 🚩",
            "Anxiety has entered the chat. 📉"
        ],
        "disgust": [
            "Major ick. The cringe is real. 🤢",
            "Bombastic side eye. Criminal offensive side eye. 😒",
            "Eww brother, eww. What's that? 🤮"
        ],
        "neutral": [
            "NPC energy. Just vibes. 😐",
            "Mid. Not great, not terrible. Just... existing. 😶",
            "Poker face strong. Are you even real? 🤖"
        ]
    }
    
    # Return a random funny message for that emotion
    # .lower() ensures it matches regardless of capitalization
    return random.choice(vibes.get(emotion.lower(), ["Vibe check failed. 404 Error. 👾"]))



# --- CONFIGURATION ---
# Default to localhost, but allow Cloud override
DEFAULT_URL = "http://localhost:8000/predict"
API_URL = os.getenv("BACKEND_URL", DEFAULT_URL)

st.set_page_config(page_title="CNN-RNN Mood Tracker (Gen-Z style)", page_icon="🧠", layout="wide")

# --- CYBERPUNK CSS STYLING ---
st.markdown("""
    <style>
    /* 1. Main Background */
    .stApp {
        background-color: #050505;
        color: #ffffff;
    }
    
    /* 2. Neon Title (Updated Name) */
    h1 {
        font-family: 'Courier New', monospace;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00f2ff, #ff0055);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0px;
    }

    /* 3. Metric Boxes */
    div[data-testid="metric-container"] {
        background-color: #111;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
    }
    label[data-testid="stMetricLabel"] {color: #ff0055 !important;}
    div[data-testid="stMetricValue"] {color: #ffffff !important; font-family: 'Courier New';}

    /* 4. HIGH VISIBILITY BUTTONS */
    /* Target the camera button to make it Neon Pink/Blue */
    button {
        background-color: #ff0055 !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        border: 2px solid #00f2ff !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: 0.3s ease;
    }
    button:hover {
        background-color: #00f2ff !important;
        color: black !important;
        box-shadow: 0 0 25px #00f2ff;
    }
    
    /* Style the label above camera */
    .camera-label {
        font-family: 'Helvetica', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        color: #00f2ff;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- EMOJI MAPPING ---
EMOJI_MAPPING = {
    'Angry': 'Angry 😡', 'Disgust': 'Disgust 🤢', 'Fear': 'Fear 😱', 
    'Happy': 'Happy 😄', 'Sad': 'Sad 😢', 'Surprise': 'Surprise 😲', 'Neutral': 'Neutral 😐'
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Network Config")
    # We keep the input here so you can change it if needed, but it's hidden from main UI
    backend_url = st.text_input("Backend API URL", value=API_URL)

# --- UI LAYOUT ---
# UPDATED TITLE AS REQUESTED
st.title("CNN-ANN-RNN MOOD TRACKER")
st.markdown("<p style='text-align: center; color: #b0b0b0;'>Hybrid Neural Architecture • Facial Expression Analysis</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown("### 📡 Live Telemetry")
    st.info("System Ready. Initialize sensor below.")
    
    # Empty slots for data
    kpi1 = st.empty()
    kpi2 = st.empty()
    
    # NOTE: API URL is removed from here as requested

with col2:
    # Custom Label
    st.markdown('<p class="camera-label">📸 SENSOR INPUT ZONE</p>', unsafe_allow_html=True)
    
    # Camera Input
    img_file = st.camera_input(label="Capture Image")

# --- LOGIC (Send to Backend) ---
if img_file is not None:
    # Show the captured image
    st.image(img_file, caption="Processing Input...", width=400)
    
    with st.spinner("🧠 Running CNN-RNN Inference..."):
        try:
            # Prepare file for upload
            files = {"file": ("image.jpg", img_file.getvalue(), "image/jpeg")}
            
            # POST Request to App.py
            response = requests.post(backend_url, files=files)
            
            if response.status_code == 200:
                data = response.json()
                raw_emotion = data['emotion']
                conf = data['confidence']
                
                # 1. Map to Emoji
                final_label = EMOJI_MAPPING.get(raw_emotion, raw_emotion)
                
                # 2. Get the Gen Z Vibe Message
                vibe_text = get_genz_vibe(raw_emotion)

                # 3. Update Standard Metrics
                kpi1.metric(label="PREDICTED EMOTION", value=final_label)
                kpi2.metric(label="CONFIDENCE", value=f"{conf}%")

                # 4. SHOW THE VIBE CHECK (This is the new part!)
                st.markdown("---")
                st.markdown(f"<h2 style='text-align: center; color: #00FF00;'>✨ VIBE CHECK ✨</h2>", unsafe_allow_html=True)
                st.info(f"**{vibe_text}**")

                if "Happy" in raw_emotion:
                    st.balloons()
            else:
                st.error(f"⚠️ Server Error: {response.text}")
                
        except Exception as e:
            st.error(f"❌ Connection Failed.")
            st.warning(f"Error Details: {e}")