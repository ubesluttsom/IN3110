from cv2 import imread
from sys import argv
from utils import save_image

def python_color2gray(inputfile, level=1.0):

  # Read original image from file
  image = imread(inputfile)

  # Extract heigth and width of image; create aliases for channels for clarity.
  heigth, width, channels = image.shape
  b, g, r = range(channels)

  # Iterate over all x,y-pixels using a good ol' fashioned loop-in-a-loop.
  for x in range(width):
    for y in range(heigth):
      # Set pixel over all channels to the weighted, normalized, sum.
      image[y,x,0] = \
      image[y,x,1] = \
      image[y,x,2] = image[y,x,b]*0.07 + image[y,x,g]*0.72 + image[y,x,r]*0.21

  save_image(inputfile, image)

if __name__ == "__main__":
  if len(argv) > 1:
    inputfile = argv[1]
    python_color2gray(inputfile)
    exit(0)
  else:
    print("usage: python_color2gray.py <imagefile>")
