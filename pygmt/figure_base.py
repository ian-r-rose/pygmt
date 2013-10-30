import api
import gmt_types
from flags import *
import numpy as np
import ctypes


class GMT_Figure_base:
 
    def __init__(self, ps_file, figure_range, projection, verbose=False):
        '''
        Initialize a GMT figure.  Sets up the GMT session,
        gets the range and projection types, and writes the
        header to the postscript file.
        '''

        self._gmt_session = api.GMT_Session(ps_file+" session")

        #set some universal GMT flags for this figure
        self.ps_file = ps_file
        self.ps_output = '->>'+ps_file
        self.ko_opt = '-O -K'
        self.range_opt = '-R'+figure_range
        self.proj_opt = '-J'+projection

        #dummy call to psxy to write the header of the postscript file
        open_options = ' '.join([self.proj_opt, self.range_opt, '-T -K ->%s'%self.ps_file])
        self._gmt_session.call_module('psxy',  open_options)

        #whether to output the GMT calls
        self.verbose = verbose
        if verbose == True:
            self.ko_opt = self.ko_opt + ' -V'

    def close(self):
        '''
        Close out the figure.  Writes the postscript trailer
        in the figure file.
        '''
        #dummy call to psxy
        close_options = ' '.join([self.proj_opt, self.range_opt, '-T -O', self.ps_output])
        self._gmt_session.call_module('psxy', close_options)

    def _print_call(self, str):
        '''
        Debug output for printing the options given to GMT modules
        '''
        if self.verbose == True:
            print(str)

    def _register_input(self, input):
        '''
        Determine what kind of input has been given to a module,
        register it, and return the id_num and id_str to which it corresponds
        '''

        id_num = -1
        in_str = ""

        #first check if it is a string.  if so, try to open
        #the file with that 
        if isinstance(input, str) == True:
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['file'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, input)
            in_str = '-<'+self._gmt_session.encode_id(id_num)
        #if instead it is a python file object, get the file descriptor
        #number and open with that
        elif isinstance(input, file) == True:
            fd =input.fileno()
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['fdesc'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, ctypes.pointer(ctypes.c_uint(fd)))
            in_str = '-<'+self._gmt_session.encode_id(id_num)

        #If it is a GMT_vector, register that.
        elif isinstance(input, gmt_types.GMT_Vector):
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['reference']+io_approach['via_vector'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, input.ptr)
            in_str = '-<'+self._gmt_session.encode_id(id_num)

        #if it is a GMT_dataset, register that
        elif isinstance(input, gmt_types.GMT_Dataset):
            data = self._gmt_session.retrieve_data(input.id_num)
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['reference'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, data)
            in_str = '-<'+self._gmt_session.encode_id(id_num)

        #if it is a GMT_grd
        elif isinstance(input, gmt_types.GMT_Grid):
            raise gmt_types.GMT_Error("This module does not support input of type GMT_Grid")

        else:
            raise gmt_types.GMT_Error("Unsupported input type") 
            
        return id_num, in_str

    def _register_output(self, output=None):
        '''
        Determine what kind of output for a module to perform.  It may already have
        specified this via options, in which case this is not necessary.  Where this is
        used is if we need to store an intermediate dataset, such as the output of blockmean
        or triangulate, before writing it to disk.  Here we register that output, come
        up with the id information, and store it in a GMT_Dataset object
        '''

        id_num = -1
        out_str = ""
      
        #In this case, GMT will handle the output in memory internally
        if output == None:
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['duplicate'],\
                                               io_geometry['point'], io_direction['out'],\
                                               None, None)
            #GMT needs to know that this is binary data so it doesn't try to read a header
            out_str = "-bo ->"+self._gmt_session.encode_id(id_num)

        #check if it is a string.  if so, try to open the file with that 
        elif isinstance(output, str) == True:
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['file'],\
                                               io_geometry['point'], io_direction['out'],\
                                               None, output)
            out_str = "->"+self._gmt_session.encode_id(id_num)

        #if instead it is a python file object, get the file descriptor number and open with that
        elif isinstance(output, file) == True:
            fd =input.fileno()
            id_num = self._gmt_session.register_io(io_family['dataset'], io_method['fdesc'],\
                                               io_geometry['point'], io_direction['out'],\
                                               None, ctypes.pointer(ctypes.c_uint(fd)))
            out_str = "->"+self._gmt_session.encode_id(id_num)

        #If it is a GMT_vector, or GMT_grid, throw an error, as we don't want to write that.
        elif isinstance(output, gmt_types.GMT_Vector):
            raise gmt_types.GMT_Error("This module does not support output of type GMT_Vector")
        elif isinstance(output, gmt_types.GMT_Grid):
            raise gmt_types.GMT_Error("This module does not support output of type GMT_Grid")

        else:
            raise gmt_types.GMT_Error("Unsupported output type") 
            
        return id_num, out_str

    def _grid_data(self, module, options, input):
        
        #first register the input
        in_id, in_str = self._register_input(input)

        #register the output direction for the memory location of the gridded data
        out_id = self._gmt_session.register_io(io_family['grid'], io_method['reference'],\
                                               io_geometry['surface'], io_direction['out'], None, None)
        out_str = self._gmt_session.encode_id(out_id)

        #do the module call, either surface or xyz2grd
        grid_opts = ' '.join([in_str, '-G'+out_str, options])
        self._gmt_session.call_module(module, grid_opts)

        #now prepare the gridded data for passing on to other modules
        data = self._gmt_session.retrieve_data(out_id)
        grd_id = self._gmt_session.register_io(io_family['grid'], io_method['reference'],\
                                              io_geometry['surface'], io_direction['in'], None, data)
        grd_str = '-<'+self._gmt_session.encode_id(grd_id)
        
        grid = gmt_types.GMT_Grid(grd_id,grd_str) 
        return grid
 

