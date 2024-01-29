import os

import numpy as np
import torch
import librosa
from preprocessing.data import DSD100, dataloader, data_split


rate = 8192
window_size = 1024
hop_lenght = 768


def save_stft(dataset_path, save_path):
    """Save the dataset audio file from dsd100 to a spectrogram.
    While saving the spectrogram the spectrogram will save in the shape of 513,128 by extracting patches
    of 128 frames.

    Parameters
    ----------
    dataset_path :str
        path of DSD100 dataset folder
    save_path : str
        path of the folder where the spectrogram needs to save
    """
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        directories = sorted(
            [dir for dir in os.listdir(dataset_path) if dir != ".DS_Store"]
        )

        mixture_folder_path = os.path.join(dataset_path, directories[0])
        sources_folder_path = os.path.join(dataset_path, directories[1])

        # mixture_folder_path = dataset_path + "/" + sorted(os.listdir(dataset_path))[0]
        # sources_folder_path = dataset_path + "/" + sorted(os.listdir(dataset_path))[1]
        # for folder in sorted(os.listdir(mixture_folder_path)):

        for folder in sorted(
            [f for f in os.listdir(mixture_folder_path) if f != ".DS_Store"]
        ):
            mixture_song_folder_path = mixture_folder_path + "/" + folder
            sources_song_folder_path = sources_folder_path + "/" + folder

            for song_name in sorted(os.listdir(mixture_song_folder_path)):
                # for song_name in sorted([name for name in os.listdir(mixture_song_folder_path) if name != '.DS_Store']):
                mixture_path = (
                    mixture_song_folder_path
                    + "/"
                    + song_name
                    + "/"
                    + sorted(os.listdir(mixture_song_folder_path + "/" + song_name))[0]
                )
                # print(mixture_path)
                bass_path = (
                    sources_song_folder_path
                    + "/"
                    + song_name
                    + "/"
                    + sorted(os.listdir(sources_song_folder_path + "/" + song_name))[0]
                )
                # print(bass_path)
                drum_path = (
                    sources_song_folder_path
                    + "/"
                    + song_name
                    + "/"
                    + sorted(os.listdir(sources_song_folder_path + "/" + song_name))[1]
                )
                # print(drum_path)
                vocal_path = (
                    sources_song_folder_path
                    + "/"
                    + song_name
                    + "/"
                    + sorted(os.listdir(sources_song_folder_path + "/" + song_name))[3]
                )
                # print(vocal_path)
                for char in ["&", "'"]:
                    song_name = song_name.replace(char, "")
                print(song_name)
                # load .wav file
                mixture_arr, _ = librosa.load(mixture_path, sr=rate)
                bass_arr, _ = librosa.load(bass_path, sr=rate)
                drum_arr, _ = librosa.load(drum_path, sr=rate)
                vocal_arr, _ = librosa.load(vocal_path, sr=rate)
                instrumental_arr = mixture_arr - vocal_arr

                # use stft on audio file
                mixture_stft = librosa.stft(
                    mixture_arr, n_fft=window_size, hop_length=hop_lenght
                )
                bass_stft = librosa.stft(
                    bass_arr, n_fft=window_size, hop_length=hop_lenght
                )
                drum_stft = librosa.stft(
                    drum_arr, n_fft=window_size, hop_length=hop_lenght
                )
                vocal_stft = librosa.stft(
                    vocal_arr, n_fft=window_size, hop_length=hop_lenght
                )
                instrumental_stft = librosa.stft(
                    instrumental_arr, n_fft=window_size, hop_length=hop_lenght
                )

                # normalize stft between [0, 1]
                # mixture_stft = ((np.abs(mixture_stft)-np.min(np.abs(mixture_stft)))
                #             / (np.max(np.abs(mixture_stft))-np.min(np.abs(mixture_stft)))
                #             )
                # bass_stft = ((np.abs(bass_stft)-np.min(np.abs(bass_stft)))
                #             / (np.max(np.abs(bass_stft))-np.min(np.abs(bass_stft)))
                #             )
                # drum_stft = ((np.abs(drum_stft)-np.min(np.abs(drum_stft)))
                #             / (np.max(np.abs(drum_stft))-np.min(np.abs(drum_stft)))
                #             )
                # vocal_stft = ((np.abs(vocal_stft)-np.min(np.abs(vocal_stft)))
                #             / (np.max(np.abs(vocal_stft))-np.min(np.abs(vocal_stft)))
                #             )
                # instrumental_stft = ((np.abs(instrumental_stft)-np.min(np.abs(instrumental_stft)))
                #             / (np.max(np.abs(instrumental_stft))-np.min(np.abs(instrumental_stft)))
                #             )
                index = 1
                for i in range(0, mixture_stft.shape[1], 25):
                    if 128 + i >= mixture_stft.shape[1]:
                        break
                    np.savez(
                        save_path + "/" + song_name + str(index) + ".npz",
                        mixture=mixture_stft[:, 0 + i : 128 + i],
                        bass=bass_stft[:, 0 + i : 128 + i],
                        drum=drum_stft[:, 0 + i : 128 + i],
                        vocal=vocal_stft[:, 0 + i : 128 + i],
                        instrumental=instrumental_stft[:, 0 + i : 128 + i],
                    )
                    index += 1
                # break
    except Exception as e:
        print(e)

    print(".npz file save complete")


# Inverse STFT
def inv_stft(audio_stft):
    audio_inv_stft = librosa.istft(
        (audio_stft[:511,]),
        n_fft=1024,
        hop_length=768,
    )
    return audio_inv_stft


# Process STFT
def convert_stft(audio_stft, stem_model, device):
    total_frame = audio_stft.shape[1] // 127 + 1
    done_frame = 0
    stem_model.eval()
    for i in range(0, audio_stft.shape[1], 127):
        mixture = np.abs(audio_stft[:511, i : i + 127])
        col_num = mixture.shape[1]
        if col_num != 127:
            mixture = np.concatenate(
                (mixture, np.zeros(shape=(511, 127 - col_num))), axis=1
            )

        mixture = torch.from_numpy(mixture[np.newaxis, np.newaxis, :, :]).to(device)
        input = dataloader(mixture.to(torch.float32), batch_size=1)
        with torch.no_grad():
            for x in input:
                # print(x.shape)
                y = stem_model(x)
                if i == 0:
                    output = y[0][0]
                else:
                    if col_num == 127:
                        output = torch.cat([output, y[0][0]], dim=1)
                    else:
                        output = torch.cat([output, y[0][0][:, :col_num]], dim=1)
        done_frame += 1
        # print(f"{done_frame}/{total_frame}")
    return output
