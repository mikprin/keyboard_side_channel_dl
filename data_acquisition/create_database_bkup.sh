#!/usr/bin/bash

# Ccript to run locally to create dataset bkup

mkdir -p bkup

# rsync -av dataset.csv bkup/
# rsync -av samples_dataset bkup/

tar -czvf bkup/dataset.tar.gz dataset.csv samples_dataset