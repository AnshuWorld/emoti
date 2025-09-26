import streamlit as st
import requests
import tempfile

# Hugging Face free API endpoint (replace with a free TTS model repo id)
TTS_API = "https://api-inference.huggingface.co/models/coqui/XTTS-v1"
TRANS_API = "https://api-inference.huggingface.co/models/facebook/m2m100_418M"
HF_TOKEN = "YOUR_HF_TOKEN"   # free account gives you one

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def translate(text, tgt_lang="hi"):
    payload = {"inputs": text, "parameters": {"src_lang": "en", "tgt_lang": tgt_lang}}
    r = requests.post(TRANS_API, headers=headers, json=payload)
    return r.json()[0]['translation_text']

def tts(text, speaker_sample, emotion="neutral"):
    files = {"inputs": text}
    data = {"options": {"use_cache": True}, "parameters": {"emotion": emotion}}
    # Pass sample audio
    files["audio"] = speaker_sample
    r = requests.post(TTS_API, headers=headers, data=data, files={"audio": speaker_sample})
    return r.content

# --- Streamlit UI ---
st.title("Free AI Voice Cloner 🌍🎙️")

sample = st.file_uploader("Upload a short voice sample", type=["wav", "mp3"])
text = st.text_area("Enter text to speak")
emotion = st.selectbox("Emotion", ["neutral", "happy", "sad", "angry"])
lang = st.selectbox("Language", ["en", "hi", "ml", "fr"])

if st.button("Generate"):
    if sample and text:
        if lang != "en":
            text = translate(text, tgt_lang=lang)
        
        audio_bytes = tts(text, sample, emotion)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(audio_bytes); tmp.close()
        st.audio(tmp.name)
