import ctypes
import flags
import api
import numpy as np

class GMT_Univector(ctypes.Union):
    _fields_ = [('uc1', ctypes.POINTER(ctypes.c_ubyte)),
                ('sc1', ctypes.POINTER(ctypes.c_byte)),
                ('ui2', ctypes.POINTER(ctypes.c_ushort)),
                ('si2', ctypes.POINTER(ctypes.c_short)),
                ('ui4', ctypes.POINTER(ctypes.c_uint)),
                ('si4', ctypes.POINTER(ctypes.c_int)),
                ('ui8', ctypes.POINTER(ctypes.c_ulong)),
                ('si8', ctypes.POINTER(ctypes.c_long)),
                ('f4', ctypes.POINTER(ctypes.c_float)),
                ('f8', ctypes.POINTER(ctypes.c_double)) ]

class GMT_Vector(ctypes.Structure):
    _fields_ = [ ('n_columns', ctypes.c_ulong),
                 ('n_rows', ctypes.c_ulong),
                 ('type' , ctypes.POINTER(ctypes.c_uint)),
                 ('range', ctypes.c_double*2) ,
                 ('data', ctypes.POINTER(ctypes.c_void_p)),
    #             ('id' , ctypes.c_uint),
                 ('alloc_mode', ctypes.c_uint), #potential for alignment issues here!
                 ('alloc_level', ctypes.c_uint) ]

def gmt_vector_from_array( vectors ):
    ncols = len(vectors)
    nrows = len(vectors[0])
    for v in vectors:
      assert (len(v) == nrows)


    gmt_vector = GMT_Vector()
    print ctypes.sizeof(gmt_vector)
    gmt_vector.n_columns = ncols
    gmt_vector.n_rows = nrows
    gmt_vector.range = (ctypes.c_double*2)()
    type_ptrs = ((ctypes.c_uint)*ncols)()
    data_ptrs = (ctypes.c_void_p*ncols)()

    for i in range(ncols):
      type_ptrs[i] = flags.data_types['double']
      data_ptrs[i] = ctypes.cast(vectors[i].ctypes.data, ctypes.c_void_p)
    

    gmt_vector.types = ctypes.cast(type_ptrs, ctypes.POINTER(ctypes.c_uint))
    gmt_vector.data = ctypes.cast(data_ptrs, ctypes.POINTER(ctypes.c_void_p))
 
    return gmt_vector

     
