#!/usr/bin/python3

from python_color2gray import python_color2gray
from numpy_color2gray import numpy_color2gray
from numba_color2gray import numba_color2gray
from utils import timer
import sys

if __name__ == "__main__":

  if len(sys.argv) > 2:
    inputfile = sys.argv[2]

    if sys.argv[1] == "numpy":
      numpy_color2gray(inputfile)
      exit(0)

    if sys.argv[1] == "python":
      python_color2gray(inputfile)
      exit(0)

    if sys.argv[1] == "numba":
      numba_color2gray(inputfile)
      exit(0)

    if sys.argv[1] == "timer":
      if len(sys.argv) > 3:
          timer(inputfile, implementations=sys.argv[3].split(' '))
      else:
        timer(inputfile)
      exit(0)

  print("usage: instapy <python|numpy|numba> <image>")
  print("       instapy timer <image> [python] [numpy] [numba]")
  exit(1)
