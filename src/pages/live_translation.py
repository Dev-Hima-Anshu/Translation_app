import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
import time

def live_translation_page():
    st.header("🎙️ Live Translation")
    st.write("Speak into your microphone and get instant translation!")

    # Language selection with improved styling
    lang_options = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "te": "Telugu", "hi": "Hindi"}
    col1, col2 = st.columns(2)  # Create two columns for better layout

    with col1:
        st.markdown("<style>.stSelectbox {background-color: #f0f0f0; border-radius: 5px; padding: 10px;}</style>", unsafe_allow_html=True)
        source_lang = st.selectbox("Select source language", list(lang_options.keys()), format_func=lambda x: lang_options[x])

    with col2:
        st.markdown("<style>.stSelectbox {background-color: #f0f0f0; border-radius: 5px; padding: 10px;}</style>", unsafe_allow_html=True)
        target_lang = st.selectbox("Select target language", list(lang_options.keys()), format_func=lambda x: lang_options[x])


    if st.button("Start Recording"):
        with st.spinner("Listening..."):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                try:
                    # The crucial change: Explicitly set a longer timeout (in seconds)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5) # Adjust timeout as needed

                    text = recognizer.recognize_google(audio, language=source_lang)
                    st.success(f"You said: {text}")

                    translator = Translator()
                    translated = translator.translate(text, dest=target_lang)
                    st.success(f"Translated: {translated.text}")

                    # Generate and play translated audio
                    tts = gTTS(text=translated.text, lang=target_lang)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        st.audio(fp.name)
                        st.download_button("Download Translated Audio", data=open(fp.name, "rb").read(), file_name="translated_audio.mp3")

                except sr.UnknownValueError:
                    st.error("Sorry, I couldn’t understand the audio. Please try again.")
                except sr.RequestError as e:
                    st.error(f"Speech recognition service is unavailable: {e}")
                except sr.WaitTimeoutError:
                    st.info("No speech detected within the timeout period. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

