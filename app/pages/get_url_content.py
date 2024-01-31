import os
import streamlit as st
import yt_dlp

# function to download audio of youtube video from url
def download_audio(yt_url, output_folder):
    
    # check if output folder exist, if not, create it
    if not os.path.exists(output_folder):
         os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    }                                   # these are like our predefined parameters
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
        with open(os.path.join(output_folder, file_name), 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)

        return "File downloaded successfully"
    except Exception as e:
        return f"An error occurred: {e}"


youtube_url = st.text_input("Enter the YouTube video URL: ")
other_url = st.text_input("Enter the other video or audio download link: ")

if st.button('Get Audio'):
    if youtube_url:
        download_audio(youtube_url, 'youtube_extractions')
        st.success("YouTube audio downloaded successfully")
    elif other_url:
        message = download_file(other_url, 'other_source_extraction')
        st.success(message)
    else:
        st.error("Please enter a URL")
