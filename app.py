import streamlit as st

# Set page configuration
st.set_page_config(page_title="Translation App", layout="wide", page_icon="🌐")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stSelectbox {
        background-color: #f0f0f0;
        border-radius: 5px;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        background-color: #34495E; /* Darker background color */
        color: #FFFFFF; /* White text */
        padding: 20px;
        
    }
    [data-testid="stSidebar"][aria-expanded="true"] .st-emotion-cache-1v0mbdj {
        background-color: #34495E;
        color: #FFFFFF;
    }

    [data-testid="stSidebar"][aria-expanded="true"] .st-emotion-cache-q8sbsg {
        color: #FFFFFF;
        font-size: 18px;
    }

    [data-testid="stSidebar"][aria-expanded="true"] .st-emotion-cache-10pw50 {
        color: #FFFFFF;
    }
    [data-testid="stSidebar"][aria-expanded="true"] .st-emotion-cache-7ym5gk {
        color: #FFFFFF;
    }

    /* Radio Button Styling in Sidebar */
    .st-bd {
        color: #FFFFFF; /* White text for radio button labels */
        font-weight: bold;
    }
    .st-da{
        color: #FFFFFF;
    }
    .st-c2{
        color: #FFFFFF;
    }

    /* Title Styling in Sidebar */
    .sidebar-title {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        border-bottom: 2px solid #FFFFFF; /* Add a line under the title */
        padding-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🌐 Translation App")
st.write("Welcome to your one-stop translation tool! Navigate using the sidebar.")

# Sidebar navigation
st.sidebar.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Live Translation", "Audio File Translation", "Text Translation"])

# Load the selected page
if page == "Live Translation":
    from src.pages.live_translation import live_translation_page
    live_translation_page()
elif page == "Audio File Translation":
    from src.pages.audio_translation import audio_translation_page
    audio_translation_page()
elif page == "Text Translation":
    from src.pages.text_translation import text_translation_page
    text_translation_page()
