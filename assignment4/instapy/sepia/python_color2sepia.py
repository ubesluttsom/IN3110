from instapy.utils import save_image, read_image
from numpy import empty_like
from sys import argv

def python_color2sepia(image, level=1.0):

  # Convert type to higher bit, to avoid overflow. NB! I'm a bit unsure if I'm
  # allowed to do this operation, considering it's tecnically a Numpy function
  # call? Maybe I should rather put this in the loop below?
  image = image.astype("uint16")

  # Make an `output` variable with same shape as input `image`. Hopefully this
  # is allowed, despite `empty_like` is a Numpy function? Since it's for
  # storage, as the assignmet opens for.
  output = empty_like(image)

  # Extract height and width of image.
  height, width, colors = image.shape

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
  max_color = 255.0

  # Iterate over all x,y-pixels using a good ol' fashioned loop-in-a-loop.
  for x in range(width):
    for y in range(height):
      for n in range(colors):
        # Do the matrix–vector multiplication.
        output[y,x,n] = \
            sum([image[y,x,m]*sepia_matrix[n][m] for m in range(colors)])
        max_color = max(max_color, output[y,x,n])

  # Scale all colors such that `max_color` * `scalar` == 255. This is an
  # expensive operation, as we have to iterate over the entire image again.
  scalar = 255 / max_color
  if scalar != 1.0:
    for x in range(width):
      for y in range(height):
        for c in range(colors):
          output[y,x,c] = output[y,x,c] * scalar

  return output

if __name__ == "__main__":
  if len(argv) > 2:
    image = read_image(argv[1])
    if argv[2] != None:
      image = python_color2sepia(image, float(argv[2]))
    else:
      image = python_color2sepia(image)
    save_image(argv[1], image, suffix='_sepia')
  else:
    print("usage: python_color2sepia.py FILE <0.0-1.0>")
    exit(1)
