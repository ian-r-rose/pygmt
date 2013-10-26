import numpy as np
import ctypes
from numpy.ctypeslib import ndpointer


#LOAD a bogus test library
#gcc -fPIC -shared -o testlib.dylib print_array_test.c
#create input and output numpy arrays
lib = ctypes.cdll.LoadLibrary('./testlib.dylib')
analyzethis = lib.multiplyarray

#lets make up some data
data=np.ones((10,3),dtype=np.double)
out=np.empty_like(data)
out2=np.empty_like(data)

#get size
nrows = data.shape[0]
ncols = data.shape[1]

#
#make c_types
c_nrows=ctypes.c_int(nrows)
c_ncols=ctypes.c_int(ncols)
c_data=ctypes.c_void_p(data.ctypes.data)
c_out =ctypes.c_void_p(out.ctypes.data)

#NUMPY INPUT
print 'Numpy Input: %s' % data

#passing the function a c_pointer to the 
analyzethis(c_data, c_nrows, c_ncols, c_out)

#NUMPY OUTPUT
print 'Numpy Output %s' % out

print "OK I can pass numpy arrays to C code no problem.\n"

#That was great and all but lets see if we can do it using a C prototype
#that actually takes numpy input
analyzethat =lib.multiplyarray
analyzethat.argtypes = [ndpointer(ctypes.c_double), ctypes.c_int, ctypes.c_int, ndpointer(ctypes.c_double)]
analyzethat(data,nrows,ncols,out2)

#NUMPY OUTPUT
print 'Numpy Output %s' % out2
print 'Practically a python function ...'

import pygmt
#Not ussually a good idea, but debugging here
from pygmt.api import *
from pygmt.flags import *

#An instance of the figure class
#fig = pygmt.GMT_Figure("output.ps", range='g', projection='H7i',verbose='TRUE')
#Doesn't work for now, got some type issues that I can't resolve
#fig.load_data(fig,family,method,geometry,direction,wesn,c_data)

#FOR READABILITY AND EASE ACCESSING THE API DIRECTLY FIGURE OUT WTF IS HAPPENING HERE
family=io_family['dataset']
method=io_method['duplicate']
geometry=io_geometry['text']
direction=io_direction['in']
wesn=None

#So let's start from scratch, and pull some functions from the dylib
GMT_Create_Session = libgmt.GMT_Create_Session
GMT_Register_IO = libgmt.GMT_Register_IO

#Start the GMT_session
GMT_Create_Session.restype = GMT_Pointer
session_ptr = GMT_Create_Session("temp", 2, 0, None)

#Did it work?
if session_ptr == None:
    raise GMT_Error("Couldn't create session")

GMT_Register_IO.argtypes = [GMT_Pointer, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint,\
                                   ctypes.c_uint, ndpointer(ctypes.c_double), ctypes.c_void_p]
