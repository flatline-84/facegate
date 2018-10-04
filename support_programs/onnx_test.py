import onnx
from onnx_tf.backend import prepare
from pprint import pprint

model = onnx.load('../data/test_network.onnx')
tf_rep = prepare(model)

pprint(vars(tf_rep))

# print(tf_rep.predict_net)
# print('-----')
# print(tf_rep.input_dict)
# print('-----')
# print(tf_rep.uninitialized)