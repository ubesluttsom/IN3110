# assignment4

## Setup

Using the built-in<sup>[1](#bloat)</sup> python module
[`venv`](https://docs.python.org/3/library/venv.html), create a virtual
environment and activate it, e.g:
```
$ python -m venv ./venv
$ source ./venv/bin/activate
```
Install requirements with
```
$ pip install --requirement requirements.txt
```

## Runtime Reports

Runtime reports can be generated thus:
```{=bash}
$ python instapy.py rain.jpg --gray --implement python --runtime 10 > python_report_color2gray.txt
$ python instapy.py rain.jpg --gray --implement python numpy --runtime 10 > numpy_report_color2gray.txt
$ python instapy.py rain.jpg --gray --implement python numpy numba --runtime 10 > numba_report_color2gray.txt
$ python instapy.py rain.jpg --sepia --implement python --runtime 10 > python_report_color2sepia.txt
$ python instapy.py rain.jpg --sepia --implement python numpy --runtime 10 > numpy_report_color2sepia.txt
$ python instapy.py rain.jpg --sepia --implement python numpy numba --runtime 10 > numba_report_color2sepia.txt
```

---

<sup><a name="bloat">1</a></sup>: As opposed to `virtualenv` or `conda`. Why does this course insist on
bloating my computer with unnecessary installations?
