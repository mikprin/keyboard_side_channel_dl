
### Imports here! ###
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pynput import keyboard
import time
import pandas as pd
import os.path
import argparse,logging, sys # All nice things

### Temp or default Settings ###
audio_sample_rate = 44100  # Sample rate
sample_duration = 0.3  # Duration of sub recording in a sample
recordings_count = 3 # Number if sub recordings in a sample
recordings_after_the_press = 2 # Delay after the press


dataset_folder = "samples_dataset"
database_file_name = "dataset.csv"

### Settings imported here ###

# No settings file yet!



### Global handler variables ###

stop_flag = False
key_pressed = ""
record_flag = True


### Logging ###

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)


class Button_Sample():
    '''Class for getting a button press from the numpy array and key stroke information'''
    def __init__(self, id, recordings,button_key,dataset_folder="samples_dataset" ,sample_rate = 44100,comment=""):
        self.comment = "" # Comment for database (if present)
        self.button_key = button_key # Key that was pressed
        self.sample_rate = sample_rate
        self.dataset_folder = dataset_folder # Folder with dataset
        self.id = id # ID for database
        self.time_created = int(time.time())
        if len(recordings) > 1:
            self.full_recording = np.concatenate(recordings)
        elif len(recordings) == 1:
            self.full_recording = recordings[0]
        else:
            raise ValueError('Empty recording list passed to the Button_Sample class.')
        self.num_samples = len(self.full_recording)
        self.save_file()
        
    def save_file(self):
        self.path = f'{self.dataset_folder}/{self.id}.wav'
        write(self.path, self.sample_rate, self.full_recording)  # Save as WAV file 
        

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

### Functions to work with database ###

class Sounds_Database():
    def __init__(self,path_to_csv,dataset_folder="samples_dataset"):
        self.dataset_folder = dataset_folder
        self.dataframe = self.read_database(path_to_csv)
        self.path = path_to_csv
        if not os.path.isdir(self.dataset_folder):
            os.mkdir(self.dataset_folder)
        
    def read_database(self,path="database.csv"):
        '''Init database'''
        print(f"PATH IS: {path}")
        if os.path.isfile(path):
            database = pd.read_csv(path)
        else:
            # Creating empty database from shema
            schema = ["id","path","key_pressed","num_of_samples","time_created","comment"]
            database = pd.DataFrame(columns =schema)
        self.path = path
        return database

    def update_on_disk(self,backup=False):
        self.dataframe.to_csv(self.path,index=False)
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Data Acquisition system to record dataset of keyboard sounds')
    parser.add_argument('-d','--csv', type=str , help="Path for database")
    parser.add_argument('--datasetpath', type=str , help="Path for dataset")
    parser.add_argument('--nodatabase', type=str , help="Use to not create database files")
    args = parser.parse_args()
    
    if args.datasetpath:
        dataset_folder = args.datasetpath
    
    if args.csv:
        database_file_name = args.csv
    database = Sounds_Database(database_file_name,dataset_folder=dataset_folder)
    
    
    
    # Parse database
    ## Get index from the database!
    
    if args.nodatabase or len(database.dataframe) == 0:
        index = 0
    else:
        index = int(database.dataframe.iloc[-1:]["id"]) + 1
    
    time.sleep(0.2) # Delay to avoid starting to early
    exit_command = False
    logging.info(f'Recording of key presses started')
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    logging.info(f'Listener started')
    
    

    while not exit_command:
        sample = record_next_press()
        if not exit_command:
            # index += 1 # Iterate index since index = last index used
            button_press = Button_Sample(index,sample,key_pressed,dataset_folder=dataset_folder)
            new_database_entery = {
                "id":index,"path":button_press.path,
                "key_pressed":button_press.button_key,
                "num_of_samples":button_press.num_samples,
                "time_created":button_press.time_created,
                "comment":button_press.comment
            }
            temp_df = pd.DataFrame(new_database_entery,index=[0])
            # logging.info(f"New entery: {pd.DataFrame(new_database_entery,index=[0])}")
            if not args.nodatabase:
                database.dataframe = pd.concat([database.dataframe,temp_df])
                database.update_on_disk()
                
        index += 1
        time.sleep(0.1) # Small delay here to avoid double taps
        
        
    