import ctypes
import flags
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
    _fields_ = [ ('n_columns', ctypes.c_ulonglong),
                 ('n_rows', ctypes.c_ulonglong),
                 ('type' , ctypes.POINTER(ctypes.c_uint)),
                 ('range', ctypes.c_double*2),
                 ('data', ctypes.c_void_p),
                 ('id' , ctypes.c_uint),
                 ('alloc_mode', ctypes.c_uint), #potential for alignment issues here!
                 ('alloc_level', ctypes.c_uint) ]

def gmt_vector_from_array( data ):
    assert(len(data.shape) == 2)
    d = np.require(data, dtype=np.float64, requirements=['A', 'W', 'O']) 
    nrows = d.shape[0]
    ncols = d.shape[1]

    vector = GMT_Vector(ncols, nrows, None, ctypes.c_uint*2, None, 0, 0, 0)
    vector.types = ctypes.POINTER(ctypes.c_uint)*ncols
    vector.data = ctypes.c_void_p*ncols

    data_cols = []
    for i in range(ncols):
      vector.types[i] = flags.data_types['double']
      data_cols.append (np.ctypeslib.as_ctypes(d[:,i]))
      vector.data[i] = data_cols[-1] 

