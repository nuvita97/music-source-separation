import streamlit as st
from loguru import logger as log
from pathlib import Path
from header import header

out_path = Path("/tmp")
in_path = Path("/tmp")

def reset_execution():
    st.session_state.executed = False

# Page 1: Instrument Separation
def page_instrument_separation():
    st.markdown(
        "<h1 style='text-align: center; color: #0077cc;'>Instrument Separation</h1>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["mp3", "wav", "ogg", "flac"],
        key="file",
        help="Supported formats: mp3, wav, ogg, flac.",
    )

    selected_instrument = st.selectbox(
        "Select Instrument to Separate:",
        ["Vocals 🎤", "Drums 🥁", "Bass 🎸", "Other 🎶"],
        key="instrument",
    )

    selected_model = st.selectbox(
        "Select Separation Model:",
        ["Custom Model", "OpenUnmix Model"],
        key="model",
    )

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        execute = st.button("Separate Music Sources 🎶", type="primary", use_container_width=True)

        if execute or st.session_state.executed:
            if execute:
                st.session_state.executed = False

            if not st.session_state.executed:
                log.info("Processing uploaded file...")
                # Perform your processing here (e.g., model separation, etc.)
                # You can access the uploaded file using `uploaded_file` object
                # Access selected instrument and model using `selected_instrument` and `selected_model`

                st.success("Processing complete!")

                # Display the result here
                st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
                # Add your result display code here

            st.session_state.executed = True

def page_upload_from_url():
    st.markdown("<h1>Upload from URL</h1>", unsafe_allow_html=True)

    url = st.text_input("Paste the URL of the audio file", key="url_input")
    selected_instrument = st.selectbox(
        "Select Instrument to Separate:",
        ["Vocals 🎤", "Drums 🥁", "Bass 🎸", "Other 🎶"],
        key="instrument",
    )

    selected_model = st.selectbox(
        "Select Separation Model:",
        ["Custom Model", "OpenUnmix Model"],
        key="model",
    )
    if url != "" and st.button("Execute 🎶", type="primary", key="url_button"):
        log.info(f"Processing audio from URL: {url}")
        # Perform processing for the "Upload from URL" page
        st.success("Processing complete!")

# Page 3: Karaoke
def page_karaoke():
    st.markdown("<h1>Karaoke</h1>", unsafe_allow_html=True)
    # Add content for the "Karaoke" page

def main():
    st.set_page_config(
        page_title="Music Source Separation",
        page_icon="images/logo.jpg",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    pages = {
        "Instrument Separation": page_instrument_separation,
        "Upload from URL": page_upload_from_url,
        "Karaoke": page_karaoke,
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    header()  # Call the header function

    pages[selected_page]()

if __name__ == "__main__":
    main()