#!/usr/bin/python3

from python_color2gray import python_color2gray
from numpy_color2gray import numpy_color2gray
from numba_color2gray import numba_color2gray
from python_color2sepia import python_color2sepia
from numpy_color2sepia import numpy_color2sepia
from numba_color2sepia import numba_color2sepia
from utils import timer
import argparse

if __name__ == "__main__":

  # Initialize the argument parser, and define some arguments
  parser = argparse.ArgumentParser(description="Filter some images.")
  parser.add_argument('file', metavar='FILE', type=str,
                      help='the filename of file to apply filter to')
  parser.add_argument('-i', '--implement',
                      choices=('python', 'numba', 'numpy'),
                      action='extend', type=str, nargs='+',
                      help='choose the implementation(s), default: \'numpy\'')
  parser.add_argument('-r', '--runtime', action='store_true',
                      help='do runtime statistics')
  parser.add_argument('-se', '--sepia', type=float, nargs='?', const=1.0,
                      help='apply sepia filter, optional 0-1 float for '
                           'desired level')
  parser.add_argument('-g', '--gray', action='store_true',
                      help='apply greyscale filter')

  args = parser.parse_args()

  if args.file:

    # If the `runtime` argument is passed, let that function do the rest, and
    # exit. `time()` will run on the entire set of `--implement` arguments
    # passed, i.e. running multiple implementation tests is allowed.

    if args.runtime:
      if args.implement:
        timer(args.file, implementations=set(args.implement),
              gray=args.gray, sepia=args.sepia)
      else:
        timer(args.file, gray=args.gray, sepia=args.sepia)
      exit(0)

    # Else, just do filtering. If no `--implement` argument is passed, use
    # numpy. If several `-i` arguments are passed (which is kinda pointless
    # without `--runtime`, but yeah), the preference is numpy > numba > python.

    if args.gray:
      if (not args.implement) or 'numpy' in args.implement:
        numpy_color2gray(args.file)
      elif 'numba' in args.implement:
        numba_color2gray(args.file)
      elif 'python' in args.implement:
        python_color2gray(args.file)

    elif args.sepia != None:
      if (not args.implement) or 'numpy' in args.implement:
        numpy_color2sepia(args.file, level=args.sepia)
      elif 'numba' in args.implement:
        numba_color2sepia(args.file, level=args.sepia)
      elif 'python' in args.implement:
        python_color2sepia(args.file, level=args.sepia)

  exit(0)
