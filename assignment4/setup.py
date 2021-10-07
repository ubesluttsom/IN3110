#!/usr/bin/env python3

from setuptools import setup

setup(
    name='instapy',
    version='0.1.0',
    author='Martin Mihle Nygaard',
    author_email='martimn@ifi.uio.no',
    description='Image filters in different python implementations — IN3110 Assignment 4',
    url='https://github.uio.no/IN3110/IN3110-martimn/tree/master/assignment4',
    packages=['instapy', 'instapy.gray', 'instapy.sepia'],
    install_requires=['numba', 'numpy', 'opencv-python'],
    scripts=['bin/instapy']
    )

# I have no idea what the assignment text refers to here --- where to put and
# for what use --- :
#
# > Include a function `grayscale_image(input filename, output filename=None)`
# > which returns a numpy (unsigned) integer 3D array of a gray image of
# > `input_filename`. If `output_filename` is supplied, the created image
# > should also be saved to the specified location with the specified name.
# >
# > The function `sepia_image(input filename, output filename=None)` should be
# > implemented in the same way as `grayscale_image()`.
# 
# So I just put them below here. I don't use them for anything.

from instapy.sepia.numpy_color2sepia import numpy_color2sepia as sepia
from instapy.gray.numpy_color2gray import numpy_color2gray as gray
from instapy.utils import read_image, save_image

def sepia_image(input_filename, output_filename=None):
  image = read_image(input_filename)
  image = sepia(image)
  if output_filename != None:
    save_image(output_filename, image)
  return image

def grayscale_image(input_filename, output_filename=None):
  image = read_image(input_filename)
  image = gray(image)
  if output_filename != None:
    save_image(output_filename, image)
  return image
