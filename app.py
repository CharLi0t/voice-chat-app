import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import requests
from gtts import gTTS
import uuid
import os
import glob
import base64

# ---------- CONFIG ----------
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-3.5-turbo"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Voice Chat"
}

@st.cache_resource
def load_model():
    return whisper.load_model("base")

def cleanup_old_audio():
    for file in glob.glob("reply_*.mp3"):
        try:
            os.remove(file)
        except:
            pass

def transcribe(audio_bytes):
    filename = f"audio_{uuid.uuid4().hex}.wav"
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    model = load_model()
    result = model.transcribe(filename, language='th')
    os.remove(filename)
    return result["text"]

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
    cleanup_old_audio()
    tts = gTTS(text=text, lang='th')
    filename = f"reply_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return filename

def autoplay_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            md = f'''
            <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            '''
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ ไม่สามารถเล่นเสียง: {e}")

# ---------- UI ----------
st.set_page_config(page_title="Voice Chat", layout="centered")

st.markdown("""
    <style>
        html, body, .stApp {
            font-family: "Cordia New", sans-serif;
            font-size: 22px;
        }
        h1 { font-size: 42px !important; }
        .title-container p { font-size: 42px !important; }
        .chat-box { font-size: 42px; line-height: 1.6; }
        .stButton > button {
            font-size: 36px !important;
            padding: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-container">
        <h1>🎤 Voice Chat กับ AI</h1>
        <p>พูด → ถอดเสียง → คุยกับ AI → ฟังคำตอบ</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="center-box">', unsafe_allow_html=True)
audio = audio_recorder(text='🟢 กดเพื่อพูด', icon_size="4x")
st.markdown('</div>', unsafe_allow_html=True)

if audio:
    st.info("🔁 ถอดเสียงพูด...")
    text = transcribe(audio)
    st.markdown(f'<div class="chat-box user-box">🧑‍💬 <strong>คุณ:</strong> {text}</div>', unsafe_allow_html=True)

    st.info("🤖 AI กำลังตอบ...")
    reply = chat_with_openrouter(text)
    st.markdown(f'<div class="chat-box">🤖 <strong>AI:</strong> {reply}</div>', unsafe_allow_html=True)

    st.info("🔊 กำลังพูดคำตอบ...")
    reply_file = speak_text(reply)
    autoplay_audio(reply_file)
    st.audio(reply_file, format="audio/mp3")
