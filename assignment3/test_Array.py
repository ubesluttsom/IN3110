from array import *

# Test basic use of `Array`s `__add__` and `__radd__`
def test_addition():
    a = Array((2,), 1, 1)
    b = Array((2,), 2.0, 2)
    c = Array((2,), 3.0, 3.0)
    d = Array((4,), 3, 3, 6, -2)
    e = Array((4,), 0, 0, -6, -1)
    f = Array((4,), 3, 3, 0, -3)
    g = Array((2,), 4.0, 4.0)
    assert a + b == c
    assert a + 2 == a + a + a
    assert 2 + a == a + a + a
    assert a + c == g
    assert d + e == f

# Test basic use of `Array`s `__sub__` and `__rsub__`
def test_subtraction():
    a = Array((2,), 1, 1)
    b = Array((2,), 2, 2)
    c = Array((2,), 3, 3)
    d = Array((4,), 3, 3, 6, -2)
    e = Array((4,), 0, 0, -6, -1)
    f = Array((4,), 3, 3, 12, -1)
    assert a - b == 0 - a
    assert c - a == b
    assert a - 2 == 0 - a
    assert 2 - a == a
    assert d - e == f

# Test basic use of `Array`s `__mul__` and `__rmul__`
def test_multiplication():
    a = Array((2,), 1.0, 1.0)
    b = Array((2,), 2.0, 2.0)
    c = Array((2,), 3, 3.0)
    d = Array((4,), 3, 3, 6, -2)
    e = Array((4,), 0, 0, -6, -1)
    f = Array((4,), 0, 0, -36, 2)
    assert a * 2 == b
    assert 3 * a == c
    assert a * b == b
    assert b * c == a + a + a + a + a + a
    assert d * e == f

# Test print function `__str__`
def test_print():
    f = Array((4,), 0, 0, -36, 2)
    g = Array((4,), 0.0, 0, -36, 2)
    assert f.__str__() == "(0, 0, -36, 2)"
    assert g.__str__() == "[0.0, 0.0, -36.0, 2.0]"

# Test equality operation `__eq__`
def test_eq():
    a = Array((2,), 1, 1)
    b = Array((2,), 2, 2)
    assert (b - a == a) == True

# Test `is_equal` function
def test_is_equal():
    a = Array((2,), 4, 2)
    b = Array((2,), 4, 2)
    c = Array((2,), True, True)
    d = Array((2,), 4, 768)
    e = Array((2,), True, False)
    assert a.is_equal(b) == c
    assert b.is_equal(a) == c
    assert b.is_equal(d) == e

# Test `min_element` function
def test_min_element(): 
    a = Array((2,), 4, 768)
    b = Array((4,), 3, 3, 0, -3)
    assert a.min_element() == 4
    assert b.min_element() == -3

# Test 2D Array addition with `__add__`
def test_2D_addition():
    a = Array((3,2), 1, 1, 1, 1, 1, 1)
    b = Array((3,2), 2, 2, 2, 2, 2, 2)
    assert a + a == b
    assert a + 1 == b
    assert 1 + a == b
    assert a + b == a + a + a

# Test 2D Array subtraction with `__sub__`
def test_2D_subtraction():
    a = Array((2,2), 2, 3, 1, 1)
    b = Array((2,2), 5, 1, 2, 2)
    c = Array((2,2), -3, 2, -1, -1)
    d = Array((2,2), 0, -1, 1, 1)
    e = Array((2,2), 0, 1, -1, -1)
    assert 2 - a == d
    assert a - 2 == e
    assert a - b == c

def test_2D_multiplication():
    # Oh boy.
    pass

# Test 2D Array equality check with `__eq__`
def test_2D_eq():
    a = Array((2,2), 0, 2, 2, 5)
    b = Array((2,2), 0, 2, 2, 5)
    assert (b == a) == True

# Test `is_equal` method with 2D Arrays
def test_2D_is_equal():
    a = Array((2,3), 4, 2, 1, 1, 1, 1)
    b = Array((2,3), 4, 2, 1, 1, 1, 1)
    c = Array((2,3), True, True, True, True, True, True)
    d = Array((1,2), 4, 0)
    e = Array((1,2), 4, 768)
    f = Array((1,2), True, False)
    assert a.is_equal(b) == c
    assert b.is_equal(a) == c
    assert e.is_equal(d) == f

# Test n-dimentional arrays
def test_nD():
    a = Array((2,3,1), 4, 2, 1, 1, 1, 1)
    b = Array((2,3,1), 4, 2, 1, 1, 1, 1)
    c = Array((2,3,1), 8, 4, 2, 2, 2, 2)
    z = Array((2,3,1), 0, 0, 0, 0, 0, 0)
    assert a == b
    assert a + b == c
    assert a - b == z
    assert c - a - b == z

test_addition()
test_subtraction()
test_multiplication()
test_print()
test_eq()
test_is_equal()
test_min_element()
test_2D_addition()
test_2D_subtraction()
#test_2D_multiplication()
test_2D_eq()
test_2D_is_equal()
test_nD()
