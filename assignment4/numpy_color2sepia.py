from cv2 import imread
from numpy import array
from sys import argv
from utils import save_image

def numpy_color2sepia(inputfile):

  # Read original image from file
  image = imread(inputfile)
  image = image.astype("uint16")

  # Sepia matrix, in BGR order
  sepia_matrix = array([[0.272 , 0.534 , 0.131],
                        [0.349 , 0.686 , 0.168],
                        [0.393 , 0.769 , 0.189]])

  # Alias, for clarity
  blue, green, red = range(3)

  # Apply matrix on all pixels. There is probably a faster numpy solution than
  # this ... but maths, blergh.
  for color in range(3):
    image[:,:,color] = image[:,:,blue]  * sepia_matrix[color][blue]  + \
                       image[:,:,green] * sepia_matrix[color][green] + \
                       image[:,:,red]   * sepia_matrix[color][red]

  # Scale all colors such that `max_color` * `scalar` == 255.
  max_color = image.max()
  scalar = 255 / max_color
  image = image * scalar

  save_image(inputfile, image, suffix='_sepia')

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    numpy_color2sepia(inputfile)
    exit(0)
  else:
    print("usage: numpy_color2gray.py <imagefile>")
    exit(1)
