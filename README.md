# FaceGate

FaceGate is a novel program to classify actions from a variety of input sources to then control a hardware component.
Requires Python >=3.4

## Required Python libraries
### Can be installed with `sudo pip3 install [xxx]`
* numpy - math calculations and data handling
* opencv-python - openCV bindings for Python
* pystasm - openStasm bindings for Python. Requires OpenCV source
* Pillow - Imaging library to display images
* pyserial - Connecting to the Arduino
* olimex-ekg-emg - EMG library
* matplotlib - For graphing
* PyOpenGL - Arm simulation
* PyOpenGL_accelerate - Arm Simulation
* pygame
* scipy
* onnx
* onnx-mxnet

python3 olimex_test.py -p /dev/ttyUSB0

### From apt-get
* python3-pil.imagetk

### Neural Network Test
* tensorflow
* tflearn (simplifies tensorflow)

### Needed library modules
pystasm requires the OpenCV source code to be installed on your system. There is a script here to install it.

### Arduino Arm Modules
Requires 'braccio' library to be installed via Library Manager.