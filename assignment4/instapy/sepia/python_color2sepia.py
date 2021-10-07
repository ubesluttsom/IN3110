from instapy.common import uint16, sepia, stepless, python_filter

@uint16
@sepia
@stepless
@python_filter
def python_color2sepia(image, level=1.0):
  pass

if __name__ == "__main__":

  from instapy.utils import save_image, read_image
  from sys import argv

  if len(argv) > 2:
    image = read_image(argv[1])
    if argv[2] != None:
      image = python_color2sepia(image, level=float(argv[2]))
    else:
      image = python_color2sepia(image)
    save_image(argv[1], image, suffix='_sepia')
  else:
    print("usage: python_color2sepia.py FILE <0.0-1.0>")
    exit(1)
