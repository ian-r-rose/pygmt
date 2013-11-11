'''
flags.py
Recreations of the relevant C enum structures which are used as flags in the GMT C API.
Here they are python dictionaries, but basically serve the same purpose
'''

io_family = { 'dataset': 0 ,
              'textset': 1 ,
              'grid'   : 2 ,
              'cpt'    : 3 ,
              'image'  : 4 ,
              'vector' : 5 ,
              'matrix' : 6 ,
              'coord' : 7 }

io_method = { 'file'      : 0 ,
              'stream'    : 1 ,
              'fdesc'     : 2 ,
              'duplicate' : 3 , 
              'reference' : 4  }

io_approach = { 'via_vector' : 100 ,
                'via_matrix' : 200  }

io_geometry = { 'point'   : 1 ,
                'line'    : 2 ,
                'polygon' : 4 ,
                'plp'     : 7 ,
                'surface' : 8 ,
                'none'    : 16 }

io_index = { 'xlo' : 0 ,
             'xhi' : 1 ,
             'ylo' : 2 ,
             'yhi' : 3 ,
             'zlo' : 4 ,
             'zhi' : 5  }

io_direction = { 'in' :  0 ,
                 'out' : 1 ,
                 'err' : 2  }

io_grid_mode = { 'real'              : 0 ,
                 'all'               : 0 ,
                 'header_only'       : 1 ,
                 'data_only'         : 2 ,
                 'complex_real'      : 4 , 
                 'complex_imag'      : 8 , 
                 'complex_mask'      : 12 , 
                 'no_header'         : 16 ,
                 'row_by_row'        : 32 ,
                 'row_by_row_manual' : 64  }

io_dataset_mode = { 'write_ogr'           : -1 ,
                    'write_set'           :  0 ,
                    'write_table'         :  1 ,
                    'write_segment'       :  2 ,
                    'write_table_segment' :  3  }

io_cpt_mode = { 'cpt'     : 0 ,
                'default' : 2 ,
                'hilo'    : 4  }

module_mode = { 'exist'   : -3 ,
                'purpose' : -2 ,
                'opt'     : -1 ,
                'cmd'     :  0  }

dimensions = { 'x' : 1 ,
               'y' : 2 ,
               'z' : 3  }

io_freg = { 'add_files_if_none' : 1 ,
            'add_files_always'  : 2 ,
            'add_stdio_if_none' : 4 ,
            'add_stdio_always'  : 8 ,
            'add_existing'      : 16 ,
            'add_default'       : 6  }

data_types = { 'char'     : 0,
               'uchar'    : 1,
               'short'    : 2,
               'ushort'   : 3,
               'int'      : 4,
               'uint'     : 5,
               'long'     : 6,
               'ulong'    : 7,
               'float'    : 8,
               'double'   : 9,
               'text'     : 10,
               'datetime' : 11,
               'ntypes'   : 12 }
