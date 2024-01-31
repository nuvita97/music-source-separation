import numpy as np
import requests
import streamlit as st
import matplotlib.pyplot as plt
import librosa.display
from loguru import logger as log
from pathlib import Path
from typing import List
from moviepy.editor import VideoFileClip
from pytube import Search, YouTube
import os
import yt_dlp
import logging


out_path = Path("/tmp")  # instrument_separation_in
in_path = Path("/tmp")  # instrument_separation_out


logger = logging.getLogger("pytube")
logger.setLevel(logging.ERROR)


@st.cache_data(show_spinner=False, max_entries=10)
def query_youtube(query: str) -> Search:
    return Search(query)


def search_youtube(query: str, limit=5) -> List:
    log.info(f"{query}")

    # Initialize search_results if not present in session_state
    if (
        "search_results" not in st.session_state
        or st.session_state.search_results is None
    ):
        st.session_state.search_results = []

    if len(query) > 3:
        search = query_youtube(query + " lyrics")
        st.session_state.search_results = search.results[:limit]

    # Extract video titles if search_results is not empty
    video_options = (
        [video.title for video in st.session_state.search_results]
        if st.session_state.search_results
        else []
    )

    st.session_state.video_options = video_options
    return video_options


def get_youtube_url(title: str) -> str:
    video = st.session_state.search_results[st.session_state.video_options.index(title)]
    return video.embed_url


def check_if_is_youtube_url(url: str) -> bool:
    return url.startswith("http")


def download_audio(yt_url, output_folder):
    # check if output folder exist, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info_dict = ydl.extract_info(yt_url, download=False)
    if info_dict.get("duration", 0) > 360:
        st.error("Song is too long. Please use a song no longer than 6 minutes.")
        return
    video_title = info_dict.get("title", None)
    video_title = os.path.join(output_folder, "audio")  # SAME NAME FOR ALL
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": video_title,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
    return f"{video_title}.mp3"


def get_audio_from_youtube(video_url):
    youtube = YouTube(video_url)
    video = youtube.streams.first()
    downloaded_file = video.download()
    # st.video(downloaded_file, format="mp4")
    video_clip = VideoFileClip(downloaded_file)
    audio_clip = video_clip.audio
    audio_file_path = in_path / "youtube_audio.mp3"
    audio_clip.write_audiofile(str(audio_file_path))
    return audio_file_path


# if anyother download link is given, if it is mp3 we download it too
def download_file(url, output_folder):
    # Import the requests library
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # The last element after splitting the URL by '/' is the file name
        file_name = url.split("/")[-1]
        # Open the file in write-binary mode ('wb')
        # os.path.join creates a new path for the file in the output folder
        with open(os.path.join(output_folder, file_name), "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        return "File downloaded successfully"
    except Exception as e:
        return f"An error occurred: {e}"


def call_api_by_model(model_choice):
    if model_choice == "Custom U-Net":
        api_url = "http://127.0.0.1:8000/separate_unet"
    elif model_choice == "Open-Unmix":
        api_url = "http://127.0.0.1:8000/separate_sota"
    return api_url


def api_call_and_display(audio_file_path, selected_model, selected_instruments):
    api_url = call_api_by_model(selected_model)
    absolute_path = os.path.abspath(audio_file_path)
    response = requests.post(url=api_url, json={"file_path": absolute_path})
    if response.status_code == 200:
        st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
        st.info(f"Separated by {selected_model} Model")
        display_selected_instruments(selected_instruments, response)
        st.success("Processing complete!")
    else:
        st.error("Failed to process the audio. Please try again.")


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


def download_uploaded_file(uploaded_file, output_folder):
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_path = os.path.join(output_folder, "audio.mp3")  # SAME NAME ALL FILE
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def page_upload_and_separation():
    st.markdown("<h1>Upload and Separation</h1>", unsafe_allow_html=True)

    option_menu = st.selectbox(
        "Select Source:",
        ["Paste URL", "Search on YouTube", "Upload Audio File"],
        key="source_option",
    )

    if option_menu == "Paste URL" or option_menu == "Search on YouTube":
        # PASTE URL
        if option_menu == "Paste URL":
            st.markdown("<h2>Upload from URL</h2>", unsafe_allow_html=True)
            source_url = st.text_input("Enter the URL:", key="source_url")
            # Options
            st.markdown("<h2>Select Instruments and Model</h2>", unsafe_allow_html=True)
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
                ["Open-Unmix", "Custom U-Net"],
                key="model",
            )
            # Separation
            if st.button(
                "Separate Music Sources 🎶", type="primary", use_container_width=True
            ):
                if source_url:
                    audio_file_path = download_audio(
                        source_url, "audio/youtube"  # change the output directory
                    )
                    st.write("Orginal Audio")
                    st.audio(audio_file_path, format="audio/wav")
                else:
                    st.error("Please enter a valid URL")
                # API Call
                api_call_and_display(
                    audio_file_path, selected_model, selected_instruments
                )

        # YOUTUBE SEARCH
        elif option_menu == "Search on YouTube":
            st.markdown("<h2>Search on Youtube</h2>", unsafe_allow_html=True)
            search_query = st.text_input(
                "Search on YouTube:",
                value="What do you want to separate",
                key="youtube_search_input",
            )
            video_options = search_youtube(search_query)
            selected_video = st.selectbox(
                "Select a video", video_options, key="youtube_video_selection"
            )
            source_url = get_youtube_url(selected_video)
            # Options
            st.markdown("<h2>Select Instruments and Model</h2>", unsafe_allow_html=True)
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
                ["Open-Unmix", "Custom U-Net"],
                key="model",
            )
            # Separation
            if st.button(
                "Separate Music Sources 🎶", type="primary", use_container_width=True
            ):
                if source_url:
                    audio_file_path = download_audio(
                        source_url, "audio/youtube"  # change the output directory
                    )
                    st.write("Orginal Audio")
                    st.audio(audio_file_path, format="audio/wav")
                else:
                    st.error("Please select a valid song")
                # API Call
                api_call_and_display(
                    audio_file_path, selected_model, selected_instruments
                )

    # UPLOAD FILE
    elif option_menu == "Upload Audio File":
        st.markdown("<h2>Upload Audio File</h2>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["mp3", "wav", "ogg", "flac"],
            key="file",
            help="Supported formats: mp3, wav, ogg, flac.",
        )
        # Options
        st.markdown("<h2>Select Instruments and Model</h2>", unsafe_allow_html=True)
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
            ["Open-Unmix", "Custom U-Net"],
            key="model",
        )
        # Separation
        if uploaded_file is not None:
            st.audio(uploaded_file, format="audio/wav")
            audio_file_path = download_uploaded_file(uploaded_file, "audio/upload")

            execute = st.button(
                "Separate Music Sources 🎶", type="primary", use_container_width=True
            )
            if "executed" not in st.session_state:
                st.session_state["executed"] = False
            if execute or st.session_state.executed:
                if execute:
                    st.session_state.executed = False

                if not st.session_state.executed:
                    api_call_and_display(
                        audio_file_path, selected_model, selected_instruments
                    )
