#!/bin/bash
apt-get update
apt-get install -y build-essential cmake
apt-get install -y libopenblas-dev liblapack-dev
pip install numpy opencv-python flask

# Manually install Dlib and its dependencies
cd ~
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake ..
cmake --build .
cd ..
python setup.py install
