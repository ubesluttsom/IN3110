from cv2 import imread
from numba import jit, uint16
from sys import argv
from instapy.utils.utils import save_image

def numba_color2sepia(inputfile, level=1.0):

  # Read original image from file
  image = imread(inputfile)
  image = image.astype("uint16")

  # Define function `f()` for Numba to compile
  @jit(uint16[:,:,:](uint16[:,:,:]), nopython=True)
  def f(image):

    # Extract height and width of image; create aliases for channels for clarity
    heigth, width, channels = image.shape
    b, g, r = range(channels)

    # Sepia matrix, in BGR order. Here I've fiddled around with the
    # `level`-weight such that when `level` == 0, the `sepia_matrix` becomes the
    # identity matrix (which does exactly nothing with the colors), and when
    # `level` == 1 it cancels out and becomes the original `sepia_matrix`
    # proposed in the assignment.
    sepia_matrix = \
        [[0.272*level+(1-level), 0.534*level          , 0.131*level          ],
         [0.349*level          , 0.686*level+(1-level), 0.168*level          ],
         [0.393*level          , 0.769*level          , 0.189*level+(1-level)]]

    # Initialize storage of highest color value; for correcting overflowing
    # color values by downscaling all pixel color values.
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
    # expensive operation, as we have to iterate over the entire image again.
    scalar = 255 / max_color
    for x in range(width):
      for y in range(heigth):
        for c in range(channels):
          image[y,x,c] = image[y,x,c] * scalar

    return image
  
  # Call optimized function
  image = f(image)

  save_image(inputfile, image, suffix='_sepia')

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    if argv[2] != None:
      numba_color2sepia(inputfile, float(argv[2]))
    else:
      numba_color2sepia(inputfile)
    exit(0)
  else:
    print("usage: numba_color2sepia.py FILE [0.0-1.0]")
    exit(1)