import _gmt_vector
import gmt_types
import api
from flags import *
import ctypes


class GMT_Text (gmt_types.GMT_Resource):
    def register_input(self, input=None):
        #first check if it is a string.  if so, try to open
        #a file with that name 
        if isinstance(input, str) == True:
            self.in_id = self._session.register_io(io_family['textset'], io_method['file'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, input)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        #if instead it is a python file object, get the file descriptor
        #number and open with that
        elif isinstance(input, file) == True:
            fd =input.fileno()
            self.in_id = self._session.register_io(io_family['textset'], io_method['fdesc'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, ctypes.pointer(ctypes.c_uint(fd)))
            self.in_str = '-<'+self._session.encode_id(self.in_id)

        #if it is a list of strings, make a GMT_Textset object and register it
        elif isinstance(input, list):
            self.textset = GMT_Textset(self._session, input)
            self.in_id = self._session.register_io(io_family['textset'], io_method['reference'],\
                                          io_geometry['point'], io_direction['in'],\
                                          None, self.textset.ptr)
            self.in_str = '-<'+self._session.encode_id(self.in_id)

class GMT_Textset:
    
    def __init__(self, session, input):
        self._session = session
         
         # do some type checking
        if isinstance( input, list) == False:
            raise gmt_types.GMT_Error("Textset must be given a list of strings")
        for s in input:
            if isinstance(s, str) == False:
                raise gmt_types.GMT_Error("Textset must be given a list of strings")
        self.string_list = input
   
        #create the textset using the GMT API
        n_records = long(len(input))
        par = (ctypes.c_ulong*3)(1,1,n_records)
        self.ptr = self._session.create_data( io_family['textset'], io_geometry['point'],\
                                              0, ctypes.cast(par, ctypes.POINTER(ctypes.c_ulong)),\
                                              None, None, 0, -1, None)
        #assign the memory locations to the internal c strings
        ctypes.c_void_p(_gmt_vector.gmt_textset_from_string_list(long(self.ptr.value), input))


    def __del__(self):
        _gmt_vector.free_gmt_textset(self.string_list)
#        self._session.destroy_data( self.ptr )


