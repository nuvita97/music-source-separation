import numpy as np
import requests
import streamlit as st
from loguru import logger as log
from pathlib import Path
import lyricsgenius as genius
import whisper
import os

# Set up Genius API
api = genius.Genius("v_CyxiEGCu4AlDye7BXWPP4X8a5wij5AjfR2thvUnoMPQJAbmga7SLY8ReD8c5D4")

# Define the base directory
# base_path = Path(
#     "Users/nguyenvietthai/Library/CloudStorage/OneDrive-EPITA/S3. Action Learning/music-source-separation/audio"
# )
in_path = Path("audio/input/")

# Define the input directory
in_path.mkdir(parents=True, exist_ok=True)


def page_karaoke():
    st.markdown("<h1>Karaoke</h1>", unsafe_allow_html=True)

    # Add Genius Lyric Finder code
    st.title("Lyric Finder")

    # Input for song title and artist
    song_title = st.text_input("Enter the song title")
    artist_name = st.text_input("Enter the artist name")

    # Button to fetch lyrics
    if st.button("Get Lyrics"):
        # Search for the song on Genius
        song = api.search_song(song_title, artist_name)

        # Check if a song was found
        if song is not None:
            # Display the lyrics
            st.write(song.lyrics)
        else:
            st.write("Song not found. Please check the song title and artist name.")

    # Add audio file upload and transcription functionality
    st.title("Audio Transcription")

    uploaded_audio = st.file_uploader(
        "Upload an audio file", type=["mp3", "wav", "ogg", "flac"]
    )

    if uploaded_audio:
        st.audio(uploaded_audio, format="audio/wav")
        transcribe_button = st.button(
            "Transcribe Audio & Extract Vocal", type="primary"
        )

        if transcribe_button:
            # Perform transcription using Whisper
            uploaded_audio_path = save_uploaded_audio(uploaded_audio)
            transcribe_audio(uploaded_audio_path)

        extract_button = st.button("Extract Vocal", type="primary")

        if extract_button:
            # Perform Vocal Extraction
            processing_message = st.empty()
            processing_message.info("Processing uploaded file...")
            api_url = "http://127.0.0.1:8000/separate_karaoke"
            response = requests.post(api_url, files={"audio_file": uploaded_audio})
            processing_message.empty()

            if response.status_code == 200:
                st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
                st.info(f"Separated the vocal from audio")
                display_vocal_extract(response)
                st.success("Processing complete!")
            else:
                st.error("Failed to process the audio. Please try again.")

        # extract_button = st.button("Extract Vocal", type="primary")


def save_uploaded_audio(uploaded_audio):
    # Save the uploaded audio file to a temporary location
    temp_path = in_path / "uploaded_audio.mp3"
    with temp_path.open("wb") as audio_file:
        audio_file.write(uploaded_audio.read())
    return str(temp_path)


def transcribe_audio(audio_path):
    # Perform transcription using Whisper
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
    st.audio(residual_array, sample_rate=sample_rate)


def callback():
    st.session_state.transcribe_button = True


# Call this function at the end of your script to run the app
page_karaoke()
