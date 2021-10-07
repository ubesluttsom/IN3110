from numpy import array, eye, empty_like

"""Common functionality shared between implementations.

Sorry, I kinda went bananas with decorators. All of the functions defined here
are decorators. When used in combination they makeup all the filter
implementations.

This is practical because it avoids code duplication.

"""

def python_filter(wrapper):
  """Python implementation of image filter.
  Returns a python filter function. Does the pixel calculations in good old
  fashioned loops-in-loops. This should be Numba compatible, and gets decorated
  with `@jit` in Numba implementations.

  Args:
      image (ndarray): Representation of image to filter in a numpy array.
      filter_matrix (ndarray): Matrix of transformation to apply to image.
          Defaults to the identity matrix.

  Returns:
      ndarray: The filtered image.
  """
  def f(image, filter_matrix=eye(3)):
    # Make an `output` variable with same shape as input `image`. Hopefully
    # this is allowed, despite `empty_like` is a Numpy function? Since it's
    # technically for storage, as the assignment opens for.
    output = empty_like(image)

    # ~~Converting `filter_matrix` --- a Numpy ndarray --- to a boring old
    # Python list, as per assignment spec.~~ Hmm. This messes up for Numba.
    # TODO: plz fix.
    #filter_matrix = filter_matrix.tolist()

    # Extract height and width of image.
    height, width, colors = image.shape

    # Initialize storage of highest color value; for correcting overflowing
    # color values by downscaling all pixel color values.
    max_color = 255.0

    # Iterate over all x,y-pixels.
    for x in range(width):
      for y in range(height):
        for n in range(colors):
          # Do the matrix–vector multiplication.
          output[y,x,n] = \
              sum([image[y,x,m]*filter_matrix[n][m] for m in range(colors)])
          max_color = max(max_color, output[y,x,n])

    # Scale all colors such that `max_color` * `scalar` == 255. This is an
    # expensive operation, as we have to iterate over the entire image again.
    scalar = 255 / max_color
    if scalar != 1.0:
      for x in range(width):
        for y in range(height):
          for c in range(colors):
            output[y,x,c] = output[y,x,c] * scalar
    return output
  return f


def numpy_filter(wrapper):
  """Numpy implementation of image filter.

  Returns a numpy filter function. It does a linear transformation on the image
  with the specified filter matrix. Also, it will downscale color values if
  needed, so that the highest possible value is 255.

  Args:
      image (ndarray): Representation of image to filter in a numpy array.
      filter_matrix (ndarray): Matrix of transformation to apply to image.
          Defaults to the identity matrix.

  Returns:
      ndarray: The filtered image.
  """
  def f(image, filter_matrix=eye(3)):
    image = image @ filter_matrix.T
    return image * (255 / max(image.max(), 255.0))
  return f


def gray(filter_implementation):
  """Specify that we want a gray filter matrix.

  Returns a function with a filter matrix variable specified to a gray scale
  transformation. Arguments are passed to the function (a filter
  implementation) decorated with this.

  Args:
      image (ndarray): Representation of image to filter in a numpy array.
      filter_matrix (ndarray): Matrix of transformation to apply to image.
          Defaults to the identity matrix. GETS OVERWRITTEN.
      level (float): Level of filtering, eventually passed to `@stepless`.

  Returns:
      ndarray: Image received from the decorated filter implementation.
  """
  return lambda image, filter_matrix=eye(3), level=1.0: \
    filter_implementation(
        image,
        level=level,
        filter_matrix=array([[ .07, .72, .21 ],
                             [ .07, .72, .21 ],
                             [ .07, .72, .21 ]]))


def sepia(filter_implementation):
  """Specify that we want a sepia filter.

  Returns a function with a filter matrix variable specified to a sepia
  transformation. Arguments are passed to the function (a filter
  implementation) decorated with this.

  Args:
      image (ndarray): Representation of image to filter in a numpy array.
      filter_matrix (ndarray): Matrix of transformation to apply to image.
          Defaults to the identity matrix. GETS OVERWRITTEN.
      level (float): Level of filtering, eventually passed to `@stepless`.

  Returns:
      ndarray: Image received from the decorated filter implementation.
  """
  return lambda image, filter_matrix=eye(3), level=1.0: \
    filter_implementation(
        image,
        level=level,
        filter_matrix=array([[0.131 , 0.534 , 0.272],
                             [0.168 , 0.686 , 0.349],
                             [0.189 , 0.769 , 0.393]]))


def uint16(filter_implementation):
  """Type cast input image to unsigned 16-bit integers.

  This is used to avoid overflow. Arguments are passed to the function (a
  filter implementation) decorated with this.

  NB! I'm a bit unsure if I'm allowed to do this operation, considering it's
  technically a Numpy function call? Should I do this in the innermost loops?

  Args:
      image (ndarray): Representation of image to filter in a numpy array.
          This is cast to `uint16`, and passed to filter implementation.
      filter_matrix (ndarray): Matrix of transformation to apply to image.
          Defaults to the identity matrix.
      level (float): Level of filtering, eventually passed to `@stepless`.

  Returns:
      ndarray: Image received from the decorated filter implementation.
  """
  return lambda image, filter_matrix=eye(3), level=1.0: \
    filter_implementation(
        image.astype('uint16'),
        level=level,
        filter_matrix=filter_matrix)


def stepless(filter_implementation):
  """Specify the degree of image filtering.

  Apply optional `level`-weighting. If `level` == 0.0, this becomes the
  identity matrix (which does nothing to the colors when multiplied in); if
  `level` == 1.0, we get the weights specified in the assignment text: a
  weighted, sum when multiplied with a pixel vector.

  Args:
      image (ndarray): Representation of image to filter in a numpy array.
      filter_matrix (ndarray): Matrix of transformation to apply to image.
          Defaults to the identity matrix.
      level (float): Level of filtering.

  Returns:
      ndarray: Image received from the decorated filter implementation.
  """
  return lambda image, filter_matrix=eye(3), level=1.0: \
    filter_implementation(
        image,
        filter_matrix= \
            filter_matrix * level + array([[1-level,       0,        0],
                                           [       0, 1-level,       0],
                                           [       0,       0, 1-level]]))

