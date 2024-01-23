import os

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, random_split

torch.manual_seed(100)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DSD100(Dataset):
    def __init__(self, data_path):
        self.spectrogram_path = [
            data_path + "/" + name for name in sorted(os.listdir(data_path))
        ]

    def __len__(self):
        return len(self.spectrogram_path)

    def __getitem__(self, index):
        data = np.load(self.spectrogram_path[index])
        mixture = data["mixture"][np.newaxis, :511, :127]
        bass = data["bass"][np.newaxis, :511, :127]
        drum = data["drum"][np.newaxis, :511, :127]
        vocal = data["vocal"][np.newaxis, :511, :127]
        instrumental = data["instrumental"][np.newaxis, :511, :127]
        return (
            torch.from_numpy(np.abs(np.copy(mixture))).to(device),
            torch.from_numpy(np.abs(np.copy(bass))).to(device),
            torch.from_numpy(np.abs(np.copy(drum))).to(device),
            torch.from_numpy(np.abs(np.copy(vocal))).to(device),
            torch.from_numpy(np.abs(np.copy(instrumental))).to(device),
        )


def data_split(dataset, train_ratio=0.8):
    return random_split(dataset, [train_ratio, 1 - train_ratio])


def dataloader(dataset, batch_size=64, shuffle=False):
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)