from python_color2gray import python_color2gray
from numpy_color2gray import numpy_color2gray
from numba_color2gray import numba_color2gray
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

  else:
    print("usage: pystagram.py numpy <input image>")
    print("       pystagram.py python <input image>")
    print("       pystagram.py numba <input image>")
    exit(1)
