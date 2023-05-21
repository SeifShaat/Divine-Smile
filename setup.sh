#!/bin/bash
apt-get update
apt-get install -y build-essential cmake
apt-get install -y libopenblas-dev liblapack-dev
pip install numpy opencv-python flask
pip install dlib
