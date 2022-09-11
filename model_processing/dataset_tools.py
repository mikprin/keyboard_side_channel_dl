# File with support code for working with dataset

### Imports here! ###
from datetime import datetime
import numpy as np
# from pynput import keyboard
import time
import pandas as pd
import os.path
import argparse,logging, sys # All nice things


import math, random
import torch
import torchaudio
from torchaudio import transforms
from IPython.display import Audio
from sklearn import preprocessing

class AudioUtil():
    # ----------------------------
    # Load an audio file. Return the signal as a tensor and the sample rate
    # ----------------------------
    @staticmethod
    def open(audio_file):
        sig, sr = torchaudio.load(audio_file)
        return (sig, sr)
    # ----------------------------
    # Generate a Spectrogram
    # ----------------------------
    @staticmethod
    def spectro_gram(aud, n_mels=64, n_fft=1024, hop_len=None):
        sig,sr = aud
        top_db = 80

        # spec has shape [channel, n_mels, time], where channel is mono, stereo etc
        spec = transforms.MelSpectrogram(sr, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(sig)

        # Convert to decibels
        spec = transforms.AmplitudeToDB(top_db=top_db)(spec)
        return (spec)
    
    
class SoundDS(torch.utils.data.Dataset):
    def __init__(self, df, data_path):
        self.df = df
        self.test_keys = self.get_unique_keys(df)
        self.data_mapper = preprocessing.LabelEncoder()
        targets = self.data_mapper.fit_transform(self.test_keys)
        # targets: array([0, 1, 2, 3])
        targets = torch.as_tensor(targets)
        self.data_path = str(data_path)
        # self.duration = 4000
        self.sr = 44100
        self.channel = 2
        self.shift_pct = 0.4
              
    # ----------------------------
    # Number of items in dataset
    # ----------------------------
    def __len__(self):
        return len(self.df)    
      
    # ----------------------------
    # Get i'th item in dataset
    # ----------------------------
    def __getitem__(self, idx):
        # Absolute file path of the audio file - concatenate the audio directory with
        # the relative path
        # audio_file = self.data_path + self.df.loc[idx, 'path']
        audio_file = os.path.join( self.data_path ,  self.df.loc[idx, 'path'])
        # Get the Class ID
        class_id = self.data_mapper.transform( [self.df.loc[idx, 'key_pressed']] )[0]

        aud = AudioUtil.open(audio_file)
        # Some sounds have a higher sample rate, or fewer channels compared to the
        # majority. So make all sounds have the same number of channels and same 
        # sample rate. Unless the sample rate is the same, the pad_trunc will still
        # result in arrays of different lengths, even though the sound duration is
        # the same.
        # reaud = AudioUtil.resample(aud, self.sr)
        # rechan = AudioUtil.rechannel(reaud, self.channel)

        # dur_aud = AudioUtil.pad_trunc(rechan, self.duration)
        # shift_aud = AudioUtil.time_shift(dur_aud, self.shift_pct)
        sgram = AudioUtil.spectro_gram(aud, n_mels=64, n_fft=1024, hop_len=None)
        # aug_sgram = AudioUtil.spectro_augment(sgram, max_mask_pct=0.1, n_freq_masks=2, n_time_masks=2)

        return sgram, class_id
  
    def get_unique_keys(self,df):
        keys = []
        for key in df['key_pressed']:
            if key not in keys:
                keys.append(key)
        return keys  