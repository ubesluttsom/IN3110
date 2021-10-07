from numpy import array, eye
from instapy.utils import save_image, read_image
from sys import argv

def numpy_filter(wrapper):
  # Return the matrix multiplication.
  return lambda image, filter_matrix=eye(3): image @ filter_matrix.T

def gray(filter_implementation):
  return lambda image, filter_matrix: \
    filter_implementation(
        image,
        filter_matrix=array([[ .07, .72, .21 ],
                             [ .07, .72, .21 ],
                             [ .07, .72, .21 ]]))

def stepless(filter_implementation):
  # Apply optional `level`-weighting. If `level` == 0.0, this becomes the
  # identity matrix (which does nothing to the colors when multiplied in); if
  # `level` == 1.0, we get the weights specified in the assignment text: a
  # weighted, normalized, sum when multiplied with a pixel vector.
  return lambda image, filter_matrix=eye(3), level=1.0: \
    filter_implementation(
        image,
        filter_matrix= \
            filter_matrix * level + array([[1-level,       0,        0],
                                           [       0, 1-level,       0],
                                           [       0,       0, 1-level]]))


@gray
@stepless
@numpy_filter
def numpy_color2gray(image, level=1.0):
  pass

if __name__ == "__main__":
  if len(argv) > 1:
    image = read_image(argv[1])
    if argv[2] != None:
      image = numpy_color2gray(image, float(argv[2]))
    else:
      image = numpy_color2gray(image)
    save_image(argv[1], image, suffix='_grayscale')
  else:
    print("usage: numpy_color2gray.py FILE [0.0-1.0]")
    exit(1)
