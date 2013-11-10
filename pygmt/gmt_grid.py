import ctypes
import numpy as np
import _gmt_structs
import api
from flags import *
import gmt_base_types


class GMT_Grid( gmt_base_types.GMT_Resource ): 
    '''
    Class for storing id information for gridded data, such as would be
    produced by xyz2grd or surface.  This will be associated with a 
    particular GMT session, so they should not be mixed and matched.
    '''

    def register_input(self, input = None):

        if input == None:
            if input.out_id == -1:
                raise api.GMT_Error("Input grid empty")
            data = self._session.retrieve_data(self.out_id)
            self.in_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                              io_geometry['surface'], io_direction['in'], None, data)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        if isinstance(input, GMT_Grid):
            if input.out_id == -1:
                raise api.GMT_Error("Input grid empty")

            data = self._session.retrieve_data(input.out_id)
            self.in_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                              io_geometry['surface'], io_direction['in'], None, data)
            self.in_str = '-<'+self._session.encode_id(self.in_id)
            

        elif isinstance(input, str) == True:
            ptr = self._session.read_data(io_family['grid'], io_method['file'],
                                              io_geometry['surface'], io_grid_mode['all'],
                                              None, input, None)
            self.in_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                               io_geometry['surface'], io_direction['in'], None, ptr)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        else:
            raise api.GMT_Error("Grid input format not supported")
        
    def register_output(self, output = None):

        if output == None:
            self.out_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                               io_geometry['surface'], io_direction['out'], None, None)
            self.out_str = '-G'+self._session.encode_id(self.out_id)

        elif isinstance(output, str) == True:
            self.out_id = self._session.register_io(io_family['grid'], io_method['file'],\
                                               io_geometry['surface'], io_direction['out'], None, output)
            self.out_str = '-G'+self._session.encode_id(self.out_id)

        else:
            raise api.GMT_Error("Grid output format not implemented")


class GMT_Matrix:
    '''
    Class for storing GMT_MATRIX objects. Not working
    '''
    def __init__(self, x,y,array):
        if not isinstance(array, np.ndarray):
            raise api.GMT_Error("Must pass in a numpy matrix to GMT_Matrix")

        self.ptr = ctypes.c_void_p(_gmt_structs.gmt_matrix_from_array(array, (np.amin(x),np.amax(x),np.amin(y),np.amax(y),0,0)))

    def __del__(self):
        _gmt_structs.free_gmt_matrix(long(self.ptr.value))


