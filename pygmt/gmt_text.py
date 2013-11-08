import _gmt_structs
import api
from flags import *
from gmt_base_types import *
import ctypes


class GMT_Text (GMT_Resource):
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
        if input == None:
            if self.out_id == -1:
                raise GMT_Error("Using empty textset as input")

            data = self._session.retrieve_data(self.out_id)
            self.in_id = self._session.register_io(io_family['textset'], io_method['reference'],\
                                              io_geometry['point'], io_direction['in'], None, data)
            self.in_str = '-<'+self._session.encode_id(self.in_id)
            

    def register_output(self, output = None):
        if output == None:
            self.out_id = self._session.register_io(io_family['textset'], io_method['reference'],\
                                               io_geometry['point'], io_direction['out'], None, None)
            self.out_str = '->'+self._session.encode_id(self.out_id)

        elif isinstance(output, str) == True:
            self.out_id = self._session.register_io(io_family['textset'], io_method['file'],\
                                               io_geometry['point'], io_direction['out'], None, output)
            self.out_str = '->'+self._session.encode_id(self.out_id)

        elif isinstance(output, file) == True:
            fd =output.fileno()
            self.out_id = self._session.register_io(io_family['textset'], io_method['fdesc'],\
                                                   io_geometry['point'], io_direction['out'],\
                                                   None, ctypes.pointer(ctypes.c_uint(fd)))
            self.out_str = '->'+self._session.encode_id(self.out_id)

        else:
            raise GMT_Error("Text output format not implemented")



class GMT_Textset:
    
    def __init__(self, session, input):
        self._session = session
         
         # do some type checking
        if isinstance( input, list) == False:
            raise GMT_Error("Textset must be given a list of strings")
        for s in input:
            if isinstance(s, str) == False:
                raise GMT_Error("Textset must be given a list of strings")
        self.string_list = input
   
        #create the textset using the GMT API
        n_records = long(len(input))
        par = (ctypes.c_ulonglong*3)(1,1,n_records)
        self.ptr = self._session.create_data( io_family['textset'], io_geometry['point'],\
                                              0, ctypes.cast(par, ctypes.POINTER(ctypes.c_ulonglong)),\
                                              None, None, 0, -1, None)
        #assign the memory locations to the internal c strings
        ctypes.c_void_p(_gmt_structs.gmt_textset_from_string_list(long(self.ptr.value), input))


    def __del__(self):
        _gmt_structs.free_gmt_textset(self.string_list)
#        self._session.destroy_data( self.ptr )


