import api
import gmt_types
from flags import *
import numpy as np


class GMT_Figure_base:
 
    def __init__(self, ps_file='', figure_range='', projection='', verbosity=-1, autopilot=True):
        '''
        Initialize a GMT figure.  Sets up the GMT session,
        gets the range and projection types, and writes the
        header to the postscript file.
        '''

        self._gmt_session = api.GMT_Session(ps_file+" session")
        self.autopilot = autopilot

        #set some universal GMT flags for this figure
        self.ps_file = ps_file
        self.ps_output = '->>'+ps_file
        self.ko_opt = '-O -K'
        self.range_opt = '-R'+figure_range
        self.proj_opt = '-J'+projection

        #what level of verbosity
        self.verbosity = verbosity
        self.verbose_opt = ''
        if verbosity >= 0:
            self.verbose_opt = '-V'+str(verbosity)

        self.autopilot_options = ''
        if self.autopilot == True:
          self.autopilot_options = ' '.join([self.range_opt, self.proj_opt, \
                                   self.ko_opt, self.verbose_opt, self.ps_output] )

        if self.autopilot == True:
            #dummy call to psxy to write the header of the postscript file
            open_options = ' '.join([self.proj_opt, self.range_opt, '-T -K ->%s'%self.ps_file])
            self._gmt_session.call_module('psxy',  open_options)

    def close(self):
        '''
        Close out the figure.  Writes the postscript trailer
        in the figure file.
        '''
        #dummy call to psxy
        if self.autopilot == True:
            close_options = ' '.join([self.proj_opt, self.range_opt, '-T -O', self.ps_output])
            self._gmt_session.call_module('psxy', close_options)

    def _print_call(self, str):
        '''
        Debug output for printing the options given to GMT modules
        '''
        if self.verbosity >= 0:
            print(str)

    def _grid_dataset(self, module, options, input, output):
        
        #first register the input
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
 
        #then register memory for the grid output
        g = gmt_types.GMT_Grid(self._gmt_session)
        g.register_output(output)

        #perform the gridding
        grid_opts = ' '.join([d.in_str, g.out_str, options])
        self._print_call(module+' '+grid_opts)
        self._gmt_session.call_module(module, grid_opts)

        return g        

