import requests
import tempfile
import io
import base64
import numpy as np
import streamlit as st
from loguru import logger as log
from pathlib import Path

# from helpers import delete_old_files

out_path = Path("/tmp")
in_path = Path("/tmp")

API_URL = "http://127.0.0.1:8000/separate/"


def reset_execution():
    st.session_state.executed = False


def body():
    st.markdown(
        "<h4><center>Music source separation </center></h4>", unsafe_allow_html=True
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

    if uploaded_file is not None:
        st.audio(uploaded_file)

        # Temporary file path
        # with open(in_path / uploaded_file.name, "wb") as f:
        #     f.write(uploaded_file.getbuffer())
        # filename = uploaded_file.name

        # st.write(f"File path: {filename}")

        execute = st.button(
            "Separate Music Sources", type="primary", use_container_width=True
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

                    st.success("Processing complete!")
                else:
                    st.error("Failed to process the audio. Please try again.")

                st.write(response)
                st.write(response.text)

            st.session_state.executed = True


if __name__ == "__main__":
    body()
