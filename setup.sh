#!/bin/bash
pip install --upgrade pip
pip install -r requirements.txt

git submodule update --init --recursive
cd real-esrgan
pip install -r requirements.txt
python setup.py develop

echo "Setup completed."