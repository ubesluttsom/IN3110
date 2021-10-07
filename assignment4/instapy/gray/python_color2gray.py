from instapy.utils import save_image, read_image
from numpy import empty_like
from sys import argv

def python_color2gray(image, level=1.0):

  # Make an `output` variable with same shape as input `image`. Hopefully this
  # is allowed, despite `empty_like` is a Numpy function? Since it's for
  # storage, as the assignmet opens for.
  output = empty_like(image)

  # Greyscale matrix in BGR order, with optional `level`-weighting. If `level`
  # == 0.0, this becomes the identity matrix (which does nothing to the colors
  # when multiplied in); if `level` == 1.0, we get the weights specified in the
  # assignment text: a weighted, normalized, sum when multiplied with a pixel
  # vector.
  gray_matrix = \
      [[0.07*level+(1-level), 0.72*level,           0.21*level          ],
       [0.07*level,           0.72*level+(1-level), 0.21*level          ],
       [0.07*level,           0.72*level,           0.21*level+(1-level)]]

  # Extract height and width of image.
  height, width, colors = image.shape

  # Iterate over all x,y-pixels.
  for x in range(width):
    for y in range(height):
      for n in range(colors):
        # Do the matrix–vector multiplication.
        output[y,x,n] = \
            sum([image[y,x,m]*gray_matrix[n][m] for m in range(colors)])

  return output

if __name__ == "__main__":
  if len(argv) > 2:
    image = read_image(argv[1])
    if argv[2] != None:
      image = python_color2gray(image, float(argv[2]))
    else:
      image = python_color2gray(image)
    save_image(argv[1], image, suffix='_grayscale')
  else:
    print("usage: python_color2gray.py FILE <0.0-1.0>")
    exit(1)
