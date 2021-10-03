from instapy.sepia.numpy_color2sepia import numpy_color2sepia as sepia
from instapy.utils import read_image, save_image

def sepia_image(input_filename, output_filename=None):
  image = read_image(input_filename)
  image = sepia(image)
  if output_filename != None:
    save_image(output_filename, image)
  return image
