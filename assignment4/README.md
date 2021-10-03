# assignment4

## Setup

Using the built-in<sup>[1](#bloat)</sup> python module
[`venv`](https://docs.python.org/3/library/venv.html), create a virtual
environment and activate it, e.g:
```{=bash}
$ python -m venv ./venv
$ source ./venv/bin/activate
```
Install `instapy` with
```{=bash}
$ pip install .
```

## Runtime Reports

Runtime reports can be generated thus:
```{=bash}
$ instapy rain.jpg -g -i python -r              > python_report_color2gray.txt
$ instapy rain.jpg -g -i python numpy -r        > numpy_report_color2gray.txt
$ instapy rain.jpg -g -i python numpy numba -r  > numba_report_color2gray.txt
$ instapy rain.jpg -se -i python -r             > python_report_color2sepia.txt
$ instapy rain.jpg -se -i python numpy -r       > numpy_report_color2sepia.txt
$ instapy rain.jpg -se -i python numpy numba -r > numba_report_color2sepia.txt
```

## TODOs

- [x] Make it a package.
- [ ] Factor out file operations from filter modules. Put them instead in
  `instapy.utils`.
- [ ] Test if `instapy.gray.numba_color2gray` works by just calling
  `instapy.gray.python_color2gray` in function body.
- [x] Change structure to `instapy/utils.py` with `instapy.utils.runtime()`,
  `instapy.utils.read_image()` and `instapy.utils.save_image()`.
- [ ] Create the following functions:
  > Include a function `grayscale_image(input filename, output filename=None)`
  > which returns a numpy (unsigned) integer 3D array of a gray image of input
  > filename. If `output_filename` is supplied, the created image should also
  > be saved to the specified location with the specified name, which returns a
  > numpy (unsigned) integer 3D array of a gray image of `input_filename`.

  > The function `sepia_image(input filename, output filename=None)` should be
  > implemented in the same way as `grayscale_image()`.
- [ ] Create unit test `test_instapy.py` using `pytest`. This can be added
  under `instapy.utils.test_instapy`, maybe?
- [ ] Improve the user interface: implement all arguments listed in assignment.
- [x] Stepless sepia filer.
- [x] Stepless gray filer. (Personal addition.)
- [x] Runtime tracking.
- [ ] Write docstrings to all functions.

---

<sup><a name="bloat">1</a></sup>: As opposed to `virtualenv` or `conda`. Why does this course insist on
bloating my computer with unnecessary installations?
