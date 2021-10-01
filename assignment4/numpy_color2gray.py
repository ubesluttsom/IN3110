from cv2 import imread
from numpy import array
from sys import argv
from utils import save_image

def numpy_color2gray(inputfile, level=1.0):

  # Read original image from file
  image = imread(inputfile)

  # Set the normalized weigths, mindful of BGR vs. RGB.
  weights = array([[ 0.07, 0.72, 0.21 ]])

  # I sum across all channels on every pixel, and I set all channels on each
  # pixel to be this value.
  image[:,:,0] = image[:,:,1] = image[:,:,2] = (image * weights).sum(axis=2)

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    numpy_color2gray(inputfile)
    exit(0)
  else:
    print("usage: numpy_color2gray.py <imagefile>")
    exit(1)
