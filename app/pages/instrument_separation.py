import numpy as np
import requests
import streamlit as st
import matplotlib.pyplot as plt
import librosa.display
from loguru import logger as log
from pathlib import Path
from pytube import YouTube


out_path = Path("/tmp")
in_path = Path("/tmp")


def call_api_by_model(model_choice):
    if model_choice == "Custom U-Net":
        api_url = "http://127.0.0.1:8000/separate_path"
    elif model_choice == "Open-Unmix":
        api_url = "http://127.0.0.1:8000/separate_sota_path"
    return api_url


def display_selected_instruments(selected_instruments, response):
    sample_rate = response.json()["sr"]
    for stem in selected_instruments:
        stem_path = response.json()[stem]
        stem_array = np.load(stem_path).squeeze()
        st.text(stem)
        st.audio(stem_array, sample_rate=sample_rate)


def reset_execution():
    st.session_state.executed = False


def plot_wave(y, sr):
    fig, ax = plt.subplots()
    img = librosa.display.waveshow(y, sr=sr, x_axis="time", ax=ax)
    return plt.gcf()


def show_results(model_name: str, dir_name_output: str, file_sources: list):
    sources = get_sources(out_path / Path(model_name) / dir_name_output, file_sources)
    tab_sources = st.tabs([f"**{label_sources.get(k)}**" for k in sources.keys()])
    for i, (file, pathname) in enumerate(sources.items()):
        with tab_sources[i]:
            cols = st.columns(2)
            with cols[0]:
                auseg = load_audio_segment(pathname, "mp3")
                st.image(
                    plot_audio(
                        auseg,
                        32767,
                        file=file,
                        model_name=model_name,
                        dir_name_output=dir_name_output,
                    ),
                    use_column_width="always",
                )
            with cols[1]:
                st.audio(str(pathname))
    log.info(f"Displaying results for {dir_name_output} - {model_name}")


def page_instrument_separation():
    st.markdown(
        "<h1 style='text-align: center; color: #0077cc;'>Instrument Separation</h1>",
        unsafe_allow_html=True,
    )
    tab1, tab2 = st.tabs(["Upload audio", "Get YouTube link"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["mp3", "wav", "ogg", "flac"],
            key="file",
            help="Supported formats: mp3, wav, ogg, flac.",
        )
        if uploaded_file:
            st.audio(uploaded_file, format="audio/wav")
            st.write(type(uploaded_file))

    with tab2:
        video_url = st.text_input(
            "Enter the YouTube video URL", key="youtube_url_input"
        )
        extract_button = st.button("Find Audio", type="primary")
        if extract_button:
            youtube = YouTube(video_url)
            audio_stream = youtube.streams.get_audio_only()
            audio_file_path = audio_stream.download()
            st.audio(audio_file_path, format="audio/wav")

    checkboxes = {
        "vocals": st.checkbox("Vocals 🎤", key="vocals"),
        "drums": st.checkbox("Drums 🥁", key="drums"),
        "bass": st.checkbox("Bass 🎸", key="bass"),
        "other": st.checkbox("Other 🎶", key="other"),
    }

    selected_instruments = [
        instrument for instrument, checked in checkboxes.items() if checked
    ]

    selected_model = st.selectbox(
        "Select Separation Model:",
        ["Custom U-Net", "Open-Unmix"],
        key="model",
    )

    if uploaded_file is not None or extract_button:
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
                api_url = call_api_by_model(selected_model)
                response = requests.post(api_url, files={"audio_file": uploaded_file})
                processing_message.empty()

                if response.status_code == 200:
                    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
                    st.info(f"Separated by {selected_model} Model")

                    display_selected_instruments(selected_instruments, response)

                    # show_results(
                    #     selected_model,
                    #     response.json()["dir_name_output"],
                    #     selected_instruments,
                    # )

                    # show_waveform = st.checkbox("Show Waveform")
                    # if show_waveform:
                    #     for stem in selected_instruments:
                    #         stem_path = response.json()[stem]
                    #         stem_array = np.load(stem_path).squeeze()
                    #         st.text(stem)
                    #         st.audio(stem_array, sample_rate=response.json()["sr"])
                    #         plot_wave(stem_array, response.json()["sr"])

                    st.success("Processing complete!")
                else:
                    st.error("Failed to process the audio. Please try again.")

            st.session_state.executed = True


page_instrument_separation()
