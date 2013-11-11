from flags import *
import _api


class GMT_Error(Exception):
    '''
    Class for a simple GMT error message. Does very little
    '''
    pass

class GMT_Session:
    '''
    Main class for the "light" wrappers for the GMT API.
    Basically, any function in the GMT API that takes the
    void* API object as its first argument should be replicated
    here.  However, instead of passing the session object
    as an argument, the functions are methods of the GMT_session
    class.  The creation and destruction of the session are
    handled by the constructors and destructors.
 
    We more or less attempt to recreate the same interface as the
    GMT C API, but with Python types where appropriate.
    '''
    def __init__(self, name ="tmp"):
         self.session_ptr = _api.gmt_create_session(name)
      
 
    def __del__(self):
#        _api.gmt_destroy_session(self.session_ptr)
        pass

    def register_io(self, family, method, geometry, direction, wesn, ptr):
        id_num = _api.gmt_register_io(self.session_ptr, family, method, geometry,\
                                    direction, wesn, ptr)
        if id_num == -1:
            raise GMT_Error("Couldn't register IO object")
        return id_num

    def encode_id(self, id_num):
        ret, id_str = _api.gmt_encode_id(self.session_ptr, id_num)
 
        if ret == 1:
            raise GMT_Error("Invalid ID for encoding")
        return id_str

    def retrieve_data(self, id_num):
        ptr = _api.gmt_retrieve_data(self.session_ptr, id_num)
        if ptr == None:
            raise GMT_Error("Could not retrieve data")
        return ptr 

    def create_data(self, family, geometry, mode, par, wesn, inc, registration, pad, ptr):
        new_data_obj = _api.gmt_create_data(self.session_ptr, family, geometry,\
                         mode, par, wesn, inc, registration, pad, ptr)
        if new_data_obj == None:
            raise GMT_Error("Could not create data")
        return new_data_obj

    def destroy_data(self, data):
        ret = _api.gmt_destroy_data(self.session_ptr, data)
        if ret != 0:
            raise GMT_Error("Couldn't destory data, error code %i" % ret)

    def read_data(self,family, method, geometry, mode, wesn, input, ptr):
        data = _api.gmt_read_data(self.session_ptr, family, method, geometry, mode, wesn, input, ptr)
        if data == None:
            raise GMT_Error("Could not read data")
        return data

    def call_module(self, module, args, mode=module_mode['cmd']):
        ret = _api.gmt_call_module(self.session_ptr, module, mode, args)
  
        if ret == -1:
            raise GMT_Error("Problem calling module " + str(module))
   
    def option(self, options):
         ret = _api.gmt_option(self.session_ptr, options)



if __name__ == "__main__":

    sess = GMT_Session("my groovy session")
    sess.call_module('pscoast', '-JH6i -Rg -Glightgray -A500 ->out.ps')
  
