# MMaVVie
### Introduction 
MMaVVie is an app that lets you enjoy music in a new way. With MMaVVie, you can separate any song into its constituent audio parts, such as vocals, drums, bass, and other instruments. You can then listen to or download any combination of these parts, or even perform a karaoke with the lyrics displayed on the screen.

MMaVVie works by extracting audio from a source, either from YouTube or from an uploaded MP3 file. It then uses a deep learning model to automatically detect and separate the audio into four sources: vocals, drums, bass, and other instruments. You can choose which sources you want to hear or mute from the output. You can also save your customized mix as a new MP3 file.

MMaVVie also has a karaoke feature that allows you to sing along with your favourite songs. It uses OpenAI’s Whisper model for transcription and yt-dlp’s API for music extraction. You can see the lyrics of the song on the screen, and hear only the instrumental parts of the audio.

MMaVVie is a fun and innovative app that gives you more control and creativity over your music. It is composed of two parts: the frontend, which is built with Streamlit, and the backend, which is powered by FastAPI. 


### Requirements
```
numpy==1.26.3
pandas==2.2.0
matplotlib==3.8.2
librosa==0.10.1
torch==2.1.2
torchsummary==1.5.1
tqdm==4.66.1
streamlit==1.30.0
loguru==0.7.2
streamlit-player==0.1.5
blinker==1.7.0
click==8.1.7
protobuf==4.25.2
python-dateutil==2.8.2
streamlit_option_menu==0.3.12
yt-dlp==2023.12.30
lyricsgenius==3.0.1
openai-whisper==20231117
openunmix==1.2.1
uvicorn==0.27.0.post1
fastapi==0.109.0
pytube==15.0.0
moviepy==1.0.3
```

### Setup
To run the app, you need to have Python >= 3.6 installed on your system. You also need to install the dependencies listed in the requirements.txt file.

Step 1: Create a virtual environment and install the dependencies
You can use any virtual environment manager of your choice, such as venv, conda, or pipenv. For example, to create a virtual environment using venv, you can run the following command in your terminal:

`python -m venv env`

This will create a folder called env in your current directory, where the virtual environment files will be stored. To activate the virtual environment, you can run the following command:

`source env/bin/activate`

This will change your prompt to indicate that you are in the virtual environment. To install the dependencies, you can clone this repository

run the following command:

`pip install -r requirements.txt`

This will install all the packages listed in the requirements.txt file in your virtual environment.

Step 2: Launch the API
The API is built with FastAPI, a modern and fast web framework for building APIs. To launch the API, you can run the following command in your terminal:

`uvicorn main:app --reload`

This will start a local server on port 8000, and reload the code automatically whenever you make any changes. You can access the API documentation at http://localhost:8000/docs.

Step 3: Launch the UI
The UI is built with Streamlit, an open-source app framework for data science and machine learning. To launch the UI, you can run the following command in your terminal:

`streamlit run app/pages/main.py`

This will open a new browser window on port 8501, where you can interact with the app. You can also access the UI at http://localhost:8501.













##Intro
Applic
requirements
how to set up
