from numpy import array, array_equal, allclose, random, matmul
# Some of the module names are a bit unwieldy (as per assignment
# specification), so I alias them.
from instapy.gray.python_color2gray   import python_color2gray  as gray_python
from instapy.gray.numpy_color2gray    import numpy_color2gray   as gray_numpy
from instapy.gray.numba_color2gray    import numba_color2gray   as gray_numba
from instapy.sepia.python_color2sepia import python_color2sepia as sepia_python
from instapy.sepia.numpy_color2sepia  import numpy_color2sepia  as sepia_numpy
from instapy.sepia.numba_color2sepia  import numba_color2sepia  as sepia_numba

def generate_image(width=200, height=200):
  if width < 0 or height < 0:
    raise ValueError(f"Negative dimensions given: '{width}'x'{height}'")
  return random.randint(0, high=255, size=(height, width, 3)).astype('uint8')

def generic_tester(
    image,
    filter_implementation,
    filter_type,
    N=100,
    verbose=False):

  # Apply filter implementation we'd like to test to a copy of the image.
  filtered = image.copy()
  filtered = filter_implementation(filtered, level=1.0)

  # Convert to higher bits
  image    = image.astype('uint16')
  filtered = filtered.astype('uint16')

  if filter_type == 'gray':
    filter_matrix = array([[0.07, 0.72, 0.21],
                           [0.07, 0.72, 0.21],
                           [0.07, 0.72, 0.21]])
    scalars = array([[ 1.0, 1.0, 1.0 ]])

  elif filter_type == 'sepia':
    filter_matrix = array([[0.131 , 0.534 , 0.272],
                           [0.168 , 0.686 , 0.349],
                           [0.189 , 0.769 , 0.393]])
  else:
    raise ValueError("`filter_type` argument must be in {'gray', 'sepia'}")

  # Assert `N` number of random pixels
  for i in range(N):

    # Choose random pixel
    x = random.randint(0, high=image.shape[1])
    y = random.randint(0, high=image.shape[0])

    # Calculate expected pixel based on chosen filter matrix. Scale the pixel
    # same as we do in sepia filtering functions, `scalar` == 1 in the grey
    # filtering case.
    expected_pixel = matmul(image[y,x,:],
                            filter_matrix.transpose())

    # Create variable for filter implementation's pixel
    filtered_pixel = filtered[y,x,:]

    # Check if color values all are within ±5 of each other. I figure this is a
    # reasonable rounding tolerance.
    try:
      assert allclose(expected_pixel * scalars, filtered_pixel, atol=5)

    # If `scalars` are not defined yet, be forgiving ONCE and store the
    # scaling factor. If the next pixels checked (next loop iteration) are
    # not also scaled by the same amount, finally raise the exception.
    except NameError: 
      scalars = (filtered_pixel / expected_pixel)
      # Why do it this way? The problem is that we need to calculate the matrix
      # multiplication for the ENTIRE image to find the right scalars, which is
      # inefficient. What I do instead, is to check that all the pixels in the
      # filtered image is scaled by the same amount.

def test_gray_python(image=None, N=100, verbose=False):
  if image == None:
    image = generate_image()
  return generic_tester(image, gray_python, 'gray', N=N, verbose=verbose)

def test_gray_numpy(image=None, N=100, verbose=False):
  if image == None:
    image = generate_image()
  return generic_tester(image, gray_numpy, 'gray', N=N, verbose=verbose)

def test_gray_numba(image=None, N=100, verbose=False):
  if image == None:
    image = generate_image()
  return generic_tester(image, gray_numba, 'gray', N=N, verbose=verbose)

def test_sepia_python(image=None, N=100, verbose=False):
  if image == None:
    image = generate_image()
  return generic_tester(image, sepia_python, 'sepia', N=N, verbose=verbose)

def test_sepia_numpy(image=None, N=100, verbose=False):
  if image == None:
    image = generate_image()
  return generic_tester(image, sepia_numpy, 'sepia', N=N, verbose=verbose)

def test_sepia_numba(image=None, N=100, verbose=False):
  if image == None:
    image = generate_image()
  return generic_tester(image, sepia_numba, 'sepia', N=N, verbose=verbose)
