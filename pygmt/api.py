from flags import *
import ctypes
from gmt_types import GMT_Pointer, GMT_Error

# import the GMT 5 library.  Must be a shared library.
# Should have a better way of locating it later
libgmt = ctypes.CDLL("libgmt.so")


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
        # set up the wrapper for GMT_Create_Session
        GMT_Create_Session = libgmt.GMT_Create_Session
        GMT_Create_Session.restype = GMT_Pointer

        #create the session
        self.session_ptr = GMT_Create_Session(name, 2, 0, None)
        self.session_name = name
        
        if self.session_ptr == None:
            raise GMT_Error("Couldn't create session")
 
    def __del__(self):
        #clean up the session
#        ret = libgmt.GMT_Destroy_Session(self.session_ptr) 
  
#        if ret == 1:
#            raise GMT_Error("Couldn't destroy session:")
        pass

    def _c_wesn(self, wesn):
        
        if wesn == None: 
            return None
        elif len(wesn) == 4:
            c_wesn = ctypes.c_double * 4  #One for each bound
            for i in range(4):
                c_wesn[i] = wesn[i]
            return ctypes.byref(c_wesn)
        raise GMT_Error("Don't understand the wesn argument")

    def register_io(self, family, method, geometry, direction, wesn, ptr):
        GMT_Register_IO = libgmt.GMT_Register_IO
        GMT_Register_IO.restype = int
        GMT_Register_IO.argtypes = [GMT_Pointer, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint,\
                           ctypes.c_uint, ctypes.POINTER(ctypes.c_double), ctypes.c_void_p]
        id_num = GMT_Register_IO(self.session_ptr, family, method, geometry,\
                                    direction, wesn, ptr)
       
        if id_num == -1:
            raise GMT_Error("Couldn't register IO object")
        return id_num

    def encode_id(self, id_num):
        filename = ctypes.create_string_buffer(16) #need at least 16 bytes for the id string
        ret = libgmt.GMT_Encode_ID(self.session_ptr, filename, id_num)
 
        if ret == 1:
            raise GMT_Error("Invalid ID for encoding")
        return filename.value

    def retrieve_data(self, id_num):
        GMT_Retrieve_Data = libgmt.GMT_Retrieve_Data
        GMT_Retrieve_Data.restype = GMT_Pointer
        GMT_Retrieve_Data.argtypes = [GMT_Pointer, ctypes.c_uint] 
        
        ptr = GMT_Retrieve_Data(self.session_ptr, id_num)

        if ptr == None:
            raise GMT_Error("Couldn't retrieve data")
        return ptr 

    def create_data(self, family, geometry, mode, par, wesn, inc, registration, pad, ptr):
        GMT_Create_Data=libgmt.GMT_Create_Data
        GMT_Create_Data.restype = GMT_Pointer
        GMT_Create_Data.argtypes = [GMT_Pointer, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, \
                                    ctypes.POINTER(ctypes.c_ulong), ctypes.POINTER(ctypes.c_double), \
                                    ctypes.POINTER(ctypes.c_double), ctypes.c_uint, ctypes.c_int, ctypes.c_void_p]
        new_data_obj = GMT_Create_Data(self.session_ptr, family, geometry, mode, par, wesn, inc, registration, pad, ptr)
        if new_data_obj == None:
            raise GMT_Error("Couldn't create data")
        return new_data_obj

    def destroy_data(self, data):
        GMT_Destroy_Data = libgmt.GMT_Destroy_Data
        GMT_Destroy_Data.restype = int
        GMT_Destroy_Data.argtypes = [GMT_Pointer, ctypes.c_void_p]
        
        ret = GMT_Destroy_Data(self.session_ptr, data)
        if ret != 0:
            print ret
            raise GMT_Error("Couldn't destory data")


    def write_data(self, family, method, geometry, mode, wesn, output, data):
        ret = libgmt.GMT_Write_Data(self.session_ptr, family, method, geometry,\
                                    mode, self._c_wesn(wesn), output, data)

    def call_module(self, module, args, mode=module_mode['cmd']):
        ret = libgmt.GMT_Call_Module(self.session_ptr, module, mode, args)
  
        if ret == -1:
            raise GMT_Error("Problem calling module " + str(module))
   
    def option(self, options):
        ret = libgmt.GMT_Option(self.session_ptr, options)




if __name__ == "__main__":

    sess = GMT_Session("my groovy session")
    sess.call_module('pscoast', '-JH6i -Rg -Glightgray -A500 ->out.ps')
  
