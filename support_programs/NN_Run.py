import os
import matlab.engine
from PIL import Image

if __name__ == '__main__':
    eng = matlab.engine.start_matlab()

    networkName = 'NN_V03_01.onnx' # Neural network
    classes = ["anger", "neutral", "scream", "smile"] # Specify classes


    # Import image
    image = Image.open('out_test/anger/m-daniel-1.png')

    net = eng.importONNXNetwork(networkName,'OutputLayerType','classification').issparse() #'ClassNames',classes)
    # [Yprob, category] = eng.classify(net, image)
    # output = eng.classify(net, image)
    # print(output)

