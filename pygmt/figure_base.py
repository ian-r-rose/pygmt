import api
import gmt_types
from flags import *
import numpy as np


class GMT_Figure_base:
 
    def __init__(self, ps_file='', figure_range='', projection='', verbosity=-1, autopilot=True, portrait=False):
        '''
        Initialize a GMT figure.  Sets up the GMT session,
        gets the range and projection types, and writes the
        header to the postscript file.
        '''

        self._gmt_session = api.GMT_Session(ps_file+" session")
        self.autopilot = autopilot

        #set some universal GMT flags for this figure
        self.ps_file = ps_file
        self.range_opt = ''
        self.proj_opt = ''
        self.ps_output = ''
        if self.ps_file != '':
            self.ps_output = '->>'+ps_file
        if figure_range != '':
            self.range_opt = '-R'+figure_range
        if projection != '':
            self.proj_opt = '-J'+projection

        #what level of verbosity
        self.verbosity = verbosity
        self.v = ''
        if verbosity >= 0:
            self.v = '-V'+str(verbosity)

        self.ko = ''
        if self.autopilot == True:
            self.ko = '-O -K'
        self.range_proj = ' '.join([self.range_opt, self.proj_opt])

        if self.autopilot == True:
            #dummy call to psxy to write the header of the postscript file
            open_options = ' '.join(['-Rg -JH1i', '-T -K ->%s'%self.ps_file])
            if portrait == True:
                open_options = open_options + ' -P'
            self._gmt_session.call_module('psxy',  open_options)

    def close(self):
        '''
        Close out the figure.  Writes the postscript trailer
        in the figure file.
        '''
        #dummy call to psxy
        if self.autopilot == True:
            close_options = ' '.join(['-Rg -JH1i', '-T -O', self.ps_output])
            self._gmt_session.call_module('psxy', close_options)

    def _print_call(self, string):
        '''
        Debug output for printing the options given to GMT modules
        '''
        if self.verbosity >= 0:
            print(string)

    def read_grid(self, gridfile):
        g = gmt_types.GMT_Grid(self._gmt_session)
        g.register_input(gridfile)
        return g

    def _grid_dataset(self, module, options, input, output):
        
        #first register the input
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
 
        #then register memory for the grid output
        g = gmt_types.GMT_Grid(self._gmt_session)
        g.register_output(output)

        #perform the gridding
        grid_opts = ' '.join([d.in_str, '-G'+g.out_str, options, self.v])
        self._print_call(module+' '+grid_opts)
        self._gmt_session.call_module(module, grid_opts)

        return g        

 
