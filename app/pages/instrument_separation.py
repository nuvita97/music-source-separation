import streamlit as st
from loguru import logger as log
from pathlib import Path

out_path = Path("/tmp")
in_path = Path("/tmp")

def reset_execution():
    st.session_state.executed = False

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
        ["Vocals, Drums, Bass & Other", "Vocals 🎤", "Drums 🥁", "Bass 🎸", "Other 🎶"],
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
