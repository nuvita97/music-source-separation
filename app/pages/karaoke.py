import streamlit as st
from pathlib import Path
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import lyricsgenius as genius

# Set up Genius API
api = genius.Genius("v_CyxiEGCu4AlDye7BXWPP4X8a5wij5AjfR2thvUnoMPQJAbmga7SLY8ReD8c5D4")

# Define the base directory
base_path = Path("C:/Users/HP/Documents/EPITA S3/Action Learning/music-source-separation/audio")

# Define the input directory
in_path = base_path / "input"
in_path.mkdir(parents=True, exist_ok=True)

# Function to download YouTube video, extract audio, and transcribe
def download_extract_transcribe_youtube(video_url):
    st.info("Downloading video...")

    # Download the video
    youtube = YouTube(video_url)
    video = youtube.streams.first()
    downloaded_file = video.download()

    st.info("Extracting audio...")

    # Extract audio
    video_clip = VideoFileClip(downloaded_file)
    audio_clip = video_clip.audio
    audio_file_path = in_path / "youtube_audio.mp3"
    audio_clip.write_audiofile(str(audio_file_path))

    st.info("Transcribing audio...")

    # Perform transcription using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(str(audio_file_path), fp16=False, verbose=True)

    # Display the transcribed text
    st.write(f"Transcription Result: {result['text']}")

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

    # Display the transcribed text
    st.write(f"Transcription Result: {result['text']}")

# Updated version using st.tabs
def page_karaoke():
    st.markdown("<h1>Karaoke</h1>", unsafe_allow_html=True)

    # Navigation with st.tabs
    selected_section = st.tabs(["Lyric Finder", "Audio Transcription", "YouTube Video Transcription"])

    # Section 1: Lyric Finder
    with selected_section[0]:
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
    with selected_section[1]:
        st.title("Audio Transcription")
        uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "flac"])
        if uploaded_audio:
            st.audio(uploaded_audio, format='audio/wav')
            transcribe_button = st.button("Transcribe Audio", type="primary")
            if transcribe_button:
                uploaded_audio_path = save_uploaded_audio(uploaded_audio)
                transcribe_audio(uploaded_audio_path)

    # Section 3: YouTube Video Transcription
    with selected_section[2]:
        st.title("YouTube Video Transcription")
        youtube_url = st.text_input("Enter YouTube Video URL:")
        if st.button("Download, Extract, and Transcribe"):
            if youtube_url:
                play_youtube_video(youtube_url)
                download_extract_transcribe_youtube(youtube_url)
            else:
                st.warning("Please enter a valid YouTube video URL.")


def play_youtube_video(video_url):
    st.video(video_url)
