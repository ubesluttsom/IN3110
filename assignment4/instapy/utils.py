from cv2 import imread, imwrite, resize
from timeit import timeit

def read_image(inputfile):
  # Read original image from file
  return imread(inputfile)

def save_image(outputfile, image, suffix=None):
  # Convert datatype in numpy array to 8-bit integers (not 16-bit or floats).
  image = image.astype("uint8")

  # If `suffix` is specified, use `outputfile` as base and add `suffix`
  if suffix != None:

    # Extract file-extension to tuple: (<base filename>, ".", <file-extension>)
    outputfile = outputfile.rpartition(".")

    # Save image to file with the specified suffix.
    imwrite(outputfile[0] + suffix + outputfile[1] + outputfile[2], image)

  # Otherwise, use specified output filename
  else:
    imwrite(outputfile, image)

def resize_image(image, scale):
  return resize(image, (int(scale*image.shape[1]), int(scale*image.shape[0])))

def runtime(inputfile,
            implementations=("python",
                             "numpy",
                             "numba"),
            gray=None,
            sepia=None,
            number=3):

  # Initialise empty dictionary for storage of statistics
  averages = dict()

  # Iterate over the tuple (or other `iterable`) of implementations.
  for implementation in implementations:

    # Level of filter and module name initialized to dummy values.
    level = 1.0
    module = ''

    # Check if `implementation` is valid
    if not implementation in ("python", "numpy", "numba"):
      raise ValueError(f"Implementation '{implementation}' not valid")
      exit(1)
    else:
      if gray != None:
        implementation = f"{implementation}_color2gray"
        level = gray
        module = 'instapy.gray'
      elif sepia != None:
        implementation = f"{implementation}_color2sepia"
        level = sepia
        module = 'instapy.sepia'
      else:  
        raise ValueError("No filter selected for testing")

    # Construct necessary info and parameters
    shape   = read_image(inputfile).shape
    command = f"{implementation}(image, level={level})"
    setup   = f"from {module}.{implementation} import {implementation}; " \
              f"from instapy.utils import read_image; " \
              f"image = read_image('{inputfile}')"

    # Inform user of test start
    print(f"Timing (with `timeit`): `{implementation}` on `{inputfile}`: "
          f"{shape[0]} px, {shape[1]} px, {shape[2]} channels ...")

    # Run and time tests. Place in dictionary of all averages (for stats below)
    averages[implementation] = round(timeit(command,
                                            setup=setup,
                                            number=number
                                            ) / number,
                                     ndigits=6)

  # Print results
  print(f"Average runtimes after {number} runs (each):")
  for implementation, average in averages.items():
    print(f"  `{implementation}`: {averages[implementation]} s")

  # Print execution times normalized to fastest implementation, if more than
  # one implementation is tested
  if len(averages) > 1:
    print("Normalized to fastest implementation time:")
    fastest_implementation_time = min(averages.values())
    for implementation, average in averages.items():
      normalized_average = round(average/fastest_implementation_time, ndigits=6)
      print(f"  `{implementation}`: {normalized_average}")
