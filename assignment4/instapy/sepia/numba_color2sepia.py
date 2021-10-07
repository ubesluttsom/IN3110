from instapy.common import uint16, sepia, stepless, python_filter
from numba import jit

@uint16
@sepia
@stepless
@jit(nopython=True)
@python_filter
def numba_color2sepia():
  pass
