#!/bin/bash
pip install -r requirements.txt

git submodule update --init --recursive
cd real-esrgan
python3 setup.py develop

echo "Setup completed."