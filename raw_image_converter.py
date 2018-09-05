import numpy, array, PIL
from PIL import Image
from struct import *
import sys, os, argparse

def convert_img(input_path, output_path, img_name):
    x = 576
    y = 768

    input_path_full = input_path + "/" + img_name 
    rawData = open(input_path_full, 'rb').read()
    imgSize = (y,x)

    print ("Converting file: " + input_path_full)
    # Use the PIL raw decoder to read the data.
    # the 'F;16' informs the raw decoder that we are reading 
    # a little endian, unsigned integer 16 bit data.
    # img = Image.fromstring('L', imgSize, rawData, 'raw', 'F;16')

    img = Image.frombytes('L', imgSize, rawData)#, 'raw', 'F;16')
    
    output_path_full = output_path + "/" + img_name + ".png" 

    img.save(output_path_full)

    print("Saved image: " + output_path_full)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # '--port', action="store", dest="port",type=int, required=True)
    parser.add_argument("--input-folder", action="store", dest="input_fol", type=str, required=True, help="The folder relative to where this program is run that has the images you want to convert")
    parser.add_argument("--output-folder", action="store", dest="output_fol", type=str, required=True, help="The folder relative to where this program is run where the new images will be stored")
    args = parser.parse_args()

    input_folder = args.input_fol
    output_folder = args.output_fol

    # print (input_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".raw"):
            convert_img(input_folder, output_folder, file)
