import mxnet as mx
import onnx_mxnet
import numpy as np
from matplotlib.pyplot import imshow
from PIL import Image


sym, arg = onnx_mxnet.import_model('NN_V03_01.onnx')
# mx.viz.plot_network(sym, node_attrs={"shape":"oval","fixedsize":"false"})



img = Image.open('out_test/anger/m-daniel-1.png').resize((350, 350))
# # img_ycbcr = img.convert("YCbCr")
# # img_y, img_cb, img_cr = img_ycbcr.split()
test_image = np.array(img)#[np.newaxis, np.newaxis, :, :]

print(test_image.shape)

data_names = [graph_input for graph_input in sym.list_inputs()
                    if graph_input not in arg]

# print(data_names)

mod = mx.mod.Module(symbol=sym, data_names=data_names, context=mx.cpu(), label_names=None)
mod.bind(for_training=False, data_shapes=[(data_names[0],test_image.shape)], label_shapes=None)
mod.set_params(arg_params=arg, aux_params=arg, allow_missing=True, allow_extra=True)

from collections import namedtuple
Batch = namedtuple('Batch', ['data'])
mod.forward(Batch([mx.nd.array(test_image)]))

output_labels = ["anger", "neutral", "scream", "smile"]

output = mod.get_outputs()[0][0].asnumpy().tolist()
# dictionary = dict(zip(output_labels, output))
# print (output)

print(output_labels[output.index(max(output))], ":", max(output))

# print(max(dictionary.values()))

# print(output_labels)
# print (output)
# print(max(output))



# mod.save_checkpoint("super_resolution",1)
#
# image = mx.image.imread('out_test/anger/m-daniel-1.png')
# # plt.imshow(image.asnumpy())
# predictions = mod(image).softmax()


# net = Import["super_resolution-symbol.json", "MXNet"]