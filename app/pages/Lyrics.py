import streamlit as st
import lyricsgenius as genius

# Set up Genius API
api = genius.Genius("v_CyxiEGCu4AlDye7BXWPP4X8a5wij5AjfR2thvUnoMPQJAbmga7SLY8ReD8c5D4")

# Create Streamlit page
st.title("Genius Lyric Finder")

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
