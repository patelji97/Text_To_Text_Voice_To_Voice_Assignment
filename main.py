import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# =============================
# 🎛 APP CONFIGURATION
# =============================
st.set_page_config(page_title="Text ↔ Voice ↔ Text Converter", page_icon="🎤", layout="centered")
st.title("🎙 Text ↔ Voice ↔ Text Converter (Cloud Ready)")
st.caption("Convert between text, voice, and language | Fully Cloud Compatible 🚀")

# =============================
# 🎧 FUNCTIONS
# =============================

# Speech → Text
def speech_to_text(uploaded_file, lang="en-IN"):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    with sr.AudioFile(temp_path) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language=lang)
        return text
    except sr.UnknownValueError:
        return "⚠ Could not understand the audio."
    except sr.RequestError:
        return "🌐 Network error, please check your internet connection."

# Text → Speech
def text_to_speech(text, lang="en"):
    if not text.strip():
        st.warning("Please enter some text first!")
        return None
    tts = gTTS(text=text, lang=lang, slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        tts.save(temp.name)
        return temp.name

# Text → Text (Translation)
def text_to_text(text, target_lang):
    if not text.strip():
        return "⚠ Please enter some text first!"
    translator = Translator()
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return f"❌ Translation failed: {str(e)}"

# =============================
# 🎛 UI DESIGN
# =============================

tab1, tab2, tab3, tab4 = st.tabs([
    "🎧 Voice → Text", 
    "💬 Text → Voice", 
    "🔁 Voice → Voice", 
    "📝 Text ↔ Text"
])

# 🎤 Voice → Text
with tab1:
    st.header("🎧 Voice → Text Converter")
    lang = st.radio("Select Language:", ["English", "Hindi"])
    lang_code = "en-IN" if lang == "English" else "hi-IN"
    uploaded = st.file_uploader("🎵 Upload your voice file (WAV/MP3):", type=["wav", "mp3"])

    if uploaded and st.button("Convert to Text"):
        text = speech_to_text(uploaded, lang=lang_code)
        st.success("Recognized Text:")
        st.write(text)

# 💬 Text → Voice
with tab2:
    st.header("💬 Text → Voice Converter")
    text_input = st.text_area("Enter your text here:")
    lang2 = st.radio("Select Voice Language:", ["English", "Hindi"], key="t2vlang")
    lang_code2 = "en" if lang2 == "English" else "hi"

    if st.button("Convert to Voice"):
        audio_file = text_to_speech(text_input, lang=lang_code2)
        if audio_file:
            st.audio(audio_file, format="audio/mp3")
            st.download_button("⬇ Download Audio", open(audio_file, "rb").read(),
                            file_name="converted_voice.mp3", mime="audio/mp3")

# 🔁 Voice → Voice
with tab3:
    st.header("🔁 Voice → Voice Converter")
    lang3 = st.radio("Select Output Voice Language:", ["English", "Hindi"], key="v2vlang")
    lang_code3 = "en" if lang3 == "English" else "hi"
    uploaded2 = st.file_uploader("🎙 Upload your voice file (WAV/MP3):", type=["wav", "mp3"], key="v2vupload")

    if uploaded2 and st.button("Convert Voice"):
        text = speech_to_text(uploaded2)
        st.write("Recognized Text:", text)
        if not text.startswith("⚠"):
            audio_out = text_to_speech(text, lang=lang_code3)
            if audio_out:
                st.audio(audio_out, format="audio/mp3")
                st.download_button("⬇ Download Converted Voice", open(audio_out, "rb").read(),
                                file_name="voice_output.mp3", mime="audio/mp3")

# 📝 Text ↔ Text
with tab4:
    st.header("📝 Text ↔ Text Converter")
    text_input2 = st.text_area("Enter your text to translate:")
    lang4 = st.radio("Select Output Language:", ["English", "Hindi"], key="t2tlang")

    if st.button("Convert Text"):
        lang_code4 = "en" if lang4 == "English" else "hi"
        translated_text = text_to_text(text_input2, lang_code4)
        st.success("✅ Translated Text:")
        st.write(translated_text)

        st.download_button(
            label="⬇ Download Translated Text",
            data=translated_text,
            file_name="translated_text.txt",
            mime="text/plain"
        )






