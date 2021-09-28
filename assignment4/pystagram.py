import cv2
import numpy
import sys

def numpy_color2gray(inputfile):

  # Read original image from file
  image = cv2.imread(inputfile)

  # Set the normalized weigths, mindful of BGR vs. RGB.
  weights = numpy.array([[ 0.07, 0.72, 0.21 ]])

  # I sum across all channels on every pixel, and I set all channels on each
  # pixel to be this value.
  image[:,:,0] = image[:,:,1] = image[:,:,2] = (image * weights).sum(axis=2)

  save_image(inputfile, image)

def python_color2gray(inputfile):

  # Read original image from file
  image = cv2.imread(inputfile)

  # Extract heigth and width of image; create aliases for channels for clarity.
  heigth, width, channels = image.shape
  b, g, r = range(channels)

  # Iterate over all x,y-pixels using a good ol' fashioned loop.
  for x in range(width):
    for y in range(heigth):
      # Set pixel over all channels to the weighted, normalized, sum.
      image[y,x,:] = image[y,x,b]*0.07 + image[y,x,g]*0.72 + image[y,x,r]*0.21

  save_image(inputfile, image)

def save_image(inputfile, image, suffix="_grayscale"):
  # Convert datatype in numpy array to integers (not floats).
  image = image.astype("uint8")

  # Extract file-extention to tuple: (<base filename>, ".", <file-extention>)
  outputfile = inputfile.rpartition(".")

  # Save image to file with the specified suffix.
  cv2.imwrite(outputfile[0] + suffix + "." + outputfile[2], image)

if __name__ == "__main__":

  if len(sys.argv) > 2:
    inputfile = sys.argv[2]

    if sys.argv[1] == "numpy":
      numpy_color2gray(inputfile)
      exit(0)

    if sys.argv[1] == "python":
      python_color2gray(inputfile)
      exit(0)

  else:
    print("usage: pystagram.py numpy <input image>")
    print("       pystagram.py python <input image>")
    exit(-1)
