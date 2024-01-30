import asyncio
import tempfile
from loguru import logger as log
import sys
import numpy as np
import torchaudio
import torch
import librosa
from fastapi import FastAPI, File, UploadFile
from openunmix import predict
from utils import separate_stem

sys.path.append("../")
from preprocessing.transform import convert_stft

app = FastAPI()


def separate_unet(waveform, sample_rate):
    stem = "vocal"
    device = torch.device("cpu")
    model = torch.load(f"../model/save/{stem}_best_model.pt", map_location=device)
    audio_output = separate_stem(waveform, sample_rate, model)
    estimates = {"vocals": audio_output}
    return estimates


def separate_ummix(waveform, sample_rate):
    estimates = predict.separate(
        audio=waveform,
        rate=sample_rate,
        # targets=["vocals"],
        # residual=True
        # model_str_or_path="unmix/unmix-vocal",
    )

    # Audio(estimates['vocals'].squeeze(0), rate=sample_rate)

    # est_dict = {"vocal": waveform}
    return estimates


# FastAPI endpoint to handle audio separation
@app.post("/separate_sota")
async def separate_model_sota(audio_file: UploadFile = File(...)):
    waveform, sample_rate = torchaudio.load(audio_file.file)
    # waveform = waveform.numpy()

    separated_audio = separate_ummix(waveform, sample_rate)
    # separated_audio = separate_unet(audio_file.file)

    waveform_vocal = separated_audio["vocals"]
    waveform_drum = separated_audio["drums"]
    waveform_bass = separated_audio["bass"]
    waveform_other = separated_audio["other"]

    np.save("vocal.npy", waveform_vocal)
    np.save("drum.npy", waveform_drum)
    np.save("bass.npy", waveform_bass)
    np.save("other.npy", waveform_other)

    return {
        "sr": sample_rate,
        "vocal": "api/vocal.npy",
        "drum": "api/drum.npy",
        "bass": "api/bass.npy",
        "other": "api/other.npy",
    }


@app.post("/separate")
async def separate_model_train(audio_file: UploadFile = File(...)):
    # Create a temporary file
    # with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
    #     # Save the uploaded file to the temporary file
    #     contents = await audio_file.read()
    #     temp_audio.write(contents)
    #     temp_audio.flush()

    waveform, sample_rate = librosa.load(audio_file.file, sr=11025)
    # # waveform = waveform.numpy()

    # # separated_audio = separate_ummix(waveform, sample_rate)
    separated_audio = separate_unet(waveform, sample_rate)

    waveform_vocal = separated_audio["vocals"]
    np.save("waveform.npy", waveform_vocal)

    return {"sr": sample_rate, "waveform": "api/waveform.npy"}
