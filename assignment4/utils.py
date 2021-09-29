from cv2 import imwrite, imread
from timeit import timeit

def timer(imagefile,
          implementations=("python",
                           "numpy",
                           "numba"),
          number=10):

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
    print("Timing:", implementation, "on image with shape", shape, "--- width,",
          "height and channels, respectively --- using the `timeit` module ...")

    # Run and time tests
    averages[implementation] = timeit(command, setup=setup, number=number) / number

    # Print results
    print("Average runtime running", implementation,
          "after", number, "runs:", averages[implementation], "s")
  
  for implementation, average in averages:
    # Do stuff ...

def save_image(inputfile, image, suffix="_grayscale"):
  # Convert datatype in numpy array to integers (not floats).
  image = image.astype("uint8")

  # Extract file-extention to tuple: (<base filename>, ".", <file-extention>)
  outputfile = inputfile.rpartition(".")

  # Save image to file with the specified suffix.
  imwrite(outputfile[0] + suffix + "." + outputfile[2], image)
