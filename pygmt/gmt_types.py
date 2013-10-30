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
    you give it a list of 1D or 2D numpy arrays.  It then constructs
    a GMT_VECTOR which GMT knows how to read.
    '''
    def __init__(self, arrays):
        tmp_arrays = []
        if not isinstance(arrays, list):
            raise GMT_Error("Must pass in a list of arrays to GMT_Vector")
        for a in arrays:
            if a.shape != arrays[0].shape:
                raise GMT_Error("Arrays must be of the same shape")
            if a.ndim != 1 and a.ndim != 2:
                raise GMT_Error("Arrays must be 1 or 2 dimensional")

            if a.ndim == 2:
                tmp_arrays.append( a.flatten() )

        if not tmp_arrays:
            self.ptr = ctypes.c_void_p(_gmt_vector.gmt_vector_from_array_list(arrays))
        else:
            self.ptr = ctypes.c_void_p(_gmt_vector.gmt_vector_from_array_list(tmp_arrays))
           

    def __del__(self):
        _gmt_vector.free_gmt_vector(long(self.ptr.value))


class GMT_Grid:
    '''
    Class for storing id information for gridded data, such as would be
    produced by xyz2grd or surface.  This will be associated with a 
    particular GMT session, so they should not be mixed and matched.
    '''
    def __init__(self, id_num, in_str):
        self.id_num = id_num
        self.in_str = in_str

class GMT_Dataset:
    '''
    Class for storing id information for a dataset, such as would be
    produced by block* or triangulate.  This will be associated with a 
    particular GMT session, so they should not be mixed and matched.
    '''
    def __init__(self, id_num, in_str):
        self.id_num = id_num
        self.in_str = in_str

class GMT_Matrix:
    '''
    Class for storing GMT_MATRIX objects.  In the initializer
    '''
    def __init__(self, x,y,array):
        if not isinstance(array, np.ndarray):
            raise GMT_Error("Must pass in a numpy matrix to GMT_Matrix")

        self.ptr = ctypes.c_void_p(_gmt_vector.gmt_matrix_from_array(array, (np.amin(x),np.amax(x),np.amin(y),np.amax(y),0,0)))

    def __del__(self):
        _gmt_vector.free_gmt_matrix(long(self.ptr.value))


