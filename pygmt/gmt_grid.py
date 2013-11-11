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
            if self.direction == io_direction['out'] and self.out_id == -1:
                raise api.GMT_Error("Input grid empty")
            elif self.direction == io_direction['err']:
                raise api.GMT_Error("Input grid empty")
            elif self.direction == io_direction['in']:  #already registered for input
                pass
            else:
                data = self._session.retrieve_data(self.out_id)
                self.in_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                                       io_geometry['surface'], io_direction['in'], None, data)
                self.in_str = '-<'+self._session.encode_id(self.in_id)

        elif isinstance(input, GMT_Grid):
            if input.direction == io_direction['out'] and input.out_id == -1:
                raise api.GMT_Error("Input grid empty")
            elif input.direction == io_direction['err']:
                raise api.GMT_Error("Input grid empty")
            elif input.direction == io_direction['in']:  #already registered for input
                self.in_id = input.in_id
                self.in_str = input.in_str 
            else:  #registered for output ,reregister as input
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

        self.direction = io_direction['in']
        
    def register_output(self, output = None):

        if output == None:
            self.out_id = self._session.register_io(io_family['grid'], io_method['reference'],\
                                               io_geometry['surface'], io_direction['out'], None, None)
            self.out_str = self._session.encode_id(self.out_id)

        elif isinstance(output, str) == True:
            self.out_id = self._session.register_io(io_family['grid'], io_method['file'],\
                                               io_geometry['surface'], io_direction['out'], None, output)
            self.out_str = self._session.encode_id(self.out_id)

        else:
            raise api.GMT_Error("Grid output format not implemented")

        self.direction = io_direction['out']
