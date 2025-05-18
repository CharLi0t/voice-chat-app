import streamlit as st
import requests
from gtts import gTTS
import uuid
import base64
import os
import time

# ---------- CONFIG ----------
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", None)
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
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as http_err:
        st.error("❌ ไม่สามารถเชื่อมต่อกับ OpenRouter ได้ (เช่น 401 Unauthorized)")
        st.code(str(http_err), language="text")
        return "ขออภัย ระบบไม่สามารถเชื่อมต่อกับ GPT ได้ในขณะนี้"
    except Exception as e:
        st.error("❌ เกิดข้อผิดพลาดระหว่างเรียกใช้งาน OpenRouter")
        st.code(str(e), language="text")
        return "เกิดข้อผิดพลาดขณะรับข้อมูลจาก GPT"

def speak_text(text):
    filename = f"reply_{uuid.uuid4().hex}.mp3"
    try:
        time.sleep(1)  # ป้องกันการโดน 429 Too Many Requests
        tts = gTTS(text=text, lang='th')
        tts.save(filename)
        return filename
    except Exception as e:
        st.warning("⚠️ ไม่สามารถแปลงข้อความเป็นเสียงได้ในตอนนี้")
        st.code(str(e), language="text")
        return None

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
        st.code(str(e))

# ---------- UI ----------
st.set_page_config(page_title="Text-to-Voice Chat", layout="centered")

st.markdown("""
    <style>
        html, body, .stApp {
            font-family: "Cordia New", sans-serif;
            font-size: 22px;
        }
        h1 {
            font-size: 26px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💬 พิมพ์ถาม → 🧠 AI → 🔊 พูดคำตอบ")

if not OPENROUTER_API_KEY:
    st.error("❌ ยังไม่ได้ตั้งค่า API KEY สำหรับ OpenRouter")
else:
    question = st.text_input("พิมพ์คำถามของคุณที่นี่:")

    if st.button("ถามเลย") and question.strip():
        st.info("🤖 กำลังคิดคำตอบ...")
        reply = chat_with_openrouter(question)
        st.markdown(f"**🤖 AI ตอบว่า:** {reply}")

        st.info("🔊 กำลังพูดคำตอบ...")
        audio_file = speak_text(reply)
        if audio_file:
            autoplay_audio(audio_file)
            st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("ไม่มีเสียงสำหรับคำตอบนี้")
