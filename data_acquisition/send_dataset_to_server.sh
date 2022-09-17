#!/bin/bash

SCRIPT_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

$SCRIPT_PATH/create_database_bkup.sh

echo "Archive ready to be sent to server"

SERVER_PATH=/6TB/DATASET/laptop_keyboard_press/dataset.tar.gz

rsync -av  -e 'ssh -p 2224' "$SCRIPT_PATH/bkup/dataset.tar.gz"  miksolo@miksolo.xyz:$SERVER_PATH