# File with code for preprocessing after dataset is ready

### Imports here! ###
from datetime import datetime
import numpy as np
from pynput import keyboard
import time
import pandas as pd
import os.path
import argparse,logging, sys # All nice things
from scipy.io import wavfile



def get_spectrum_from_path(path,db=True, n_fft=2048, hop_length=512):
    samplerate, data = wavfile.read(path)
    mono_data = data.transpose()[0]
    sfft = librosa.core.stft(mono_data, hop_length=hop_length, n_fft=n_fft )
    spectrogram = np.abs(sfft)
    if db:
        spectrogram = librosa.amplitude_to_db(spectrogram)
    return spectrogram
    
    
def load_data(path_to_csv):
    pass
    # return inputs,targets