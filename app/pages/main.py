import streamlit as st
from header import header
from instrument_separation import page_instrument_separation
from upload_from_url import page_upload_from_url
from get_url_content import page_get_url_content
from karaoke import page_karaoke
from about import page_about


def main():
    st.set_page_config(
        page_title="Music Source Separation",
        page_icon="images/logo.jpg",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    pages = {
        "Instrument Separation": page_instrument_separation,
        # "Upload from URL": page_upload_from_url,
        "Upload from URL": page_get_url_content,
        "Karaoke": page_karaoke,
        "About": page_about,
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    header()  # Call the header function

    pages[selected_page]()


if __name__ == "__main__":
    main()
