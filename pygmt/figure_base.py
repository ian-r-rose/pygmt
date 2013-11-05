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

    def _grid_dataset(self, module, options, input):
        
        #first register the input
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
 
        #then register memory for the grid output
        g = gmt_types.GMT_Grid(self._gmt_session)
        g.register_output()

        #perform the gridding
        grid_opts = ' '.join([d.in_str, '-G'+g.out_str, options])
        self._print_call(module+' '+grid_opts)
        self._gmt_session.call_module(module, grid_opts)

        g.register_input()
        return g        
