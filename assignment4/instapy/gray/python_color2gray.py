from cv2 import imread
from sys import argv
from instapy.utils.utils import save_image

def python_color2gray(inputfile, level=1.0):

  # Read original image from file
  image = imread(inputfile)

  # Extract height and width of image; create aliases for channels for clarity.
  heigth, width, channels = image.shape
  b, g, r = range(channels)

  # Greyscale matrix in BGR order, with optional `level`-weighting. If `level`
  # == 0.0, this becomes the identity matrix (which does nothing to the colors
  # when multiplied in); if `level` == 1.0, we get the weights specified in the
  # assignment text: a weighted, normalized, sum when multiplied with a pixel
  # vector. I state the `1.0` case explicitly, to minimize miniscule floating
  # point errors; it's important that the row sum is exactly 1, else you will
  # see faint colors in the resulting image.
  if level == 1.0:
    gray_matrix = \
        [[0.07, 0.72, 0.21],
         [0.07, 0.72, 0.21],
         [0.07, 0.72, 0.21]]
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
          # Assign all channels to the same sum to get true gray colors.
          image[y,x,0] = \
          image[y,x,1] = \
          image[y,x,2] = image[y,x,b]*gray_matrix[c][b] + \
                         image[y,x,g]*gray_matrix[c][g] + \
                         image[y,x,r]*gray_matrix[c][r]
  else:
    # Iterate over all x,y-pixels
    for x in range(width):
      for y in range(heigth):
        for c in range(channels):
          # Do the matrix–vector multiplication manually
          image[y,x,c] = image[y,x,b]*gray_matrix[c][b] + \
                         image[y,x,g]*gray_matrix[c][g] + \
                         image[y,x,r]*gray_matrix[c][r]

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    if argv[2] != None:
      python_color2gray(inputfile, float(argv[2]))
    else:
      python_color2gray(inputfile)
  else:
    print("usage: python_color2gray.py FILE [0.0-1.0]")
