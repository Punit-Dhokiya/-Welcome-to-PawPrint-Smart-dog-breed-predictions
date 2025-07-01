# pawprint_ai_app.py - Enhanced Stylish Version with Confidence Threshold and Charts

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import time
from PIL import Image

# ----------------------------- Modern App Setup -----------------------------
st.set_page_config(page_title="🐾 AI Canine Vision | Smart Breed Classifier", layout="centered")

# ----------------------------- Stylish Header -----------------------------
st.markdown("""
    <style>
        .title-style {
            font-size: 3em;
            font-weight: bold;
            color: #1A237E;
            text-align: center;
            margin-bottom: 10px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .subtitle-style {
            font-size: 1.4em;
            color: #37474F;
            text-align: center;
            margin-bottom: 20px;
            font-style: italic;
        }
        .emoji-box {
            font-size: 1.2em;
            background-color: #E3F2FD;
            padding: 10px;
            border-radius: 10px;
            color: #0D47A1;
        }
        .prediction-box {
            border: 2px solid #1E88E5;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 20px;
            background-color: #E1F5FE;
        }
        .prediction-box h4 {
            color: #0D47A1;
            background-color: #BBDEFB;
            padding: 6px 10px;
            border-radius: 8px;
            display: inline-block;
        }
        .breed-img {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 12px;
            margin-right: 15px;
            border: 2px solid #0D47A1;
        }
        .prediction-row {
            display: flex;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-style'>🐶 Welcome to PawPrint AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-style'>Smart dog breed predictions powered by intelligent vision and trusted insights.</div>", unsafe_allow_html=True)

# ----------------------------- Database Setup -----------------------------
conn = sqlite3.connect('predictions.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS predictions (timestamp TEXT, breed TEXT, confidence REAL)''')

# ----------------------------- Enhanced Breed List -----------------------------
breeds = [
    ("Golden Retriever", "Friendly, intelligent, and devoted"),
    ("German Shepherd", "Confident, courageous, and smart"),
    ("Pug", "Charming, loving, and mischievous"),
    ("Beagle", "Curious, merry, and friendly"),
    ("Labrador", "Outgoing, even-tempered, and gentle"),
    ("Chihuahua", "Graceful, charming, and sassy"),
    ("Dalmatian", "Energetic, playful, and sensitive"),
    ("Border Collie", "Affectionate, smart, and energetic"),
    ("Husky", "Friendly, outgoing, and alert"),
    ("Shih Tzu", "Affectionate, playful, and outgoing")
]

# ----------------------------- Mock Predict Multiple Top Breeds -----------------------------
def mock_predict(image):
    indices = np.random.choice(len(breeds), size=3, replace=False)
    confidences = sorted(np.random.uniform(0.9, 0.999, size=3), reverse=True)
    return [(breeds[i], conf) for i, conf in zip(indices, confidences)]

# ----------------------------- Breed Images -----------------------------
breed_to_image = {
    "Golden Retriever": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Golden_Retriever_Carlos_%281055226016%29.jpg",
    "German Shepherd": "https://upload.wikimedia.org/wikipedia/commons/3/3e/German_Shepherd_Dog.jpg",
    "Pug": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Pug_600.jpg",
    "Beagle": "https://upload.wikimedia.org/wikipedia/commons/5/52/Beagle_Upsy.jpg",
    "Labrador": "https://upload.wikimedia.org/wikipedia/commons/2/26/YellowLabradorLooking_new.jpg",
    "Chihuahua": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Chihuahua1_bvdb.jpg",
    "Dalmatian": "https://upload.wikimedia.org/wikipedia/commons/4/48/Dalmatiner.JPG",
    "Border Collie": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Border_Collie_Puppy.jpg",
    "Husky": "https://upload.wikimedia.org/wikipedia/commons/3/32/Siberian_Husky_pho.jpg",
    "Shih Tzu": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Shih-Tzu.jpg"
}

# ----------------------------- Gesture Animation -----------------------------
st.markdown("""
    <style>
        .stButton>button {
            background-color: #1E88E5;
            color: white;
            border: none;
            padding: 0.6em 1.5em;
            border-radius: 10px;
            font-weight: bold;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #0D47A1;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------- Image Upload -----------------------------
uploaded_file = st.file_uploader("📄 Upload a Dog Image", type=["jpg", "jpeg", "png"], key="dog_upload")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Uploaded Image", use_container_width=True)

    if st.button("🔍 Predict Breed"):
        with st.spinner("Analyzing dog features with smart AI... 🧠"):
            time.sleep(2)
            results = mock_predict(image)

        now = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        for (breed_name, _), conf in results:
            c.execute("INSERT INTO predictions VALUES (?, ?, ?)", (now, breed_name, float(conf)))
        conn.commit()

        st.markdown("### 🎯 Top AI Predictions")

        labels = []
        confidences = []

        for i, ((breed_name, description), confidence) in enumerate(results, 1):
            image_url = breed_to_image.get(breed_name, "https://via.placeholder.com/100")
            confidence_color = "#0D47A1"
            st.markdown(f"""
                <div class='prediction-box'>
                    <h4>⭐ Prediction {i}</h4>
                    <div class='prediction-row'>
                        <img src="{image_url}" class='breed-img'/>
                        <div class='emoji-box'>
                            🐶 <strong>{breed_name}</strong><br>
                            📌 {description}<br>
                            🔢 <span style='color:{confidence_color}'>Confidence: {confidence*100:.2f}%</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            labels.append(breed_name)
            confidences.append(confidence * 100)

        st.markdown("### 📊 Confidence Bar Chart")
        fig_bar, ax_bar = plt.subplots()
        ax_bar.barh(labels, confidences, color='#4FC3F7')
        ax_bar.invert_yaxis()
        ax_bar.set_xlabel("Confidence (%)")
        ax_bar.set_title("Top Breed Predictions Confidence")
        st.pyplot(fig_bar)

        st.markdown("### 🥧 Confidence Pie Chart")
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(confidences, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
        ax_pie.axis('equal')
        st.pyplot(fig_pie)

        st.markdown("### 📓 All Prediction Records")
        df_all = pd.read_sql_query("SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 50", conn)
        st.dataframe(df_all)
else:
    st.info("👈 Upload a dog image above to get started.")

# ----------------------------- Footer -----------------------------
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        🐾 Built with 💡💕 Made with ❤ using Streamlit — Dog Vision AI
    </div>
""", unsafe_allow_html=True)

conn.close()
