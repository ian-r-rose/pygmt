import pygmt
#Not ussually a good idea, but debugging here
from pygmt.api import *
from pygmt.flags import *
from pygmt.gmt_types import *
#An instance of the figure class
#fig = pygmt.GMT_Figure("output.ps", range='g', projection='H7i',verbose='TRUE')
#Doesn't work for now, got some type issues that I can't resolve
#fig.load_data(fig,family,method,geometry,direction,wesn,c_data)

#FOR READABILITY AND EASE ACCESSING THE API DIRECTLY FIGURE OUT WTF IS HAPPENING HERE
family=io_family['vector']
method=io_method['duplicate']
geometry=io_geometry['point']
direction=io_direction['in']
wesn=np.array([])

#So let's start from scratch, and pull some functions from the dylib
#We will keep the Names Identical, the ctypes library will allow us to makes
#the calls as if we were in C, we just don't have access to the include files

GMT_Create_Session = libgmt.GMT_Create_Session
GMT_Register_IO = libgmt.GMT_Register_IO
GMT_Read_Data =libgmt.GMT_Read_Data
GMT_Create_Data=libgmt.GMT_Create_Data

#Start the GMT_session
GMT_Create_Session.restype = GMT_Pointer
session_ptr = GMT_Create_Session("test", 2, 0, None)
#Did it work?
if session_ptr == None:
        raise GMT_Error("Couldn't create session")

#Lets create some vectors in memory 
GMT_Create_Data.argtypes = [GMT_Pointer, ctypes.c_uint,ctypes.c_uint,ctypes.c_ulonglong,ctypes.POINTER(ctypes.c_double),\
                                ctypes.POINTER(ctypes.c_double), ctypes.c_uint,ctypes.C_int,ctypes.c_void_p]
#######UPDATED THE FLAGS

###CAN'T FIGURE OUT HOW TO PASS dim....
V = GMT_Create_Data(session_ptr,family,geometry, 0, dim, None, None, 0, 0, None)

#Read Data
GMT_Read_Data.restype = GMT_Pointer
ARGS=[ALI,FMILY,METHOD, geometry, MODE(NOT USED FOR DATA TABLE), wesn, direction,
GMT_Read_Data.argtypes = [GMT_Pointer, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_unit,\
                                ctypes.c_double, ctypes.c_ubyte, ctypes.c_void_p]
session_data = GMT_Read_Data( session_ptr, family, method, geometry, None, None,direction,None)

#Set the input argument types
GMT_Register_IO.argtypes = [GMT_Pointer, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint,\
                                   ctypes.c_uint, ndpointer(ctypes.c_double),GMT_Pointer]
id = GMT_Register_IO( session_ptr,5, method, geometry,direction, wesn,GMT_DATA )


GMT_DATA=gmt_vector_from_array(data)
my_pointer=GMT_Pointer(ctypes.POINTER
id = GMT_Register_IO( session_ptr, family, method, geometry,direction, wesn,GMT_DATA )
