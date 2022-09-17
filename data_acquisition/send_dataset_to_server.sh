#!/bin/bash

SCRIPT_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

$SCRIPT_PATH/create_database_bkup.sh
echo "Archive ready to be sent to server"

SERVER_PATH=/6TB/DATASET/laptop_keyboard_press



SHA_256_PATH="$SCRIPT_PATH/bkup/dataset.tar.gz.sha256"
sha256sum $SCRIPT_PATH/bkup/dataset.tar.gz | cut -d ' ' -f 1 > $SHA_256_PATH

rsync -av  -e 'ssh -p 2224' "$SCRIPT_PATH/bkup/dataset.tar.gz"  miksolo@miksolo.xyz:$SERVER_PATH
rsync -av  -e 'ssh -p 2224' "$SHA_256_PATH"  miksolo@miksolo.xyz:$SERVER_PATH