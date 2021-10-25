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

from instapy.sepia.numpy_color2sepia import numpy_color2sepia
from instapy.gray.numpy_color2gray import numpy_color2gray
from instapy.sepia.numpy_color2sepia import numba_color2sepia
from instapy.gray.numpy_color2gray import numba_color2gray
from instapy.sepia.numpy_color2sepia import python_color2sepia
from instapy.gray.numpy_color2gray import python_color2gray

from instapy.utils import read_image, save_image

def sepia_image(input_filename, output_filename=None, implementation="numpy"):
  image = read_image(input_filename)

  # Would love a switch case, but you know...
  if implementation == "numpy":
    image = numpy_color2sepia(image)
  elif implementation == "numba":
    image = numba_color2sepia(image)
  elif implementation == "python":
    image = python_color2sepia(image)
  else:
    raise ValueError

  if output_filename != None:
    save_image(output_filename, image)
  return image

def grayscale_image(input_filename, output_filename=None, implementation="numpy"):
  image = read_image(input_filename)

  # Would love a switch case, but you know...
  if implementation == "numpy":
    image = numpy_color2gray(image)
  elif implementation == "numba":
    image = numba_color2gray(image)
  elif implementation == "python":
    image = python_color2gray(image)
  else:
    raise ValueError

  if output_filename != None:
    save_image(output_filename, image)
  return image


"""

Its quite obvious that you know what you are doing and know how to code python.
Very good docstrings and commenting on the code.

Good tests, everything seems to work.

As you have said yourself you played around with decorators. Even though they work
and the code looks very neat, it can a bit confusing for someone reading the code.
When the entire function and parameters are defined in decorators. Like this:

@uint16
@sepia
@stepless
@numpy_filter
def numpy_color2sepia():
  pass

Its a great idea to have decorators, so you can chose which "filters" and options you want
to use. But as someone that would want to use this package it would be really confusing to 
find out how to use these functions.

Regarding the functions sepia_image and grayscale_image. My interpretation was that they are
the main functions of the package. And that a potential user would use them for their images.
Example:

import instapy

my_image = instapy.sepia_image("input.jpg", "output.jpg")
# or
my_image = instapy.sepia_image("input.jpg", "output.jpg", "python")


Therefor it would be necessary to be able to choose a implementation, that is the only 
change I would do to this assignment. Even though the assigment doesnt specify to take
implementation as a optional parameter, it has been discussed on mattermost as a "good"
solution. So im going by that.

"""