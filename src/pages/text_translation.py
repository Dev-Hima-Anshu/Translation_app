import streamlit as st
from googletrans import Translator
from gtts import gTTS
import tempfile

def text_translation_page():
    st.header("📝 Text Translation")
    st.write("Enter text, translate it, and optionally hear it!")

    # Text input
    text = st.text_area("Enter text to translate", key="translation_text")

    # Language selection
    lang_options = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "te": "Telugu", "hi": "Hindi"}
    target_lang = st.selectbox("Select target language", list(lang_options.keys()), format_func=lambda x: lang_options[x])

    # Initialize session state variables *before* using them
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    if "speech_checkbox" not in st.session_state:
        st.session_state.speech_checkbox = False


    if st.button("Translate Text"):
        if text:
            with st.spinner("Translating..."):
                translator = Translator()
                try:
                    translated = translator.translate(text, dest=target_lang)
                    st.session_state.translated_text = translated.text
                    st.success(f"Translated text: {st.session_state.translated_text}")
                    #reset the checkbox if translation is successful
                    st.session_state.speech_checkbox = False
                except Exception as e:
                    st.error(f"Translation error: {e}")
        else:
            st.warning("Please enter some text.")

    # Conditional speech generation *after* translation and checkbox check
    if st.session_state.translated_text:
        #this section was causing the error.
        #The error was coming from trying to assign to st.session_state.speech_checkbox before it was initialized.
        #Now it checks if it's already in the session state before changing the value.d
        if "speech_checkbox" in st.session_state and st.checkbox("Convert to speech", key="speech_checkbox", value=st.session_state.speech_checkbox):
            st.session_state.speech_checkbox = True
            with st.spinner("Generating speech..."):
                try:
                    tts = gTTS(text=st.session_state.translated_text, lang=target_lang)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                        tts.save(fp.name)
                        st.audio(fp.name)
                        st.download_button("Download Audio", data=open(fp.name, "rb").read(), file_name="translated_text.mp3")
                except Exception as e:
                    st.error(f"An error occurred during speech generation: {e}")

