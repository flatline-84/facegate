import os
import matlab.engine




if __name__ == '__main__':
    eng = matlab.engine.start_matlab()

    networkName = 'NN_Daniel_04_78,4.onnx' # Neural network
    classes = ["anger", "neutral", "scream", "smile"] # Specify classes

    net = eng.importONNXNetwork(networkName,'OutputLayerType','classification') #'ClassNames',classes)

    # Import image

    [Yprob, category] = classify(net, image)

