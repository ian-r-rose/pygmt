import ctypes
import numpy as np
import _gmt_vector


class GMT_Vector:
    def __init__(self, arrays):
        self.ptr = ctypes.c_void_p(_gmt_vector.gmt_vector_from_array_list(arrays))

    #boo memory leak!
    def __del__(self):
#        _gmt_vector.free_gmt_vector(self.ptr)
        pass


   
