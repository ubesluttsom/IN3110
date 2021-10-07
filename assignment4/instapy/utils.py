from cv2 import imread, imwrite, resize
from timeit import timeit

def read_image(inputfile):
  """ Read image from file.
  
  Args:
      inputputfile (str): Path/filename of input file.

  Returns:
      ndarray: Image read from file, represented in a Numpy array.
  """
  return imread(inputfile)

def save_image(outputfile, image, suffix=None):
  """ Write image to file.
  
  Args:
      outputfile (str): Path/filename of output file.
      image (ndarray): Image to write to file, represented in a Numpy array.
      suffix (str, optional): Suffix to add to output file. Defaults to `None`.
  """
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
  """ Resize image.

  Args:
      image (ndarray): Image to be resized, represented in a Numpy array.
      scale (float): Factor of which to scale image by.

  Returns:
      ndarray: The resized image.
  """
  return resize(image, (int(scale*image.shape[1]), int(scale*image.shape[0])))

def runtime(inputfile,
            implementations=("python",
                             "numpy",
                             "numba"),
            gray=None,
            sepia=None,
            number=3):
  """Measure runtime of image filter implementations.

  Takes the average of multiple runs, usint the `timeit` module, and prints the
  results. If running more than one implementation, it will also print the
  average times normalized to the fastest implementation (usually Numpy).

  Args:
      inputfile (str):
      implementations (str[], optional): Set of implementations to measure, in
           strings.  Defaults to `("python", "numpy", "numba")`
      gray (bool, optional): Apply a gray filter, mutually exclusive with
          `sepia`. Defaults to `None`.
      sepia (bool, optional): Apply a sepia filter, mutually exclusive with
          `gray`. Defaults to `None`.
      number (int): Number of runs to do per implementation. Defaults to 3.:

  Example:
      >>> runtime('rain.jpg', sepia=True, implementations=('numpy', 'python'))
      Timing (with `timeit`): `numpy_color2sepia` on `rain.jpg`: 400 px, 600
      px, 3 channels ...
      Timing (with `timeit`): `python_color2sepia` on `rain.jpg`: 400 px, 600
      px, 3 channels ...
      Average runtimes after 3 runs (each):
        `numpy_color2sepia`: 0.00235 s
        `python_color2sepia`: 4.314514 s
      Normalized to fastest implementation time:
        `numpy_color2sepia`: 1.0
      `python_color2sepia`: 1835.963404 
  """

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
