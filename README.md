# Keyboard side channeling

This repository contains my attempt at reproducing the keyboard side channeling attack with deep learning approach described in [this article](https://towardsdatascience.com/audio-deep-learning-made-simple-sound-classification-step-by-step-cebc936bbe5 ).


# Data collection

The bright side of this project is that it is relatively easy to prepare a custom dataset for classifing keys. For that 

## Requirements for data collection

- Python 3.6
- Install packages from `data_acquisition/requirements.txt` file


## Data collection process

1. Run `python3 data_acquisition/get_key_sample.py` script. It will record audio from your microphone and save it to your current directory `samples_dataset` will contain audio files and file `dataset.csv`. You can change directory and name of the CSV file using `--csv` flag and the path. Also you can change `samples_dataset` folder to your liking using `--datasetpath` flag and your own path. The script will stop recording when you press `escape`.

```
Data Acquisition system to record dataset of keyboard sounds

options:
  -h, --help            show this help message and exit
  -d CSV, --csv CSV     Path for database (default: dataset.csv)
  --datasetpath DATASETPATH
                        Path for dataset files (default: samples_dataset)
  --nodatabase NODATABASE
                        Use to not create database files only record audio files
  -i INDEX, --index INDEX
                        Index for the first sample
```

2. You can add comments to the dataset using `--comment` flag. For example `python3 data_acquisition/get_key_sample.py --comment "I am recording my keyboard"` will add a comment to the dataset.

3. After recording is done you will have a `dataset.csv` file with the following structure:

`id , path , key_pressed , num_of_samples , time_created , comment`



# Model training and evaluation

After data is collected you can use it to train your model.

After installation you can use `model_processing/audio_process_notebook.ipynb` notebook to train and evaluate your model. It has it's own comments. Also 
`utils.py` and `dataset_tools.py` are used in the notebook as imported class and function. If you interested in them you can also check them out.

## Requirements for model processing

### Containerized installation

For model processing I use a containerized environment. To build the container, run the following command:

    `docker-compose up -d --build`

Then you will be able to connect to it's jupyter notebook server on your local 8000 port. To check the exact address, run:

    `docker-compose logs`

### Local installation

If you want to install the environment locally, you will need to install:

- Python 3.8 or higher
- PyTorch and pytorch-audio
- CUDA 11.6 (or compatible with your pytorch version)
- Packages from `model_processing/requirements.txt` file
