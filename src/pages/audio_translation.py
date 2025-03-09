import io
import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
import wave

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
                    # Check if it's a WAV file (basic check)
                    audio_bytes = uploaded_file.read()
                    try:
                        with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
                            num_channels = wf.getnchannels()
                            frame_rate = wf.getframerate()
                            sample_width = wf.getsampwidth()
                            num_frames = wf.getnframes()

                            #Further validation if needed
                            if num_channels != 1:
                                st.error("Only mono WAV files (1 channel) are supported.")
                                return

                    except wave.Error as e:
                        st.error(f"Invalid WAV file: {e}")
                        return #Exit if not a valid WAV file



                    try:
                        data, fs = wavfile.read(io.BytesIO(audio_bytes))
                        if not isinstance(data, np.ndarray):
                            st.error("Error: Uploaded audio file is not a valid WAV file (data type check failed).")
                            return

                        with io.BytesIO() as buffer:
                            wavfile.write(buffer, fs, data)
                            audio_bytes = buffer.getvalue()

                        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                            audio = recognizer.record(source)
                            # ... (rest of your speech recognition and translation code) ...

                    except Exception as e:
                        st.error(f"Error reading/processing WAV file: {e}")
                        return

                except sr.UnknownValueError:
                    st.error("Could not understand audio. Try a clearer file.")
                except sr.RequestError as e:
                    st.error(f"Speech recognition service error: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload an audio file.")
