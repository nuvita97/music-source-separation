import requests
import tempfile
import io
import base64
import numpy as np
import streamlit as st
from loguru import logger as log
from pathlib import Path
from header import header

# from helpers import delete_old_files

out_path = Path("/tmp")
in_path = Path("/tmp")

API_URL = "http://127.0.0.1:8000/separate/"


def reset_execution():
    st.session_state.executed = False


# Page 1: Instrument Separation
def page_instrument_separation():
    st.markdown(
        "<h1 style='text-align: center; color: #0077cc;'>Instrument Separation</h1>",
        unsafe_allow_html=True,
    )

    waveform = np.load("api/waveform.npy")
    # log.info(waveform)
    st.audio(waveform, sample_rate=44100)

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
        st.audio(uploaded_file, format="audio/wav")

        # Temporary file path
        # with open(in_path / uploaded_file.name, "wb") as f:
        #     f.write(uploaded_file.getbuffer())
        # filename = uploaded_file.name

        # st.write(f"File path: {filename}")

        execute = st.button(
            "Separate Music Sources 🎶", type="primary", use_container_width=True
        )

        if "executed" not in st.session_state:
            st.session_state["executed"] = False

        if execute or st.session_state.executed:
            if execute:
                st.session_state.executed = False

            if not st.session_state.executed:
                log.info("Processing uploaded file...")

                # Read the uploaded file
                # file_bytes = uploaded_file.read()

                # Send the file to the "separate-audio" API
                response = requests.post(API_URL, files={"audio_file": uploaded_file})

                # Check if the request was successful
                if response.status_code == 200:
                    sample_rate = response.json()["sr"]
                    waveform_path = response.json()["waveform"]

                    waveform_array = np.load(waveform_path)
                    # log.info(waveform)
                    st.audio(waveform_array, sample_rate=sample_rate)

                    # Display the audio
                    # st.audio(waveform, sample_rate=sample_rate)
                    # Access selected instrument and model using `selected_instrument` and `selected_model`

                    st.success("Processing complete!")
                else:
                    st.error("Failed to process the audio. Please try again.")

                st.write(response)
                st.write(response.text)

                # Display the result here
                st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
                # Add your result display code here

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
