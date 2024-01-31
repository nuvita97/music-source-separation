import streamlit as st
from loguru import logger as log
from streamlit_option_menu import option_menu
from pathlib import Path

DEFAULT_PAGE = "Instrument Separation"

def header(logo_and_title=True):


    if logo_and_title:
        head = st.columns([2, 1, 5, 5])
        with head[1]:
            st.image("images/logo.jpg", use_column_width=False, width=70)
        with head[2]:
            st.markdown(
                "<h1>Music Source Separation</h1><p><b></b></p>",
                unsafe_allow_html=True,
            )

# Usage in your main script

