#!/usr/bin/env python3

from python_color2gray import python_color2gray
from numpy_color2gray import numpy_color2gray
from numba_color2gray import numba_color2gray
from python_color2sepia import python_color2sepia
from numpy_color2sepia import numpy_color2sepia
from numba_color2sepia import numba_color2sepia
from utils import timer
import argparse

if __name__ == "__main__":

  # Initialize the argument parser, and define some arguments.
  parser = argparse.ArgumentParser(description="Filter some images.")

  # Providing a filename is mandatory, a «positional argument». If not
  # provided, usage information is printed.
  parser.add_argument('file', metavar='FILE',
                      action='extend', type=str, nargs='+',
                      help='the filename(s) of file(s) to apply filter to')

  # Add argument for which implementation to use. Multiple values are allowed,
  # and constructive for testing runtime.
  parser.add_argument('-i', '--implement',
                      choices=('python', 'numba', 'numpy'),
                      action='extend', type=str, nargs='+',
                      help='choose the implementation(s), otherwise use '
                           '\'numpy\'')

  # Add argument for testing runtime.
  parser.add_argument('-r', '--runtime', metavar='N',
                      type=int, nargs='?', const=3,
                      help='do runtime statistics, optional N number of runs,'
                           ' default to 3')

  # Add a mutually exclusive group for filters; you can only apply one filter
  # at a time. Print error message if attempted.
  filters = parser.add_mutually_exclusive_group()
  filters.add_argument('-se', '--sepia', metavar='float',
                       type=float, nargs='?', const=1.0,
                       help='apply sepia filter, optional 0-1 float for '
                            'desired level; where 0 is no filter, and 1.0 is '
                            'max filtering')
  filters.add_argument('-g', '--gray', metavar='float',
                       type=float, nargs='?', const=1.0,
                       help='apply greyscale filter, optional 0-1 float for '
                            'desired level; where 0 is no filter, and 1.0 is '
                            'max filtering')

  # Parse the command line arguments, according to the rules defined above.
  args = parser.parse_args()

  for file in args.file:

    # If the `runtime` argument is passed, let that function do the rest, and
    # exit. `time()` will run on the entire set of `--implement` arguments
    # passed, i.e. running multiple implementation tests is allowed.

    if args.runtime != None:
      if args.implement:
        timer(file, implementations=set(args.implement),
              number=args.runtime, gray=args.gray, sepia=args.sepia)
      else:
        timer(file, number=args.runtime, gray=args.gray,
              sepia=args.sepia)

    # Else, just do filtering. If no `--implement` argument is passed, use
    # numpy. If several `-i` arguments are passed (which is kinda pointless
    # without `--runtime`, but yeah), the preference is numpy > numba > python.

    elif args.gray != None:

      # Though the results of filter levels higher than 1.0 or levels lower
      # than 0.0 look entertaining, we'll take the boring route of prohibiting
      # such values.
      args.gray = min([1.0, args.gray])
      args.gray = max([0.0, args.gray])

      if (not args.implement) or 'numpy' in args.implement:
        numpy_color2gray(file, level=args.gray)
      elif 'numba' in args.implement:
        numba_color2gray(file, level=args.gray)
      elif 'python' in args.implement:
        python_color2gray(file, level=args.gray)

    elif args.sepia != None:

      # Same as the greyscale-filter above: limit the filter level to the
      # interval [0.0, 1.0].
      args.sepia = min([1.0, args.sepia])
      args.sepia = max([0.0, args.sepia])

      if (not args.implement) or 'numpy' in args.implement:
        numpy_color2sepia(file, level=args.sepia)
      elif 'numba' in args.implement:
        numba_color2sepia(file, level=args.sepia)
      elif 'python' in args.implement:
        python_color2sepia(file, level=args.sepia)
