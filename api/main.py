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

app = FastAPI()


def separate_unet(waveform, sample_rate):
    device = torch.device("cpu")
    estimates = {}
    for stem in ["vocals", "drums", "bass", "other"]:
        model = torch.load(f"../model/save/{stem}_best_model.pt", map_location=device)
        audio_output = separate_stem(waveform, sample_rate, model)
        estimates[stem] = audio_output
    return estimates


def separate_ummix(waveform, sample_rate):
    estimates = predict.separate(
        audio=waveform,
        rate=sample_rate,
        # targets=["vocals"],
        # residual=True
        # model_str_or_path="unmix/unmix-vocal",
    )
    return estimates


def extract_vocal(waveform, sample_rate):
    estimates = predict.separate(
        audio=waveform, rate=sample_rate, targets=["vocals"], residual=True
    )
    return estimates


# FastAPI endpoint to handle audio separation
@app.post("/separate_sota")
async def separate_model_sota(audio_file: UploadFile = File(...)):
    waveform, sample_rate = torchaudio.load(audio_file.file)
    # waveform = waveform.numpy()

    separated_audio = separate_ummix(waveform, sample_rate)

    result = {"sr": sample_rate}

    for stem in ["vocals", "drums", "bass", "other"]:
        waveform = separated_audio[stem]
        np.save(f"{stem}.npy", waveform)
        result[stem] = f"api/{stem}.npy"

    return result


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

    separated_audio = separate_unet(waveform, sample_rate)

    result = {"sr": sample_rate}

    for stem in ["vocals", "drums", "bass", "other"]:
        waveform = separated_audio[stem]
        np.save(f"{stem}.npy", waveform)
        result[stem] = f"api/{stem}.npy"

    return result


@app.post("/separate_karaoke")
async def separate_model_karaoke(audio_file: UploadFile = File(...)):
    waveform, sample_rate = torchaudio.load(audio_file.file)
    separated_audio = extract_vocal(waveform, sample_rate)
    instrument = separated_audio["residual"]
    np.save(f"residual.npy", instrument)
    instrument_array = f"api/residual.npy"
    result = {"sr": sample_rate, "residual": instrument_array}
    return result
