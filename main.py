import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import sounddevice as sd
import wavio
import tempfile
import os

# ==============  BASIC CONFIG  =================
st.set_page_config(page_title="🗣 Text ↔ Voice Converter", page_icon="🎤", layout="centered")

st.title("🎙 Smart Converter: Text ↔ Voice ↔ Text")
st.caption("Convert easily between Text, Voice, and more | English + Hindi support")

# ==============  FUNCTION DEFINITIONS  =================

# 🎤 Record audio
def record_audio(duration=5, fs=16000):
    st.info(f"🎙 Recording for {duration} seconds...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            wavio.write(temp.name, recording, fs, sampwidth=2)
            return temp.name
    except Exception as e:
        st.error(f"⚠ Error during recording: {e}")
        return None

# 🎧 Convert speech → text
def speech_to_text(filename, lang="en-IN"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language=lang)
        return text
    except sr.UnknownValueError:
        return "⚠ Could not understand the audio. Try again!"
    except sr.RequestError:
        return "🌐 Internet connection error. Please retry."

# 🔊 Convert text → speech
def text_to_speech(text, lang="en"):
    try:
        if not text.strip():
            st.warning("⚠ Please enter some text first.")
            return None
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
            tts.save(temp.name)
            return temp.name
    except Exception as e:
        st.error(f"⚠ Text-to-speech failed: {e}")
        return None

# ✏️ Convert text → text (simple transformations)
def text_to_text(text, mode):
    if mode == "UPPERCASE":
        return text.upper()
    elif mode == "lowercase":
        return text.lower()
    elif mode == "Reverse text":
        return text[::-1]
    elif mode == "Capitalize Each Word":
        return text.title()
    else:
        return text

# ==============  APP UI  =================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎤 Voice → Text", 
    "💬 Text → Voice", 
    "🔁 Voice → Voice", 
    "📝 Text → Text"
])

# ==============  TAB 1: VOICE TO TEXT  =================
with tab1:
    st.subheader("🎧 Voice → Text Converter")

    lang_choice = st.radio("Select Language:", ["English", "Hindi"])
    lang_code = "en-IN" if lang_choice == "English" else "hi-IN"

    duration = st.slider("Recording Duration (seconds)", 3, 10, 5)

    if st.button("🎙 Start Recording", key="rec1"):
        file = record_audio(duration)
        if file:
            text = speech_to_text(file, lang=lang_code)
            st.success("🗣 Recognized Text:")
            st.write(text)

# ==============  TAB 2: TEXT TO VOICE  =================
with tab2:
    st.subheader("💬 Text → Voice Converter")

    text_input = st.text_area("📝 Enter text here:")
    lang_choice2 = st.radio("Select Voice Language:", ["English", "Hindi"], key="lang2")
    lang_code2 = "en" if lang_choice2 == "English" else "hi"

    if st.button("🔊 Convert to Voice"):
        audio_file = text_to_speech(text_input, lang=lang_code2)
        if audio_file:
            st.audio(audio_file, format="audio/mp3")
            st.download_button("⬇ Download Audio", open(audio_file, "rb").read(),
                            file_name="converted_voice.mp3", mime="audio/mp3")

# ==============  TAB 3: VOICE TO VOICE  =================
with tab3:
    st.subheader("🔁 Voice → Voice Converter")

    lang_choice3 = st.radio("Select Output Voice Language:", ["English", "Hindi"], key="lang3")
    lang_code3 = "en" if lang_choice3 == "English" else "hi"
    duration2 = st.slider("Recording Duration (seconds)", 3, 10, 5, key="duration2")

    if st.button("🎙 Record & Convert", key="rec2"):
        file = record_audio(duration2)
        if file:
            text = speech_to_text(file, lang="en-IN")
            st.write("🗣 You said:", text)
            if not text.startswith("⚠"):
                audio_out = text_to_speech(text, lang=lang_code3)
                if audio_out:
                    st.audio(audio_out, format="audio/mp3")
                    st.download_button("⬇ Download Voice", open(audio_out, "rb").read(),
                                    file_name="voice_output.mp3", mime="audio/mp3")

# ==============  TAB 4: TEXT TO TEXT  =================
with tab4:
    st.subheader("📝 Text → Text Converter")

    input_text = st.text_area("✍ Enter your text:")
    mode = st.selectbox("Select conversion mode:", 
                        ["UPPERCASE", "lowercase", "Reverse text", "Capitalize Each Word"])

    if st.button("🔁 Convert Text", key="convert_text"):
        if input_text.strip():
            result = text_to_text(input_text, mode)
            st.success("✅ Converted Text:")
            st.code(result)
        else:
            st.warning("⚠ Please enter some text to convert.")

