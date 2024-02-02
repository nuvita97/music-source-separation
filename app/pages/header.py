import streamlit as st
from loguru import logger as log
from streamlit_option_menu import option_menu
from pathlib import Path

DEFAULT_PAGE = "Instrument Separation"

def header(logo_and_title=True):
    if logo_and_title:
        head = st.columns([2, 1, 10, 4])
        with head[1]:
            st.image("images/logo.png", use_column_width=False, width=100)
        with head[2]:
            st.markdown(
                """
                <div style="text-align: center;">
                    <h1 style="margin-top: 100x;">Music Source Separation</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Usage in your main script
if __name__ == "__main__":
    st.set_page_config(
        page_title="Action Learning : Music source separation",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    header()