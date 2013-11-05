import ctypes
import numpy as np
import _gmt_vector
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

class GMT_Textset( GMT_Resource ):
    pass

class GMT_Image( GMT_Resource ):
    pass

class GMT_Grid( GMT_Resource ): 
    '''
    Class for storing id information for gridded data, such as would be
    produced by xyz2grd or surface.  This will be associated with a 
    particular GMT session, so they should not be mixed and matched.
    '''

    def register_input(self, input = None):

        if input == None and self.out_id != -1:
            data = self._session.retrieve_data(self.out_id)
            self.in_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                              io_geometry['surface'], io_direction['in'], None, data)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        elif isinstance(input, str) == True:
            self.out_id = self._session.register_io(io_family['grid'], io_method['file'],\
                                               io_geometry['surface'], io_direction['in'], None, input)
            self.out_str = self._session.encode_id(self.in_id)

        elif isinstance(input, file) == True:
            fd =input.fileno()
            self.out_id = self._session.register_io(io_family['grid'], io_method['fdesc'],\
                                                   io_geometry['surface'], io_direction['out'],\
                                                   None, ctypes.pointer(ctypes.c_uint(fd)))
            self.out_str = '-<'+self._session.encode_id(self.in_id)

        else:
            raise GMT_Error("Grid input format not implemented")
        
    def register_output(self, output = None):

        if output == None:
            self.out_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                               io_geometry['surface'], io_direction['out'], None, None)
            self.out_str = self._session.encode_id(self.out_id)

        elif isinstance(output, str) == True:
            self.out_id = self._session.register_io(io_family['grid'], io_method['file'],\
                                               io_geometry['surface'], io_direction['out'], None, output)
            self.out_str = self._session.encode_id(self.out_id)

        elif isinstance(output, file) == True:
            fd =output.fileno()
            self.out_id = self._session.register_io(io_family['grid'], io_method['fdesc'],\
                                                   io_geometry['surface'], io_direction['out'],\
                                                   None, ctypes.pointer(ctypes.c_uint(fd)))
            self.out_str = '-<'+self._session.encode_id(self.out_id)

        else:
            raise GMT_Error("Grid output format not implemented")


class GMT_Dataset (GMT_Resource):
    '''
    Class for storing id information for a dataset, such as would be
    produced by block* or triangulate.  This will be associated with a 
    particular GMT session, so they should not be mixed and matched.
    '''
    def register_input(self, input = None):
        
        #first check if it is a string.  if so, try to open
        #a file with that name 
        if isinstance(input, str) == True:
            self.in_id = self._session.register_io(io_family['dataset'], io_method['file'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, input)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        #if instead it is a python file object, get the file descriptor
        #number and open with that
        elif isinstance(input, file) == True:
            fd =input.fileno()
            self.in_id = self._session.register_io(io_family['dataset'], io_method['fdesc'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, ctypes.pointer(ctypes.c_uint(fd)))
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        #If it is a GMT_vector, just register that.
        elif isinstance(input, GMT_Vector):
            self.in_id = self._session.register_io(io_family['dataset'], io_method['reference']+io_approach['via_vector'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, input.ptr)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        #if it is a list of numpy arrays, make a GMT_Vector object out of them and register
        elif isinstance(input, list):
            self.vec = GMT_Vector( input )
            self.in_id = self._session.register_io(io_family['dataset'], io_method['reference']+io_approach['via_vector'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, self.vec.ptr)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        #if it is a GMT_dataset, register that
        elif isinstance(input, GMT_Dataset):
            assert( input.out_id != -1 )
            data = self._session.retrieve_data(input.out_id)  # retrieve from
            self.in_id = self._session.register_io(io_family['dataset'], io_method['reference'],\
                                         io_geometry['point'], io_direction['in'],\
                                         None, data)
            self.in_str = '-<'+self._session.encode_id(self.in_id)


        #if it is some other GMT resource, throw an error
        elif isinstance(input, GMT_Resource) and isinstance(input, GMT_Dataset) == False:
            raise GMT_Error("This module does not support GMT resources other than Datasets")

        elif input == None:
            raise GMT_Error("Not implemented")

        else:
            raise GMT_Error("Unsupported input type") 

    def register_output(self, output=None):
        '''
        Determine what kind of output for a module to perform.  It may already have
        specified this via options, in which case this is not necessary.  Where this is
        used is if we need to store an intermediate dataset, such as the output of blockmean
        or triangulate, before writing it to disk.  Here we register that output, come
        up with the id information, and store it in a GMT_Dataset object
        '''
      
        #In this case, GMT will handle the output in memory internally
        if output == None:
            self.out_id = self._session.register_io(io_family['dataset'], io_method['duplicate'],\
                                               io_geometry['point'], io_direction['out'],\
                                               None, None)
            #GMT needs to know that this is binary data so it doesn't try to read a header
            self.out_str = "-bo ->"+self._session.encode_id(self.out_id)

        #check if it is a string.  if so, try to open the file with that 
        elif isinstance(output, str) == True:
            self.out_id = self._session.register_io(io_family['dataset'], io_method['file'],\
                                               io_geometry['point'], io_direction['out'],\
                                               None, output)
            self.out_str = "->"+self._session.encode_id(self.out_id)

        #if instead it is a python file object, get the file descriptor number and open with that
        elif isinstance(output, file) == True:
            fd =input.fileno()
            self.out_id = self._session.register_io(io_family['dataset'], io_method['fdesc'],\
                                               io_geometry['point'], io_direction['out'],\
                                               None, ctypes.pointer(ctypes.c_uint(fd)))
            self.out_str = "->"+self._session.encode_id(self.out_id)

        #If it is a GMT_vector, or GMT_grid, throw an error, as we don't want to write that.
        elif isinstance(output, GMT_Vector):
            raise GMT_Error("This module does not support output of type GMT_Vector")
        elif isinstance(output, GMT_Resource):
            raise GMT_Error("This module does not support output to specific GMT Resources")
        else:
            raise GMT_Error("Unsupported output type") 
            
            


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
            assert( isinstance(a, np.ndarray) )
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


class GMT_Matrix:
    '''
    Class for storing GMT_MATRIX objects. Not working
    '''
    def __init__(self, x,y,array):
        if not isinstance(array, np.ndarray):
            raise GMT_Error("Must pass in a numpy matrix to GMT_Matrix")

        self.ptr = ctypes.c_void_p(_gmt_vector.gmt_matrix_from_array(array, (np.amin(x),np.amax(x),np.amin(y),np.amax(y),0,0)))

    def __del__(self):
        _gmt_vector.free_gmt_matrix(long(self.ptr.value))


