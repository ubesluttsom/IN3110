from instapy.utils import save_image, read_image
from sys import argv

def python_color2sepia(image, level=1.0):

  # Convert type to higher bit, to avoid overflow. NB! I'm a bit unsure if I'm
  # allowed to do this operation, considering it's tecnically a Numpy function
  # call? Maybe I should rather put this in the loop below?
  image = image.astype("uint16")

  # Extract height and width of image; create aliases for channels for clarity.
  heigth, width, channels = image.shape
  b, g, r = range(channels)

  # Sepia matrix, in BGR order. Here I've fiddled around with the `level`-weight
  # such that when `level` == 0, the `sepia_matrix` becomes the identity matrix
  # (which does exactly nothing with the colors), and when `level` == 1 it
  # cancels out and becomes the original `sepia_matrix` proposed in the
  # assignment.
  sepia_matrix = \
      [[0.131*level+(1-level), 0.534*level          , 0.272*level          ],
       [0.168*level          , 0.686*level+(1-level), 0.349*level          ],
       [0.189*level          , 0.769*level          , 0.393*level+(1-level)]]

  # Initialize storage of highest color value; for correcting overflowing
  # color values by downscaling all pixel color values.
  max_color = 0.0

  # Iterate over all x,y-pixels using a good ol' fashioned loop-in-a-loop.
  for x in range(width):
    for y in range(heigth):
      for c in range(channels):
        # Do the matrix–vector multiplication manually
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

if __name__ == "__main__":
  if len(argv) > 1:
    image = read_image(argv[1])
    if argv[2] != None:
      image = python_color2sepia(image, float(argv[2]))
    else:
      image = python_color2sepia(image)
    save_image(argv[1], image, suffix='_sepia')
  else:
    print("usage: python_color2sepia.py FILE [0.0-1.0]")
    exit(1)
