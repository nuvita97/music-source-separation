import os
import numpy as np
import requests
import streamlit as st
import yt_dlp
from pytube import YouTube
from pathlib import Path
from moviepy.editor import VideoFileClip


# in_path = Path("audio/input/")
in_path = Path(
    "/Users/nguyenvietthai/Library/CloudStorage/OneDrive-EPITA/S3. Action Learning/music-source-separation/audio/input"
)
in_path.mkdir(parents=True, exist_ok=True)


# function to download audio of youtube video from url
def download_audio(yt_url, output_folder):
    # check if output folder exist, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
    }  # these are like our predefined parameters
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])


# if anyother download link is given, if it is mp3 we download it too
def download_file(url, output_folder):
    # Import the requests library
    import requests

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


def page_get_url_content():
    video_url = st.text_input("Enter the YouTube video URL", key="youtube_url_input")
    # extract_button = st.button("Find Audio", type="primary")
    # if extract_button:
    if video_url:
        # youtube = YouTube(video_url)
        # audio_stream = youtube.streams.get_audio_only()
        # audio_file_path = audio_stream.download()
        # audio_check = st.audio(audio_file_path, format="audio/wav")
        # st.write(type(audio_stream))

        youtube = YouTube(video_url)
        video = youtube.streams.first()
        downloaded_file = video.download()
        # st.video(downloaded_file, format="mp4")
        video_clip = VideoFileClip(downloaded_file)
        audio_clip = video_clip.audio
        audio_file_path = in_path / "youtube_audio.mp3"
        audio_clip.write_audiofile(str(audio_file_path))

        st.write(audio_file_path)

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

    if video_url:
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
                # processing_message = st.empty()
                # processing_message.info("Processing uploaded file...")

                api_url = call_api_by_model(selected_model)

                # test_path = "data/Triviul_Dorothy_mixture.wav"
                absolute_test_path = os.path.abspath(audio_file_path)
                # st.write(absolute_test_path)

                response = requests.post(
                    url=api_url, json={"file_path": absolute_test_path}
                )
                if response.status_code == 200:
                    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
                    st.info(f"Separated by {selected_model} Model")

                    display_selected_instruments(selected_instruments, response)

                    # processing_message.empty()
                    st.success("Processing complete!")
                else:
                    st.error("Failed to process the audio. Please try again.")

            st.session_state.executed = True
    # youtube_url = st.text_input("Enter the YouTube video URL: ")
    # other_url = st.text_input("Enter the other video or audio download link: ")

    # if st.button("Get Audio"):
    #     if youtube_url:
    #         download_audio(youtube_url, "youtube_extractions")
    #         st.success("YouTube audio downloaded successfully")
    #     elif other_url:
    #         message = download_file(other_url, "other_source_extraction")
    #         st.success(message)
    #     else:
    #         st.error("Please enter a URL")


def call_api_by_model(model_choice):
    if model_choice == "Custom U-Net":
        api_url = "http://localhost:8000/separate_unet"
    elif model_choice == "Open-Unmix":
        api_url = "http://localhost:8000/separate_sota"
    return api_url


def display_selected_instruments(selected_instruments, response):
    sample_rate = response.json()["sr"]
    for stem in selected_instruments:
        stem_path = response.json()[stem]
        stem_array = np.load(stem_path).squeeze()
        st.text(stem)
        st.audio(stem_array, sample_rate=sample_rate)


page_get_url_content()
