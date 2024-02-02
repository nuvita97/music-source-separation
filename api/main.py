import os
import sys
import numpy as np
import torchaudio
import torch
import librosa
from pydantic import BaseModel
from pathlib import Path
from fastapi import FastAPI, HTTPException
from openunmix import predict
from utils import separate_stem

sys.path.append("../")

app = FastAPI()

save_path = Path("save/")
save_path.mkdir(parents=True, exist_ok=True)


class AudioRequest(BaseModel):
    file_path: str


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
        # model_str_or_path="unmix/unmix-vocal",
    )
    return estimates


def extract_vocal(waveform, sample_rate):
    estimates = predict.separate(
        audio=waveform, rate=sample_rate, targets=["vocals"], residual=True
    )
    return estimates


# @app.post("/separate_sota")
# async def separate_sota_by_file(audio_file: UploadFile = File(...)):
#     waveform, sample_rate = torchaudio.load(audio_file.file)
#     separated_audio = separate_ummix(waveform, sample_rate)
#     result = {"sr": sample_rate}
#     for stem in ["vocals", "drums", "bass", "other"]:
#         waveform = separated_audio[stem]
#         np.save(f"{stem}.npy", waveform)
#         result[stem] = f"api/{stem}.npy"
#     return result


# @app.post("/separate_unet")
# async def separate_unet_by_file(audio_file: UploadFile = File(...)):
#     waveform, sample_rate = librosa.load(audio_file.file, sr=11025)
#     separated_audio = separate_unet(waveform, sample_rate)
#     result = {"sr": sample_rate}
#     for stem in ["vocals", "drums", "bass", "other"]:
#         waveform = separated_audio[stem]
#         np.save(f"{stem}.npy", waveform)
#         result[stem] = f"api/{stem}.npy"
#     return result


@app.post("/separate_karaoke")
async def separate_karaoke_by_path(audio_request: AudioRequest):
    audio_file_path = audio_request.file_path
    if not os.path.isfile(audio_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    waveform, sample_rate = torchaudio.load(audio_file_path)
    separated_audio = extract_vocal(waveform, sample_rate)
    instrument = separated_audio["residual"]
    file_path = save_path / "residual.npy"
    np.save(file_path, instrument)
    result = {"sr": sample_rate, "residual": f"api/{file_path}"}
    return result


@app.post("/separate_unet")
async def separate_unet_by_path(audio_request: AudioRequest):
    audio_file_path = audio_request.file_path
    if not os.path.isfile(audio_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    waveform, sample_rate = librosa.load(audio_file_path, sr=11025)
    separated_audio = separate_unet(waveform, sample_rate)
    result = {"sr": sample_rate}
    for stem in ["vocals", "drums", "bass", "other"]:
        waveform = separated_audio[stem]
        file_path = save_path / f"{stem}.npy"
        np.save(file_path, waveform)
        result[stem] = f"api/{file_path}"
    return result


@app.post("/separate_sota")
async def separate_sota_by_path(audio_request: AudioRequest):
    audio_file_path = audio_request.file_path
    if not os.path.isfile(audio_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    waveform, sample_rate = torchaudio.load(audio_file_path)
    separated_audio = separate_ummix(waveform, sample_rate)
    result = {"sr": sample_rate}
    for stem in ["vocals", "drums", "bass", "other"]:
        waveform = separated_audio[stem]
        file_path = save_path / f"{stem}.npy"
        np.save(file_path, waveform)
        result[stem] = f"api/{file_path}"
    return result
