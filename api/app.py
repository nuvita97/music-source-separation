import streamlit as st
import requests


# Streamlit app code
def main():
    st.title("Audio Separation App")
    st.write("Upload an audio file and separate it using FastAPI")

    # File upload
    audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

    if audio_file is not None:
        # Display uploaded audio file
        st.audio(audio_file, format="audio/wav")

        # Button to start separation
        if st.button("Separate Audio"):
            # Send audio file to FastAPI for separation
            response = requests.post(
                "http://localhost:8000/separate", files={"audio": audio_file}
            )

            if response.status_code == 200:
                # Display separated audio files
                st.write("Separated Audio Files:")
                for file_name, file_content in response.json().items():
                    st.audio(file_content, format="audio/wav", caption=file_name)
            else:
                st.error("Error occurred during separation")


if __name__ == "__main__":
    main()
