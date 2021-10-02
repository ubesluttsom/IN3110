from cv2 import imread
from numpy import array
from sys import argv
from utils import save_image

def numpy_color2gray(inputfile, level=1.0):

  # Read original image from file
  image = imread(inputfile)

  weights = array([[ 0.07, 0.72, 0.21 ]])

  # Greyscale matrix in BGR order, with optional `level`-weighting. If `level`
  # == 0.0, this becomes the identity matrix (which does nothing to the colors
  # when multiplied in); if `level` == 1.0, we get the weights specified in the
  # assignment text: a weighted, normalized, sum when multiplied with a pixel
  # vector.
  gray_matrix = \
      array([[.07*level+(1-level), .72*level,           .21*level          ],
             [.07*level,           .72*level+(1-level), .21*level          ],
             [.07*level,           .72*level,           .21*level+(1-level)]])

  # Do the matrix multiplication. There might be a better way to do this, but
  # this seems pretty efficient. In the `image` and gray_matrix variables 0, 1,
  # and 2 represents the color channels blue, green, and red, respectively.
  image[:,:,0] = (image * gray_matrix[0]).sum(axis=2)
  image[:,:,1] = (image * gray_matrix[1]).sum(axis=2)
  image[:,:,2] = (image * gray_matrix[2]).sum(axis=2)

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    if argv[2] != None:
      numpy_color2gray(inputfile, float(argv[2]))
    else:
      numpy_color2gray(inputfile)
  else:
    print("usage: numpy_color2gray.py FILE [0.0-1.0]")
    exit(1)
