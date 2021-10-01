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
                      help='choose the implementation(s). Default: \'numpy\'')
  parser.add_argument('-r', '--runtime', metavar='N',
                      type=int, nargs='?', const=3,
                      help='do runtime statistics, optional N number of runs. '
                           'Default: 3')
  parser.add_argument('-se', '--sepia', metavar='LEVEL',
                      type=float, nargs='?', const=1.0,
                      help='apply sepia filter, optional 0-1 float for '
                           'desired level. Default: 1.0')
  parser.add_argument('-g', '--gray', metavar='LEVEL',
                      type=float, nargs='?', const=1.0,
                      help='apply greyscale filter, optional 0-1 float for '
                           'desired level. Default: 1.0')

  args = parser.parse_args()

  if args.file:

    # If the `runtime` argument is passed, let that function do the rest, and
    # exit. `time()` will run on the entire set of `--implement` arguments
    # passed, i.e. running multiple implementation tests is allowed.

    if args.runtime != None:
      if args.implement:
        timer(args.file, implementations=set(args.implement),
              number=args.runtime, gray=args.gray, sepia=args.sepia)
      else:
        timer(args.file, number=args.runtime, gray=args.gray, sepia=args.sepia)
      exit(0)

    # Else, just do filtering. If no `--implement` argument is passed, use
    # numpy. If several `-i` arguments are passed (which is kinda pointless
    # without `--runtime`, but yeah), the preference is numpy > numba > python.

    if args.gray != None:
      if (not args.implement) or 'numpy' in args.implement:
        numpy_color2gray(args.file, level=args.gray)
      elif 'numba' in args.implement:
        numba_color2gray(args.file, level=args.gray)
      elif 'python' in args.implement:
        python_color2gray(args.file, level=args.gray)

    elif args.sepia != None:
      if (not args.implement) or 'numpy' in args.implement:
        numpy_color2sepia(args.file, level=args.sepia)
      elif 'numba' in args.implement:
        numba_color2sepia(args.file, level=args.sepia)
      elif 'python' in args.implement:
        python_color2sepia(args.file, level=args.sepia)

  exit(0)
