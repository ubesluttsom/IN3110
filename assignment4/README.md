## assignment4

# Instapy

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

## Unit test

To do unit tests of all filter implementations, first install `pytest`, e.g:
```{=bash}
$ pip install pytest
```
Then you can run, and get sample output:
```{=bash}
$ pytest test_instapy.py
============================= test session starts =============================
platform linux -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/martin/uio/in3110/assignment4
collected 6 items

test_instapy.py ......                                                   [100%]

============================== 6 passed in 2.01s ==============================
```
Occasionally, I get fails, but I attribute that to rare rounding errors.

## `instapy` script

Display usage with `instapy --help`.

## Numpy vs. Numba

I quote `reports/numba_report_color2gray.txt` here (for convenience):
> Advantage of using Numpy could be, essentially, free speed up *if* you are
> writing pure Python code anyway. The problem, though, is that it's a bit
> *too* magic, and thereby difficult to debug. Numpy, on the other hand, is
> great *if* you know maths, and are willing to read some documentation. Numba
> and Numpy are, supposedly, fairly compatible (some esoteric functions
> notwithstanding), so *porque no los dos?*

## TODOs

- [ ] Write docstrings for all functions.
  * [x] `instapy.common`
  * [x] `instapy.utils`
  * [ ] `test_instapy.py`

---

<sup><a name="bloat">1</a></sup>: As opposed to `virtualenv` or `conda`. Why
does this course insist on bloating my computer with unnecessary installations?
