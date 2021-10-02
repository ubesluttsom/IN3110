from cv2 import imread
from numba import jit, uint8
from sys import argv
from utils import save_image

def numba_color2gray(inputfile, level=1.0):

  # Read original image from file
  image = imread(inputfile)

  # Define function `f()` for Numba to compile
  @jit(uint8[:,:,:](uint8[:,:,:]), nopython=True)
  def f(image):

    # Greyscale matrix in BGR order, with optional `level`-weighting. If
    # `level` == 0.0, this becomes the identity matrix (which does nothing to
    # the colors when multiplied in); if `level` == 1.0, we get the weights
    # specified in the assignment text: a weighted, normalized, sum when
    # multiplied with a pixel vector.
    gray_matrix = \
        [[0.07*level+(1-level), 0.72*level,           0.21*level          ],
         [0.07*level,           0.72*level+(1-level), 0.21*level          ],
         [0.07*level,           0.72*level,           0.21*level+(1-level)]]

    # Extract height and width of image; create aliases for channels for clarity
    heigth, width, channels = image.shape
    b, g, r = range(channels)

    # Iterate over all x,y-pixels
    for x in range(width):
      for y in range(heigth):
        for c in range(channels):
          # Do the matrix–vector multiplication manually
          image[y,x,c] = image[y,x,b]*gray_matrix[c][b] + \
                         image[y,x,g]*gray_matrix[c][g] + \
                         image[y,x,r]*gray_matrix[c][r]

    return image
  
  # Call optimized function
  image = f(image)

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    if argv[2] != None:
      numba_color2gray(inputfile, float(argv[2]))
    else:
      numba_color2gray(inputfile)
  else:
    print("usage: numba_color2gray.py FILE [0.0-1.0]")
    exit(1)
