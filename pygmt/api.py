from flags import *
import ctypes

# import the GMT 5 library.  Must be a shared library.
# Should have a better way of locating it later
libgmt = ctypes.CDLL("libgmt.so")

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
        ret = libgmt.GMT_Destroy_Session(self.session_ptr) 
  
        if ret == 1:
            raise GMT_Error("Couldn't destroy session:")

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
        id = libgmt.GMT_Register_IO(self.session_ptr, family, method, geometry,\
                                    direction, self._c_wesn(wesn), ptr)
       
        if id == -1:
            raise GMT_Error("Couldn't register IO object")
        return id

    def encode_id(self, id):
        filename = ctypes.create_string_buffer(16) #need at least 16 bytes for the id string
        ret = libgmt.GMT_Encode_ID(self.session_ptr, filename, id)
 
        if ret == 1:
            raise GMT_Error("Invalid ID for encoding")
        return filename.value

    def retrieve_data(self, id):
        GMT_Retrieve_Data = libgmt.GMT_Retrieve_Data
        GMT_Retrieve_Data.restype = GMT_Pointer
        
        ptr = GMT_Retrieve_Data(self.session_ptr, id)

        if ptr == None:
            raise GMT_Error("Couldn't retrieve data")
        return ptr 

    def read_data(self, family, method, geometry, mode, wesn, input, ptr=None):
        data = libgmt.GMT_Read_Data(self.session_ptr, family, method, geometry, \
                                   mode, self._c_wesn(wesn), input, ptr)
        
        if data == None:
            raise GMT_Error("Couldn't read data")
        return data

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
  
