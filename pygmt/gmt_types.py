import ctypes
import numpy as np
import _gmt_vector

class GMT_Pointer(ctypes.c_void_p):
    '''
    Unusual construct, but this is a type for storing the
    gmt session pointer.  It is exactly the same as the c_void_p
    type, which is just the normal void* in C.  We want to subclass
    this because the Python automatically converts the return
    value of void* to long int.  We'd rather avoid this casting
    and keep it as a c_void_p, and this subclassing accomplishes that.
    Also, kind of nice to work with richer types.
    '''
    pass


class GMT_Error(Exception):
    '''
    Class for a simple GMT error message. Does very little
    '''
    pass

class GMT_Vector:
    '''
    Class for storing GMT_VECTOR objects.  In the initializer
    you give it a list of 1D numpy arrays.  It then constructs
    a GMT_VECTOR which GMT knows how to read.
    '''
    def __init__(self, arrays):
        if not isinstance(arrays, list):
            raise GMT_Error("Must pass in a list of arrays to GMT_Vector")
        for a in arrays:
            if isinstance(a, np.ndarray) == False or a.ndim != 1:
                raise GMT_Error("Arrays must be one-dimensional")

        self.ptr = ctypes.c_void_p(_gmt_vector.gmt_vector_from_array_list(arrays))

    def __del__(self):
        _gmt_vector.free_gmt_vector(long(self.ptr.value))


   
