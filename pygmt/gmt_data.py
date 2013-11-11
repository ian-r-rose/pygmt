import numpy as np
import _gmt_structs
import api
from flags import *
import gmt_base_types

class GMT_Dataset (gmt_base_types.GMT_Resource):
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
            raise api.GMT_Error("Please give filename instead of open file object")


        #if it is a list of numpy arrays, make a GMT_Vector object out of them and register
        elif isinstance(input, list):
            self.vec = GMT_Vector( self._session, input )
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
        elif isinstance(input, gmt_base_types.GMT_Resource) and isinstance(input, GMT_Dataset) == False:
            raise api.GMT_Error("This module does not support GMT resources other than Datasets")

        elif input == None:
            raise api.GMT_Error("Not implemented")

        else:
            raise api.GMT_Error("Unsupported input type") 

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
            raise api.GMT_Error("Please give filename instead of open file object")

        #If it is a GMT_vector, or GMT_grid, throw an error, as we don't want to write that.
        elif isinstance(output, GMT_Vector):
            raise api.GMT_Error("This module does not support output of type GMT_Vector")
        elif isinstance(output, gmt_base_types.GMT_Resource):
            raise api.GMT_Error("This module does not support output to specific GMT Resources")
        else:
            raise api.GMT_Error("Unsupported output type") 
            

class GMT_Vector:
    '''
    Class for storing GMT_VECTOR objects.  In the initializer
    you give it a list of 1D or 2D numpy arrays.  It then constructs
    a GMT_VECTOR which GMT knows how to read.
    '''
    def __init__(self, session, arrays):
        self._session = session
        tmp_arrays = []
        if not isinstance(arrays, list):
            raise api.GMT_Error("Must pass in a list of arrays to GMT_Vector")
        for a in arrays:
            assert( isinstance(a, np.ndarray) )
            if a.shape != arrays[0].shape:
                raise api.GMT_Error("Arrays must be of the same shape")
            if a.ndim != 1 and a.ndim != 2:
                raise api.GMT_Error("Arrays must be 1 or 2 dimensional")

            if a.ndim == 2:
                tmp_arrays.append( a.flatten() )


        if not tmp_arrays:
            self.array_list = arrays
        else:
            self.array_list = arrays

        par = [len(self.array_list),len(self.array_list[0])]
        self.ptr = self._session.create_data( io_family['vector'], io_geometry['point'],\
                                                  0, par, None, None, 0, -1, None)
        _gmt_structs.gmt_vector_from_array_list(self.ptr, self.array_list)
           

    def __del__(self):
#        _gmt_structs.free_gmt_vector(long(self.ptr.value), self.array_list)
        pass

