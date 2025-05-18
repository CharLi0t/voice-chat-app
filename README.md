# 🧠 Thai Voice Chat AI — Feature Summary & Future Development

This project is a web app that lets you **type a question → get a response from GPT → convert it to Thai speech**, built with Streamlit and GPT-3.5 via the OpenRouter API.

---

## ✅ Current Features

- 💬 Type questions in Thai
- 🔗 Connects to GPT-3.5 via [OpenRouter.ai](https://openrouter.ai)
- 🧠 Receives intelligent answers from the AI
- 🔊 Converts responses to Thai audio using [gTTS](https://pypi.org/project/gTTS/)
- ▶️ Automatically plays the response in the browser
- 🔐 Uses API Key securely through Environment Variables
- ☁️ Deployable on Render (Free Tier)

---

## 🛠️ Ideas for Further Development

### 🔄 Improve User Experience
- Add chat history logging
- Add a "Repeat" button to replay the answer

### 🗣️ Add Voice Input
- Use `audio_recorder_streamlit` to record from mic
- Transcribe audio using [Whisper](https://github.com/openai/whisper) or `faster-whisper` (requires more memory)

### 🧏‍♀️ Upgrade Text-to-Speech
- Switch to `edge-tts` (Microsoft TTS) for better quality and fewer rate limits
- Support multi-language and different voices

### 💾 Implement Audio Caching
- Avoid regenerating audio for identical responses
- Speed up response time and reduce API load

### 🌐 Support More AI Models
- Let users choose GPT-4, Claude, or other models via OpenRouter

### 🎨 UI Enhancements
- Support light/dark themes
- Make UI more mobile-friendly

---

## 📦 Tech Stack

| Technology | Purpose |
|------------|---------|
| Streamlit  | Build the web UI |
| gTTS       | Convert text to Thai speech |
| OpenRouter | Connect to GPT API |
| Python 3.9+| Core programming language |

---

## 🙏 Credits

- [OpenRouter.ai](https://openrouter.ai)
- [Google Text-to-Speech (gTTS)](https://pypi.org/project/gTTS/)
- [Streamlit](https://streamlit.io)

---

## 🪄 License

MIT © 2025 by You 😄

---

## 🚀 Try it Live

🧪 You can try the deployed app here:

👉 [https://voice-chat-app-1nze.onrender.com](https://voice-chat-app-1nze.onrender.com)

> Note: First-time load may take ~30s due to Render free tier cold start.
