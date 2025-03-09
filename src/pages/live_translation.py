import io
import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile
import sounddevice as sd
import numpy as np
from scipy.io import wavfile #Import wavfile

def live_translation_page():
    st.header("🎙️ Live Translation")
    st.write("Speak into your microphone and get instant translation!")

    # Language selection 
    lang_options = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "te": "Telugu", "hi": "Hindi"}
    col1, col2 = st.columns(2)

    with col1:
        source_lang = st.selectbox("Source Language", list(lang_options.keys()), format_func=lambda x: lang_options[x])
    with col2:
        target_lang = st.selectbox("Target Language", list(lang_options.keys()), format_func=lambda x: lang_options[x])


    if st.button("Start Recording"):
        with st.spinner("Listening..."):
            recognizer = sr.Recognizer() # define recognizer here
            try:
                fs = 44100
                duration = 5
                recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
                sd.wait()

                with io.BytesIO() as buffer:
                    wavfile.write(buffer, fs, recording)
                    audio_bytes = buffer.getvalue()

                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio, language=source_lang)
                    st.success(f"You said: {text}")

                    translator = Translator()
                    translated = translator.translate(text, dest=target_lang)
                    st.success(f"Translated: {translated.text}")

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

