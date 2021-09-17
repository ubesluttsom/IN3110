
class Array:

    def __init__(self, shape, *values):
        """
        
        Initialize an array of 1-dimensionality. Elements can only be of type:
        - int
        - float
        - bool
        
        Make sure that you check that your array actually is an array, which
        means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n
            elements will have shape = (n,).  *values: The values in the array.
            These should all be the same data type. Either numeric or boolean.

        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        
        # Check if the values are of valid type

        if len(shape) not in (1, 2):
            raise ValueError
        if not isinstance(shape, tuple):
            raise ValueError
        for i in shape:
            if not type(i) is int:
                raise ValueError
        for v in values:
            if not type(v) in (int, float, bool):
                raise ValueError
        
        # Optional: If not all values are of same type, all are converted to
        # floats.

        # TODO!

        self.shape = shape
        self.values = values
        
        pass

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        return self.values.__str__()

    def __getitem__ (self, item): # Same as in assignment text example
        """ Returns value of item in array.

            Args :
                item (int) : Index of value to return.

            Returns :
                value : Value of the given item.
        """
        return self.values[item]

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied
        arguments (specific data type or shape), it should return
        NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise
            to this array.

        Returns:
            Array: the sum as a new array.

        """
        
        # check that the method supports the given arguments (check for data
        # type and shape of array)

        # Check if Arrays or scalar
        if type(self) == type(other):   # if both Array

            # Check if values are of same type
            if type(self.values[0]) != type(other.values[0]):
                raise NotImplemented

            # Check if shapes are equal
            for s, o in zip(self.shape, other.shape):
                if s != o:
                    raise NotImplemented

            # Add Array values, create and return new array
            new_array_values = list(self.values)
            for i in range(self.shape[0]):
                new_array_values[i] += other.values[i]
            return Array(self.shape, *new_array_values)
        
        elif not type(other) in (int, float, bool):   # if not scalar
            raise NotImplemented

        else:   # that is, if scalar

            # Add scalar
            new_array_values = list(self.values)
            for i in range(self.shape[0]):
                new_array_values[i] += other
            return Array(self.shape, *new_array_values)

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied
        arguments (specific data type or shape), it should return
        NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise
            to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self + other

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied
        arguments (specific data type or shape), it should return
        NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract
            element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if type(other) in (float, int):
            return self + (- other)
        elif type(other) is Array:
            neg_values = list(other.values)
            for i, v in enumerate(neg_values):
                neg_values[i] = -v
            return self + Array(other.shape, *neg_values)
        else:
            raise NotImplemented

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied
        arguments (specific data type or shape), it should return
        NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted
            from.

        Returns:
            Array: the difference as a new array.

        """

        neg_values = list(self.values)
        for i, v in enumerate(neg_values):
            neg_values[i] = -v

        return Array(self.shape, *neg_values) + other

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied
        arguments (specific data type or shape), it should return
        NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply
            element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """

        # Check if Arrays or scalar
        if type(self) == type(other):   # if both Array

            # Check if values are of same type
            if type(self.values[0]) != type(other.values[0]):
                raise NotImplemented

            # Check if shapes are equal
            for s, o in zip(self.shape, other.shape):
                if s != o:
                    raise NotImplemented

            # Multiply Array values, create and return new array
            new_array_values = list(self.values)
            for i in range(self.shape[0]):
                new_array_values[i] *= other.values[i]
            return Array(self.shape, *new_array_values)
        
        elif type(other) in (int, float, bool):   # if scalar

            # Multiply scalar
            new_array_values = list(self.values)
            for i in range(self.shape[0]):
                new_array_values[i] *= other
            return Array(self.shape, *new_array_values)

        else:
            raise NotImplemented

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied
        arguments (specific data type or shape), it should return
        NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply
            element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False
            otherwise.

        """
        if type(self) == type(other):   # if both Array

            # Check if `values` are of same type
            if type(self.values[0]) != type(other.values[0]):
                return False

            # Check if `shape`s are equal
            for s, o in zip(self.shape, other.shape):
                if s != o:
                    return False

            # Check if `values` are equal
            for s, o in zip(self.values, other.values):
                if s != o:
                    return False

            return True
     
        else:
            return False        

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this
        method should raise ValueError.  If `other` is not an array or a
        number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this
            array.

        Returns:
            Array: An array of booleans with True where the two arrays match
            and False where they do not.  Or if `other` is a number, it returns
            True where the array is equal to the number and False where it is
            not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """

        pass
    

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        
        pass


# TEST AREA

def test_addition():
    a = Array((2,), 1, 1)
    b = Array((2,), 2, 2)
    c = Array((2,), 3, 3)
    d = Array((4,), 3, 3, 6, -2)
    e = Array((4,), 0, 0, -6, -1)
    f = Array((4,), 3, 3, 0, -3)
    assert a + b == c
    assert a + 2 == a + a + a
    assert 2 + a == a + a + a
    assert a + c == a + a + a + a
    assert d + e == f

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

def test_multiplication():
    a = Array((2,), 1, 1)
    b = Array((2,), 2, 2)
    c = Array((2,), 3, 3)
    d = Array((4,), 3, 3, 6, -2)
    e = Array((4,), 0, 0, -6, -1)
    f = Array((4,), 0, 0, -36, 2)
    assert a * 2 == b
    assert 3 * a == c
    assert a * b == b
    assert b * c == a + a + a + a + a + a
    assert d * e == f

test_addition()
test_subtraction()
test_multiplication()
