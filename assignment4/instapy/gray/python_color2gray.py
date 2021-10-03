from instapy.utils import save_image, read_image
from sys import argv

def python_color2gray(image, level=1.0):

  # Greyscale matrix in BGR order, with optional `level`-weighting. If `level`
  # == 0.0, this becomes the identity matrix (which does nothing to the colors
  # when multiplied in); if `level` == 1.0, we get the weights specified in the
  # assignment text: a weighted, normalized, sum when multiplied with a pixel
  # vector. I state the `1.0` case explicitly, to minimize miniscule floating
  # point errors; it's important that the row sum is exactly 1, else you will
  # see faint colors in the resulting image.
  if level == 1.0:
    gray_matrix = \
        [0.07, 0.72, 0.21]
  else:
    gray_matrix = \
        [[0.07*level+(1-level), 0.72*level,           0.21*level          ],
         [0.07*level,           0.72*level+(1-level), 0.21*level          ],
         [0.07*level,           0.72*level,           0.21*level+(1-level)]]

  # Extract height and width of image; create aliases for channels for clarity
  heigth, width, channels = image.shape
  b, g, r = range(channels)

  # Again, I define the `1.0` case explicitly to ensure all channels are
  # exactly equal. It's also slightly more efficient in this case, as I don't
  # need the innermost loop, and only need to do one sum per pixel (not three).
  if level == 1.0:
    # Iterate over all x,y-pixels
    for x in range(width):
      for y in range(heigth):
          # Assign all channels to the same sum to get true gray colors, and
          # avoid floating point rounding errors.
          image[y,x,b] = \
          image[y,x,r] = \
          image[y,x,g] = image[y,x,b]*gray_matrix[b] + \
                         image[y,x,g]*gray_matrix[g] + \
                         image[y,x,r]*gray_matrix[r]
  else:
    # Iterate over all x,y-pixels
    for x in range(width):
      for y in range(heigth):
        for c in range(channels):
          # Do the matrix–vector multiplication manually
          image[y,x,c] = image[y,x,b]*gray_matrix[c][b] + \
                         image[y,x,g]*gray_matrix[c][g] + \
                         image[y,x,r]*gray_matrix[c][r]

  return image

if __name__ == "__main__":
  if len(argv) > 1:
    image = read_image(argv[1])
    if argv[2] != None:
      image = python_color2gray(image, float(argv[2]))
    else:
      image = python_color2gray(image)
    save_image(arg[1], image, suffix='_grayscale')
  else:
    print("usage: python_color2gray.py FILE [0.0-1.0]")
    exit(1)
