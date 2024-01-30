import streamlit as st
from loguru import logger as log
from header import header

def page_upload_from_url():
    st.markdown("<h1>Upload from URL</h1>", unsafe_allow_html=True)

    url = st.text_input("Paste the URL of the audio file", key="url_input")
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
    if url != "" and st.button("Execute 🎶", type="primary", key="url_button"):
        log.info(f"Processing audio from URL: {url}")
        # Perform processing for the "Upload from URL" page
        st.success("Processing complete!")
