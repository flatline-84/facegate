import os
from PIL import Image
import operator
from functools import reduce

def equalize(h):
    
    lut = []

    for b in range(0, len(h), 256):

        # step size
        step = reduce(operator.add, h[b:b+256]) / 255

        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i+b]

    return lut

if __name__ == "__main__":

    im = Image.open("original_no_hist.png")

    # calculate lookup table
    lut = equalize(im.histogram())

    # map image through lookup table
    im = im.point(lut)

    im.save("modified_hist.png")