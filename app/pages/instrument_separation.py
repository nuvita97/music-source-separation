import numpy as np
import requests
import streamlit as st
from loguru import logger as log
from pathlib import Path

out_path = Path("/tmp")
in_path = Path("/tmp")


def call_api_by_model(model_choice):
    if model_choice == "Custom U-Net":
        api_url = "http://127.0.0.1:8000/separate"
    elif model_choice == "Open-Unmix":
        api_url = "http://127.0.0.1:8000/separate_sota"
    return api_url


def reset_execution():
    st.session_state.executed = False


def page_instrument_separation():
    st.markdown(
        "<h1 style='text-align: center; color: #0077cc;'>Instrument Separation</h1>",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["mp3", "wav", "ogg", "flac"],
        key="file",
        help="Supported formats: mp3, wav, ogg, flac.",
    )

    selected_instrument = st.selectbox(
        "Select Instrument to Separate:",
        ["Vocals, Drums, Bass & Other", "Vocals 🎤", "Drums 🥁", "Bass 🎸", "Other 🎶"],
        key="instrument",
    )

    selected_model = st.selectbox(
        "Select Separation Model:",
        ["Custom U-Net", "Open-Unmix"],
        key="model",
    )

    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/wav")
        execute = st.button(
            "Separate Music Sources 🎶", type="primary", use_container_width=True
        )

        if "executed" not in st.session_state:
            st.session_state["executed"] = False

        if execute or st.session_state.executed:
            if execute:
                st.session_state.executed = False

            if not st.session_state.executed:
                # Create a placeholder for the processing message
                processing_message = st.empty()
                processing_message.info("Processing uploaded file...")

                # Read the uploaded file
                # file_bytes = uploaded_file.read()

                api_url = call_api_by_model(selected_model)

                # Send the file to the "separate-audio" API
                response = requests.post(api_url, files={"audio_file": uploaded_file})

                # Remove the processing message
                processing_message.empty()

                # Check if the request was successful
                if response.status_code == 200:
                    sample_rate = response.json()["sr"]
                    waveform_path = response.json()["waveform"]

                    waveform_array = np.load(waveform_path).squeeze()
                    # log.info(waveform)

                    # Display the result
                    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
                    st.info(f"Separated by {selected_model} Model")
                    st.audio(waveform_array, sample_rate=sample_rate)

                    st.success("Processing complete!")
                else:
                    st.error("Failed to process the audio. Please try again.")

            st.session_state.executed = True