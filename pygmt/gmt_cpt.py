import _gmt_structs
import api
from flags import *
import gmt_base_types


class GMT_CPT (gmt_base_types.GMT_Resource):
    def register_input(self, input=None):
        #first check if it is a string.  if so, try to open
        #a file with that name 
        if isinstance(input, str) == True:
            ptr = self._session.read_data(io_family['cpt'], io_method['file'],
                                              io_geometry['none'], 0,
                                              None, input, None)
            self.in_id = self._session.register_io(io_family['cpt'], io_method['reference'],\
                                          io_geometry['none'], io_direction['in'],\
                                          None, ptr)
            self.in_str = '-C'+self._session.encode_id(self.in_id)

        elif isinstance(input, file) == True:
            raise api.GMT_Error("Please give filename instead of open file object")

        if input == None:
            if self.out_id == -1:
                raise api.GMT_Error("Using empty cpt as input")

            data = self._session.retrieve_data(self.out_id)
            self.in_id = self._session.register_io(io_family['cpt'], io_method['reference'],\
                                          io_geometry['none'], io_direction['in'],\
                                          None, data)
            self.in_str = '-C'+self._session.encode_id(self.in_id)

        elif isinstance(input, GMT_CPT):
            if input.direction == io_direction['out'] and input.out_id == -1:
                raise api.GMT_Error("Input text empty")
            elif input.direction == io_direction['err']:
                raise api.GMT_Error("Input text empty")
            elif input.direction == io_direction['in']:  #already registered for input
                self.in_id = input.in_id
                self.in_str = input.in_str 
            else:  #registered for output ,reregister as input
                data = self._session.retrieve_data(input.out_id)
                self.in_id = self._session.register_io(io_family['cpt'], io_method['reference'],\
                                                       io_geometry['none'], io_direction['in'],\
                                                       None, data)
                self.in_str = '-C'+self._session.encode_id(self.in_id)

        self.direction = io_direction['in']
            

    def register_output(self, output = None):
        if output == None:
            self.out_id = self._session.register_io(io_family['cpt'], io_method['duplicate'],\
                                               io_geometry['none'], io_direction['out'], None, None)
            self.out_str = '->'+self._session.encode_id(self.out_id)

        elif isinstance(output, str) == True:
            self.out_id = self._session.register_io(io_family['cpt'], io_method['file'],\
                                               io_geometry['none'], io_direction['out'], None, output)
            self.out_str = '->'+self._session.encode_id(self.out_id)

        elif isinstance(output, file) == True:
            raise api.GMT_Error("Please give filename instead of open file object")

        else:
            raise api.GMT_Error("CPT output format not implemented")

        self.direction = io_direction['out']


