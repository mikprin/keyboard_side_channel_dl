from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pynput import keyboard
import time

### Settings imported here ###


### Settings ###
audio_sample_rate = 44100  # Sample rate
sample_duration = 0.3  # Duration of sub recording in a sample
recordings_count = 3 # Number if sub recordings in a sample
recordings_after_the_press = 2 # Delay after the press


samples_folder = "samples_dataset"


### Global handler variables ###

stop_flag = False
key_pressed = ""
record_flag = True


### Logging ###
import logging
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)


class Button_Sample():
    '''Class for getting a button press from the numpy array and key stroke information'''
    def __init__(self, id, recordings,button_key,sample_rate = 44100):
        self.button_key = button_key
        self.sample_rate = sample_rate
        self.id = id
        self.time_created = int(time.time())
        if len(recordings) > 1:
            self.full_recording = np.concatenate(recordings)
        elif len(recordings) == 1:
            self.full_recording = recordings[0]
        else:
            raise ValueError('Empty recording list passed to the Button_Sample class.')
        self.save_file()
        
    def save_file(self):
        global samples_folder
        path = f'{samples_folder}/{self.id}.wav'
        write(path, self.sample_rate, self.full_recording)  # Save as WAV file 
        

def on_press(key):
    global key_pressed
    try:
        logging.info(f'Pressed: {key.char}')
        key_pressed = key.char
        # print('Alphanumeric key pressed: {0} '.format(
        #     key.char))
        # if (key.char == "s"):
        #     print("STOPPING")
    except AttributeError:
        pass
        # print('special key pressed: {0}'.format(
            # key))
        

def on_release(key):
    global stop_flag # Global handle for stopping the program
    global record_flag # Global handle for stopping the sample record
    # print('Key released: {0}'.format(
    #     key))
    if key == keyboard.Key.esc:
        global exit_command
        exit_command = True
        logging.info('Esc pressed exiting!')
        # Stop listener
        return False
    else: stop_flag = True

def record_next_press():
    logging.info(f'Press recording invoked!')
    i = 0
    recordings = []
    global recordings_count
    global record_flag
    global stop_flag
    global exit_command
    while (record_flag) and not exit_command:
        new_recording = sd.rec(int(sample_duration * audio_sample_rate), samplerate=audio_sample_rate, channels=2)
        if len(recordings) > recordings_count:
            recordings.pop(0)
        sd.wait()  # Wait until recording is finished
        recordings.append(new_recording)
        # print(f"record flag: {record_flag}")
        if (stop_flag):
            i += 1
            if i > recordings_after_the_press:
                record_flag = False
    logging.info(f'Key {key_pressed} recorded')
    stop_flag = False
    record_flag = True
    # print(recordings)
    return recordings


# def read_database(path="database.csv"):
    
#     return database


if __name__ == '__main__':
    
    time.sleep(0.4)
    exit_command = False
    logging.info(f'Recording of key presses started')
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    logging.info(f'Listener started')
    index = 0
    while not exit_command:
        sample = record_next_press()
        if not exit_command:
            button_press = Button_Sample(index,sample,key_pressed)
        time.sleep(0.1)
        index += 1
        
    