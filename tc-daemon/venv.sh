#!/bin/bash

VENV_DIR=".venv"

if [ ! -d $VENV_DIR ]; then
    python3 -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    python3 -m pip install -r requirements.txt
fi
