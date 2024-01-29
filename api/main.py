import io
import os
import base64
import numpy as np
import torchaudio
import librosa
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from openunmix import predict

app = FastAPI()


# Function to perform audio separation using your model (replace with your logic)
def separate_ummix(waveform, sample_rate):
    estimates = predict.separate(
        audio=waveform,
        rate=sample_rate,
        targets=["vocals"],
        residual=True
        # residual=True,
        # model_str_or_path="unmix/unmix-vocal",
    )

    # Audio(estimates['vocals'].squeeze(0), rate=sample_rate)

    # est_dict = {"vocal": waveform}
    return estimates


# FastAPI endpoint to handle audio separation
@app.post("/separate")
async def separate_audio(audio_file: UploadFile = File(...)):
    waveform, sample_rate = torchaudio.load(audio_file.file)

    # Read the contents of the uploaded audio file
    # audio_content = await audio_file.read()

    # Perform audio separation
    separated_audio = separate_ummix(waveform, sample_rate)

    waveform_vocal = separated_audio["vocals"]
    np.save("waveform.npy", waveform_vocal)

    return {"sr": sample_rate, "waveform": "api/waveform.npy"}
    # return FileResponse("waveform.npy", media_type="application/octet-stream")

    # # Convert the numpy array to bytes
    # waveform_bytes = io.BytesIO()
    # np.save(waveform_bytes, waveform)
    # waveform_bytes = waveform_bytes.getvalue()

    # # Convert bytes to base64 string
    # waveform_str = base64.b64encode(waveform_bytes).decode("utf-8")

    # # Return the waveform and sample rate as a response
    # return JSONResponse(content={"sr": sample_rate, "waveform": waveform_str})
