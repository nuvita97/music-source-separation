import streamlit as st
from karaoke import page_karaoke
from about import page_about
from separation_features import page_upload_and_separation


def main():
    st.set_page_config(
        page_title="Music Source Separation",
        page_icon="images/logo.jpg",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    pages = {
        "Upload and Separation": page_upload_and_separation,
        "Karaoke": page_karaoke,
        "About": page_about,
    }

    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))

    pages[selected_page]()


if __name__ == "__main__":
    main()
