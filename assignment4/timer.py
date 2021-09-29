import timeit

n = 10

implementation = "pyton_color2gray"
print("Timing:", implementation)
average = timeit.timeit('python_color2gray("rain.jpg")', setup='from python_color2gray import python_color2gray', number=n)
print("Average runtime running", implementation, "after", n, "runs:", average, "s")
print("Timing preformed using: `timeit`")

implementation = "numpy_color2gray"
print("Timing:", implementation)
average = timeit.timeit('numpy_color2gray("rain.jpg")',  setup='from numpy_color2gray import numpy_color2gray'  , number=n)
print("Average runtime running", implementation, "after", n, "runs:", average, "s")
print("Timing preformed using: `timeit`")

implementation = "numba_color2gray"
print("Timing:", implementation)
average = timeit.timeit('numba_color2gray("rain.jpg")',  setup='from numba_color2gray import numba_color2gray'  , number=n)
print("Average runtime running", implementation, "after", n, "runs:", average, "s")
print("Timing preformed using: `timeit`")
