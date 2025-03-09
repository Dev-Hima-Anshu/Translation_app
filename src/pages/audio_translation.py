import io
import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile

def audio_translation_page():
    st.title("Audio File Translator 🎧")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload your audio:")
        uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"], help="Supported formats: WAV, MP3")

    with col2:
        st.subheader("Select Languages:")
        lang_options = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "te": "Telugu", "hi": "Hindi"}
        source_lang = st.selectbox("Source Language", list(lang_options.keys()), format_func=lambda x: lang_options[x])
        target_lang = st.selectbox("Target Language", list(lang_options.keys()), format_func=lambda x: lang_options[x])

    if uploaded_file is not None:
        if st.button("Translate"):
            with st.spinner("Translating..."):
                recognizer = sr.Recognizer()
                try:
                    with sr.AudioFile(io.BytesIO(uploaded_file.read())) as source:
                        audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio, language=source_lang)
                    st.success(f"**Original Text:**\n{text}")

                    translator = Translator()
                    translated = translator.translate(text, dest=target_lang)
                    st.success(f"**Translated Text:**\n{translated.text}")

                    tts = gTTS(text=translated.text, lang=target_lang)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        st.audio(fp.name)
                        st.download_button("Download Translated Audio", data=open(fp.name, "rb").read(), file_name="translated_audio.mp3", use_container_width=True)

                except sr.UnknownValueError:
                    st.error("Could not understand audio. Try a clearer file.")
                except sr.RequestError as e:
                    st.error(f"Speech recognition service error: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an audio file.")

