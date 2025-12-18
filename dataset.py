import os
import numpy as np
import torch
from torch.utils.data import Dataset

class MultimodalIEMOCAPDataset(Dataset):
    def __init__(self, folder_names, data_path, params):
        """
        folder_names: list of folder names like 'Ses01F_script01_1b_Emotion'
        data_path: root path of data folders
        params: argparse or namespace with .audio_feature, .video_feature, .text_feature
        """
        self.folder_names = folder_names
        self.data_path = data_path
        self.params = params

    def __len__(self):
        return len(self.folder_names)

    def __getitem__(self, idx):
        name = self.folder_names[idx]

        audio_path = os.path.join(self.data_path, name, 'audio', self.params.audio_feature, 'sample.npy')
        video_path = os.path.join(self.data_path, name, 'video', self.params.video_feature, 'sample.npy')
        text_path  = os.path.join(self.data_path, name, 'text',  self.params.text_feature,  'sample.npy')
        label_path = os.path.join(self.data_path, name, 'label', 'sample.txt')

        audio = torch.from_numpy(np.load(audio_path)).float()
        video = torch.from_numpy(np.load(video_path)).float()
        text  = torch.from_numpy(np.load(text_path)).float()

        with open(label_path, 'r') as f:
            label = int(f.read().strip())

        return text, video, audio, label