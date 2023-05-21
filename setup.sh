#!/bin/bash
apt-get update
apt-get install -y cmake
apt-get install -y libboost-all-dev
apt-get install -y libopenblas-dev liblapack-dev
pip install numpy opencv-python flask
pip install cmake
pip install dlib
