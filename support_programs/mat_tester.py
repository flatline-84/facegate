import scipy.io

filename = '../data/test_NN.mat'

mat = scipy.io.loadmat(filename)
# print(scipy.io.whosmat(filename))
print(mat)