import streamlit as st
from loguru import logger as log
from pathlib import Path
from helpers import delete_old_files

out_path = Path("/tmp")
in_path = Path("/tmp")

def reset_execution():
    st.session_state.executed = False

def body():
    st.markdown("<h4><center>Music source separation </center></h4>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["mp3", "wav", "ogg", "flac"],
        key="file",
        help="Supported formats: mp3, wav, ogg, flac.",
    )

    if uploaded_file is not None:
        st.audio(uploaded_file)
        execute = st.button("Separate Music Sources", type="primary", use_container_width=True)

        if execute or st.session_state.executed:
            if execute:
                st.session_state.executed = False

            if not st.session_state.executed:
                log.info("Processing uploaded file...")
                # Perform your processing here (e.g., model separation, etc.)
                # You can access the uploaded file using `uploaded_file` object

                st.success("Processing complete!")

            st.session_state.executed = True

if __name__ == "__main__":
    body()
