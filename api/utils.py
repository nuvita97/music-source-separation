import torch
import librosa
import os
import sys
import numpy as np
from IPython.display import Audio

sys.path.append("../")
# print(sys.path)

from preprocessing.transform import convert_stft


def get_audio_stft(file_path, n_fft=1024, hop_length=768):
    audio_array, sr = librosa.load(file_path)
    audio_stft = librosa.stft(audio_array, n_fft=n_fft, hop_length=hop_length)
    return audio_stft


def separate_stem(waveform, sample_rate, model):
    audio_stft = librosa.stft(waveform, n_fft=1024, hop_length=768)
    # audio_stft = get_audio_stft(file_audio)

    device = torch.device("cpu")
    output_stem = (
        convert_stft(audio_stft, model, device).to(torch.device("cpu"))
    ).numpy()

    output_stem = np.multiply(audio_stft[:511, :], output_stem)
    audio_output_stem = librosa.istft(output_stem, n_fft=1024, hop_length=768)

    return audio_output_stem
