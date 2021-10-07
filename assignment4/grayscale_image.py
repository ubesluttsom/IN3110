from instapy.gray.numpy_color2gray import numpy_color2gray as gray
from instapy.utils import read_image, save_image

def grayscale_image(input_filename, output_filename=None):
  image = read_image(input_filename)
  image = gray(image)
  if output_filename != None:
    save_image(output_filename, image)
  return image
