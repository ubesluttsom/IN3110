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

        # if len(shape) not in (1, 2):
        #     raise ValueError
        if not isinstance(shape, tuple):
            raise ValueError
        for i in shape:
            if not type(i) is int:
                raise ValueError

        # Check if number of elements fit the shape
        elements = 1
        for dimention in shape:
            elements *= dimention
        if len(values) != elements:
            raise ValueError
        else: 
            self.shape = shape

        # Check value types
        value_types = set()
        for v in values:
            if not type(v) in (int, float, bool):
                raise ValueError
            else:
                value_types.add(type(v))
        # If the set of value types contains more than 1 type, convert all
        # values to floating points before setting Array objects values.
        if len(value_types) > 1:
            float_values = list()
            for v in values:
                float_values.append(float(v))
            self.values = float_values
        # Else, keep the value type
        else:
            self.values = values

    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        return self.values.__str__()

    def __getitem__ (self, item):
        """ Returns value of item in array.

            Args :
                item (int) : Index of value to return.

            Returns :
                value : Value of the given item.
        """
        # Not really properly implemeted.
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

        new_values = list()

        # Check if Arrays or scalar
        if type(self) == type(other):   # if both Array

            # # Check if values are of same type
            # if type(self.values[0]) != type(other.values[0]):
            #     raise NotImplemented

            # Check if shapes are equal
            for s, o in zip(self.shape, other.shape):
                if s != o:
                    raise NotImplemented

            # Add Array values, append to new array
            for s, o in zip(self.values, other.values):
                new_values.append(s + o)
        
        elif type(other) in (int, float, bool):   # If scalar

            # Add scalar
            for value in self.values:
                new_values.append(value + other)

        else:
            raise NotImplemented

        return Array(self.shape, *new_values)

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

            # Negate all of `other`s values
            neg_values = list()
            for value in other.values:
                neg_values.append(-value)

            # Return sum of self and the negated values
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

        new_values = list()

        # Check if Arrays or scalar
        if type(self) == type(other):   # if both Array

            # Check if values are of same type
            if type(self.values[0]) != type(other.values[0]):
                raise NotImplemented

            # Check if shapes are equal
            for s, o in zip(self.shape, other.shape):
                if s != o:
                    raise NotImplemented

            # Multiply Array values, and append to new array
            for s, o in zip(self.values, other.values):
                new_values.append(s * o)
        
        elif type(other) in (int, float, bool):   # if scalar

            # Multiply scalar
            for value in self.values:
                new_values.append(value * other)

        else:
            raise NotImplemented

        return Array(self.shape, *new_values)

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
        new_values = list()

        if type(self) == type(other):   # if both Array

            # Check if `shape`s are equal
            for s, o in zip(self.shape, other.shape):
                if s != o:
                    raise ValueError

            # Check if `values` are equal
            new_values = list()
            for s, o in zip(self.values, other.values):
                new_values.append((s == o))

        elif type(other) in (int, float, bool):   # if scalar
            # Check if `values` are equal scalar
            for value in self.values:
                new_values.append((value == other))

        else:
            raise TypeError

        return Array(self.shape, *new_values)
    

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        return min(self.values)   # <-- This is so dumb
