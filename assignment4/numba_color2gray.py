from cv2 import imread
from numba import jit, uint8
from sys import argv
from utils import save_image

def numba_color2gray(inputfile):

  # Read original image from file
  image = imread(inputfile)

  # Define function `f()` for Numba to compile
  @jit(uint8[:,:,:](uint8[:,:,:]), nopython=True)
  def f(image):

    # Extract heigth and width of image; create aliases for channels for clarity
    heigth, width, channels = image.shape
    b, g, r = range(channels)

    # Iterate over all x,y-pixels
    for x in range(width):
      for y in range(heigth):
        # Set pixel over all channels to the weighted, normalized, sum
        image[y,x,:] = image[y,x,b]*0.07 + image[y,x,g]*0.72 + image[y,x,r]*0.21

    return image
  
  # Call optimized function
  image = f(image)

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    numba_color2gray(inputfile)
    exit(0)
  else:
    print("usage: numba_color2gray.py <imagefile>")
    exit(1)
