import ctypes
import numpy as np
import api
from flags import *

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

class GMT_Resource:
    '''
    Abstract base class for GMT resources, defining the
    interface.  You should not need to deal directly with
    this class, it does very little.
    '''
    def __init__(self, session):
        self.in_id = -1
        self.in_str = ''
        self.out_id = -1
        self.out_str = ''
        assert( isinstance(session, api.GMT_Session) )
        self._session = session

    def register_input(self, input = None):
        raise GMT_Error("Base class method not implemented")

    def register_output(self, output = None):
        raise GMT_Error("Base class method not implemented")

