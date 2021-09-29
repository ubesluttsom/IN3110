from cv2 import imwrite, imread
from timeit import timeit

def timer(imagefile,
          implementations=("python",
                           "numpy",
                           "numba"),
          number=10):

  # Initialise empty dictionary for storage of statistics
  averages = dict()

  # Iterate over the tuple (or other `iterable`) of implementations.
  for implementation in implementations:

    # Check if `implementation` is valid
    if not implementation in ("python", "numpy", "numba"):
      raise ValueError("Implementation must be one of: " +
                       "'python', 'numpy' or 'numba'")
      exit(1)
    else:
      implementation = implementation + "_color2gray"

    # Construct necessary info and parameters
    shape   = imread(imagefile).shape
    command = ''.join([implementation, "('", imagefile, "')"])
    setup   = ' '.join(["from", implementation, "import", implementation])
    print("Timing (with `timeit`): `" + implementation + "` on '" + imagefile +
          "':", shape[0], "px,", shape[1], "px,", shape[2], "channels ...")

    # Run and time tests. Place in dictionary of all averages (for stats below)
    averages[implementation] = round(timeit(command,
                                            setup=setup,
                                            number=number) / number, ndigits=6)

  # Print results
  print("Average runtimes after", number, "runs (each):")
  for implementation, average in averages.items():
    print("  `" + implementation + "`:", averages[implementation], "s")

  # Print execution times normalized to fastest implementation, if more than
  # one implementation is tested
  if len(averages) > 1:
    print("Normalized to fastest implementation time:")
    fastest_implementation_time = min(averages.values())
    for implementation, average in averages.items():
      normalized_average = round(average/fastest_implementation_time, ndigits=6)
      print("  `" + implementation + "`:", normalized_average)

def save_image(inputfile, image, suffix="_grayscale"):
  # Convert datatype in numpy array to integers (not floats).
  image = image.astype("uint8")

  # Extract file-extention to tuple: (<base filename>, ".", <file-extention>)
  outputfile = inputfile.rpartition(".")

  # Save image to file with the specified suffix.
  imwrite(outputfile[0] + suffix + "." + outputfile[2], image)
