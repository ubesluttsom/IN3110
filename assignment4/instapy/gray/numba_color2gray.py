from instapy.common import gray, stepless, python_filter
from numba import jit

@gray
@stepless
@jit(nopython=True)
@python_filter
def numba_color2gray():
  pass
