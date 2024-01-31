import base64
import os
import numpy as np
import requests
import streamlit as st
from pathlib import Path
import whisper
import lyricsgenius as genius
from http.client import IncompleteRead
from separation_features import download_audio
import time
import soundfile as sf
from scipy.io.wavfile import write


# Set up Genius API
api = genius.Genius("v_CyxiEGCu4AlDye7BXWPP4X8a5wij5AjfR2thvUnoMPQJAbmga7SLY8ReD8c5D4")

# Define the base directory
base_path = Path("audio")
# Define the input directory
in_path_1 = base_path / "upload"
in_path_1.mkdir(parents=True, exist_ok=True)
in_path_2 = base_path / "youtube"
in_path_2.mkdir(parents=True, exist_ok=True)
in_path_3 = base_path / "extract"
in_path_3.mkdir(parents=True, exist_ok=True)


# Function to download YouTube video, extract audio, and transcribe
def download_extract_transcribe_youtube(video_url):
    audio_file_path = download_audio(
        video_url, "audio/youtube"  # change the output directory
    )
    # Perform transcription using Whisper
    transcribe_audio(audio_file_path)
    # Extract audio
    extract_vocal(audio_file_path)


def save_uploaded_audio(uploaded_audio):
    # Save the uploaded audio file to a temporary location
    temp_path = in_path_1 / "audio.mp3"
    with temp_path.open("wb") as audio_file:
        audio_file.write(uploaded_audio.read())
    return str(temp_path)


def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False, verbose=True)
    lyrics = ""
    for sentence in result["segments"]:
        lyrics += f"{sentence['start']} - {sentence['end']}: {sentence['text']}  \n"
    st.info("Transcription Result")
    st.write(lyrics)


def display_vocal_extract(response):
    sample_rate = response.json()["sr"]
    residual_path = response.json()["residual"]
    residual_array = np.load(residual_path).squeeze()
    # Define the output file path and save file
    # output_file_path = in_path_3 / "audio.wav"
    # write(output_file_path, sample_rate, residual_array)
    st.audio(residual_array, sample_rate=sample_rate)
    # return output_file_path


def extract_vocal(uploaded_audio_path):
    api_url = "http://127.0.0.1:8000/separate_karaoke"
    absolute_test_path = os.path.abspath(uploaded_audio_path)
    response = requests.post(url=api_url, json={"file_path": absolute_test_path})
    if response.status_code == 200:
        st.info(f"Separated the vocal from audio")
        display_vocal_extract(response)
        st.success("Processing complete!")
    else:
        st.error("Failed to process the audio. Please try again.")


def page_karaoke():
    st.markdown("<h1>Karaoke</h1>", unsafe_allow_html=True)

    # Navigation with st.tabs
    selected_tab = st.tabs(
        ["Lyric Finder", "Audio Transcription", "YouTube Video Transcription"]
    )

    # Section 1: Lyric Finder
    with selected_tab[0]:
        st.title("Lyric Finder")
        song_title = st.text_input("Enter the song title")
        artist_name = st.text_input("Enter the artist name")
        if st.button("Get Lyrics"):
            song = api.search_song(song_title, artist_name)
            if song is not None:
                st.write(song.lyrics)
            else:
                st.write("Song not found. Please check the song title and artist name.")

    # Section 2: Audio Transcription
    with selected_tab[1]:
        st.title("Audio Transcription")
        uploaded_audio = st.file_uploader(
            "Upload an audio file", type=["mp3", "wav", "ogg", "flac"]
        )
        if uploaded_audio:
            st.audio(uploaded_audio, format="audio/wav")
            transcribe_button = st.button(
                "Transcribe Audio and Extract Vocal", type="primary"
            )
            if transcribe_button:
                uploaded_audio_path = save_uploaded_audio(uploaded_audio)
                transcribe_audio(uploaded_audio_path)
                extract_vocal(uploaded_audio_path)

    # Section 3: YouTube Video Transcription
    with selected_tab[2]:
        st.title("YouTube Video Transcription")
        youtube_url = st.text_input("Enter YouTube Video URL:")
        if st.button("Download, Extract, and Transcribe"):
            if youtube_url:
                audio_file_path = download_audio(
                    youtube_url, "audio/youtube"  # change the output directory
                )
                model = whisper.load_model("base")
                extract_vocal(audio_file_path)
                autoplay_audio(audio_file_path)
                lyrics_sync(audio_file_path, model)
            else:
                st.warning("Please enter a valid YouTube video URL.")


def play_youtube_video(video_url):
    st.video(video_url)


def lyrics_sync(audio_file_path, model):
    result = model.transcribe(audio_file_path, fp16=False, verbose=True)
    lyrics_placeholder = st.empty()  # Create a placeholder for the lyrics
    start_time = time.time()  # Get the current time
    for sentence in result["segments"]:
        # Calculate the start and end time of the sentence relative to the current time
        sentence_start_time = start_time + sentence["start"] - 1
        sentence_end_time = start_time + sentence["end"] - 1
        # Wait until the start time of the sentence
        while time.time() < sentence_start_time:
            time.sleep(0.1)
        # Update the placeholder with the current lyrics
        lyrics = f"{sentence['start']} - {sentence['end']}: {sentence['text']}"
        lyrics_placeholder.text(lyrics)
        # Wait until the end time of the sentence
        while time.time() < sentence_end_time:
            time.sleep(0.1)


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        # md = f"""
        #     <script>
        #     setTimeout(function(){{
        #         var audio = new Audio("data:audio/mp3;base64,{b64}");
        #         audio.play();
        #     }}, 5000);
        #     </script>
        #     """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
