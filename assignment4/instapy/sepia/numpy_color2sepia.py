from numpy import array, tensordot
from instapy.utils import save_image, read_image
from sys import argv

def numpy_color2sepia(image, level=1.0):

  # Convert type to higher bit, to avoid overflow.
  image = image.astype("uint16")

  # Sepia matrix, in BGR order. Here I've fiddled around with the `level`-weight
  # such that when `level` == 0, the `sepia_matrix` becomes the identity matrix
  # (which does exactly nothing with the colors), and when `level` == 1 it
  # cancels out and becomes the original `sepia_matrix` proposed in the
  # assignment.
  sepia_matrix = array([[0.131 , 0.534 , 0.272],
                        [0.168 , 0.686 , 0.349],
                        [0.189 , 0.769 , 0.393]])
  if level != 1.0:
    sepia_matrix = sepia_matrix * level + array([[1-level,       0,       0],
                                                [       0, 1-level,       0],
                                                [       0,       0, 1-level]])

  # Alias, for clarity
  blue, green, red = range(3)

  # Apply matrix on all pixels. There is probably a faster numpy solution than
  # this ... but maths, blergh.
  for color in range(3):
    image[:,:,color] = image[:,:,blue ] * sepia_matrix[color][blue ] + \
                       image[:,:,green] * sepia_matrix[color][green] + \
                       image[:,:,red  ] * sepia_matrix[color][red  ]

  # Scale all colors such that `max_color` * `scalar` == 255.
  max_color = image.max()
  scalar = 255 / max_color

  return image * scalar

if __name__ == "__main__":
  if len(argv) > 1:
    image = read_image(argv[1])
    if argv[2] != None:
      image = numpy_color2sepia(image, float(argv[2]))
    else:
      image = numpy_color2sepia(image)
    save_image(argv[1], image, suffix='_sepia')
  else:
    print("usage: numpy_color2sepia.py FILE [0.0-1.0]")
    exit(1)
