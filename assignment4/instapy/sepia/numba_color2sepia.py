from instapy.common import uint16, sepia, stepless, python_filter
from numba import jit

@uint16
@sepia
@stepless
@jit(nopython=True)
@python_filter
def numba_color2sepia(image, level=1.0):
  pass

if __name__ == "__main__":

  from instapy.utils import save_image, read_image, uint16, sepia, python_filter
  from sys import argv

  if len(argv) > 1:
    image = read_image(argv[1])
    if argv[2] != None:
      image = numba_color2sepia(image, float(argv[2]))
    else:
      image = numba_color2sepia(image)
    save_image(argv[1], image, suffix='_sepia')
  else:
    print("usage: numba_color2sepia.py FILE <0.0-1.0>")
    exit(1)
