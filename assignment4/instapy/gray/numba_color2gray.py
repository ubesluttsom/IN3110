from instapy.common import gray, stepless, python_filter
from numba import jit

@gray
@stepless
@jit(nopython=True)
@python_filter
def numba_color2gray(image, level=1.0):
  pass

if __name__ == "__main__":

  from instapy.utils import save_image, read_image
  from sys import argv

  if len(argv) > 2:
    image = read_image(argv[1])
    if argv[2] != None:
      image = numba_color2gray(image, level=float(argv[2]))
    else:
      image = numba_color2gray(image)
    save_image(argv[1], image, suffix='_grayscale')
  else:
    print("usage: numba_color2gray.py FILE <0.0-1.0>")
    exit(1)
