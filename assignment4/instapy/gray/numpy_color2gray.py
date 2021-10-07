from instapy.common import gray, stepless, numpy_filter

@gray
@stepless
@numpy_filter
def numpy_color2gray(image, level=1.0):
  pass

if __name__ == "__main__":

  from instapy.utils import save_image, read_image
  from sys import argv

  if len(argv) > 1:
    image = read_image(argv[1])
    if argv[2] != None:
      image = numpy_color2gray(image, level=float(argv[2]))
    else:
      image = numpy_color2gray(image)
    save_image(argv[1], image, suffix='_grayscale')
  else:
    print("usage: numpy_color2gray.py FILE [0.0-1.0]")
    exit(1)
