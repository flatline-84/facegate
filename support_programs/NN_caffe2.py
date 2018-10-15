import onnx
import caffe2.python.onnx.backend
from PIL import Image
import numpy as np

# # Prepare the inputs, here we use numpy to generate some random inputs for demo purpose
# import numpy as np
# img = np.random.randn(1, 3, 224, 224).astype(np.float32)

# Load the ONNX model
model = onnx.load('../matlab/NeuralNetworks/NN_V02_Test.onnx')
# Run the ONNX model with Caffe2

print("Loaded the model")

# Import image
faceImg = Image.open('out_test/anger/m-daniel-1.png')
faceNp = np.array(faceImg)
img = np.random.randn(1,1,224,224).astype(np.float32)
print("Loaded the image")

outputs = caffe2.python.onnx.backend.run_model(model, [img])

# outputs = caffe2.python.onnx.backend.run_model(model, [faceNp])
print(outputs)