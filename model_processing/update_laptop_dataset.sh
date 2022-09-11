#!/usr/bin/bash

# This script is used to update the dataset from the laptop

SERVER_PATH=/6TB/DATASET/laptop_keyboard_press/dataset.tar.gz

LAPTOP_DATASET_PATH="../data_acquisition/laptop_dataset/"

cd $LAPTOP_DATASET_PATH

rsync -av  -e 'ssh -p 2224' miksolo@miksolo.xyz:$SERVER_PATH .


tar -xvzf dataset.tar.gz
rm dataset.tar.gz

