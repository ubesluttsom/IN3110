from cv2 import imread
from numba import jit, uint16
from sys import argv
from utils import save_image

def numba_color2sepia(inputfile):

  # Read original image from file
  image = imread(inputfile)
  image = image.astype("uint16")

  # Define function `f()` for Numba to compile
  @jit(uint16[:,:,:](uint16[:,:,:]), nopython=True)
  def f(image):

    # Extract heigth and width of image; create aliases for channels for clarity
    heigth, width, channels = image.shape
    b, g, r = range(channels)

    # Sepia matrix, in BGR order
    sepia_matrix = [[0.272 , 0.534 , 0.131],
                    [0.349 , 0.686 , 0.168],
                    [0.393 , 0.769 , 0.189]]

    # Initialize storage of highest colorvalue; for correcting overflowing
    # colorvalues by downscaling all pixel colorvalues.
    max_color = 0.0

    # Iterate over all x,y-pixels
    for x in range(width):
      for y in range(heigth):
        for c in range(channels):
          image[y,x,c] = image[y,x,b]*sepia_matrix[c][b] + \
                         image[y,x,g]*sepia_matrix[c][g] + \
                         image[y,x,r]*sepia_matrix[c][r]
          max_color = max(max_color, image[y,x,c])

    # Scale all colors such that `max_color` * `scalar` == 255. This is an
    # expensive operation, as we have to itterate over the entire image again.
    scalar = 255 / max_color
    for x in range(width):
      for y in range(heigth):
        for c in range(channels):
          image[y,x,c] = image[y,x,c] * scalar

    return image
  
  # Call optimized function
  image = f(image)

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    numba_color2sepia(inputfile)
    exit(0)
  else:
    print("usage: numba_color2sepia.py <imagefile>")
    exit(1)
