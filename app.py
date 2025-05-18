import streamlit as st
import requests
from gtts import gTTS
import uuid
import base64
import os

# ---------- CONFIG ----------
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-3.5-turbo"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Text-to-Speech Chat"
}

# ---------- FUNCTIONS ----------
def chat_with_openrouter(prompt):
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    try:
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"❌ ERROR: {e}")
        st.code(response.text)
        return "ขออภัย ระบบไม่สามารถตอบกลับได้ในตอนนี้"

def speak_text(text):
    tts = gTTS(text=text, lang='th')
    filename = f"reply_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

def autoplay_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            md = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error("ไม่สามารถเล่นเสียงอัตโนมัติ")

# ---------- UI ----------
st.set_page_config(page_title="Text-to-Voice Chat", layout="centered")
st.markdown("""
    <style>
        html, body, .stApp {
            font-family: "Cordia New", sans-serif;
            font-size: 22px;
        }
        h1 {
            font-size: 22px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💬 พิมพ์ถาม → 🧠 AI → 🔊 พูดคำตอบ")

question = st.text_input("พิมพ์คำถามของคุณที่นี่:")

if st.button("ถามเลย") and question.strip():
    st.info("🤖 กำลังคิดคำตอบ...")
    reply = chat_with_openrouter(question)
    st.markdown(f"**🤖 AI ตอบว่า:** {reply}")

    st.info("🔊 กำลังพูดคำตอบ...")
    audio_file = speak_text(reply)
    autoplay_audio(audio_file)
    st.audio(audio_file, format="audio/mp3")
