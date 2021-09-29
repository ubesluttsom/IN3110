import timeit

def time(implementations=("python_color2gray",
                          "numpy_color2gray",
                          "numba_color2gray"),
                          imagefile,
                          number=10):

  # Iterate over the tuple (or other iterable) of implementations.
  for implementation in implemenations:

    # Check if `implementation` is valid
    if implementation not in ("python_color2gray",
                              "numpy_color2gray",
                              "numba_color2gray"):
      raise ValueError("Error: implementation must be one of: " +
            "'python_color2gray', 'numpy_color2gray' or 'numba_color2gray'")
      exit(1)

    print("Timing:", implementation, "on image with dimentions", image.shape)
    command = ''.join(implementation, "(", imagefile, ")")
    setup   = ' '.join("from", implementation, "import", "implementation")
    average = timeit.timeit(command, setup=setup, number=number)
    print("Average runtime running", implementation, "after", n, "runs:", average, "s")
    print("Timing preformed using: `timeit`")
