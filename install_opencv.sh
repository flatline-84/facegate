#!/bin/bash

OPENCV_VERSION='3.4.2'

# 1. Update Ubuntu

sudo apt-get -y update
sudo apt-get -y upgrade
#sudo apt-get -y dist-upgrade
#sudo apt-get -y autoremove


# 2. Install dependencies
# Build tools:
sudo apt-get install -y build-essential cmake

# OpenCV dependencies
sudo apt-get install -y qt5-default libvtk6-dev zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libopenexr-dev libgdal-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libv4l-dev libxine2-dev libtbb-dev libeigen3-dev

# Python
sudo apt-get install -y python-dev python-tk python-numpy python3-dev python3-tk python3-numpy


# 3. INSTALL THE LIBRARY

sudo apt-get install -y unzip wget
wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip
unzip ${OPENCV_VERSION}.zip
rm ${OPENCV_VERSION}.zip
mv opencv-${OPENCV_VERSION} OpenCV
cd OpenCV
mkdir build
cd build
cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON -DENABLE_PRECOMPILED_HEADERS=OFF ..
make -j2
sudo make install
sudo ldconfig
cd ../../
rm -rf OpenCV

sudo pip3 install PyStasm
