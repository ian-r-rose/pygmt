import api
import gmt_types
import gmt_text
from flags import *
import numpy as np
import ctypes
from figure_base import GMT_Figure_base


class GMT_Figure(GMT_Figure_base):
    '''
    Derive from the base class, which handles all the i/o stuff, 
    setting up, and tearing down.  Here we just want to define
    all the normal GMT modules.
    ''' 

    ### All the GMT modules for creating, writing, reading, and
    ### converting gridded data
    def xyz2grd(self, options, input):
        return self._grid_dataset('xyz2grd', options, input)

    def surface(self, options, input):
        return self._grid_dataset('surface', options, input)

    ### All the GMT modules for doing operations on gridded data
    ### implement some of these!

    ### All the GMT modules for plotting things related to gridded data
    def grdcontour(self,options, grid):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        assert( isinstance(grid, gmt_types.GMT_Grid) == True)
        module_options = ' '.join([grid.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('grdcontour '+module_options)
        self._gmt_session.call_module('grdcontour', module_options)

    def grdimage(self,options, grid):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        assert( isinstance(grid, gmt_types.GMT_Grid) == True)
        module_options = ' '.join([grid.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('grdimage '+module_options)
        self._gmt_session.call_module('grdimage', module_options)

    ### All the GMT modules that plot without needing input data
 
    def pscoast(self,options):
        '''
        Call the GMT pscoast module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pscoast '+module_options)
        self._gmt_session.call_module('pscoast', module_options)

    def psbasemap(self,options):
        '''
        Call the GMT psbasemap module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psbasemap '+module_options)
        self._gmt_session.call_module('psbasemap', module_options)


    #All the GMT modules dealing with plotting text or numeric data
   
    def pstext(self, options, input):
        '''
        Call the GMT pstext module with the text string "options" and the input "input"
        options is a text string of the flags to be given to pstext.
        '''
        t = gmt_text.GMT_Text(self._gmt_session)
        t.register_input(input)
        module_options = ' '.join([t.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pstext '+module_options)
        self._gmt_session.call_module('pstext', module_options)

    def psxy(self, options, input):
        '''
        Call the GMT psxy module with the text string "options" and the input "input"
        options is a text string of the flags to be given to psxy.
        '''
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psxy '+module_options)
        self._gmt_session.call_module('psxy', module_options)

    def psclip(self,options, input):
        '''
        Call the GMT psclip module with the text string "options"
        '''
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psclip '+module_options)
        self._gmt_session.call_module('psclip', module_options)

    def pscontour(self,options, input):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pscontour '+module_options)
        self._gmt_session.call_module('pscontour', module_options)

    def psmask(self,options, input):
        '''
        Call the GMT psmask module with the text string "options"
        '''
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psmask '+module_options)
        self._gmt_session.call_module('psmask', module_options)

    def pswiggle(self,options,input):
        '''
        Call the GMT pswiggle module with the text string "options"
        '''
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pswiggle '+module_options)
        self._gmt_session.call_module('pswiggle', module_options)


    ### All the GMT modules that do text or data operations without plotting
 
    def grd2cpt(self, options, grid, outfile):
        assert( isinstance(grid, gmt_types.GMT_Grid) == True)
        cpt_output = '->'+outfile
        module_options = ' '.join([grid.in_str, options, cpt_output])
        self._print_call('grd2cpt '+module_options)
        self._gmt_session.call_module('grd2cpt', module_options)

    def makecpt(self, options, outfile):
        cpt_output = '->'+outfile
        module_options = ' '.join([options, cpt_output])
        self._print_call('makecpt '+module_options)
        self._gmt_session.call_module('makecpt', module_options)

    def blockmean(self, options, input):
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input( input )
        d.register_output()

        module_options = ' '.join([d.in_str, options, d.out_str])
        self._gmt_session.call_module('blockmean', module_options)
        return d
         
    def blockmedian(self, options, input):
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input( input )
        d.register_output()

        module_options = ' '.join([d.in_str, options, d.out_str])
        self._gmt_session.call_module('blockmedian', module_options)
        return d
       
    def blockmode(self, options, input):
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input( input )
        d.register_output()

        module_options = ' '.join([d.in_str, options, d.out_str])
        self._gmt_session.call_module('blockmode', module_options)
        return d       

    def triangulate(self, options, input):
        d = gmt_types.GMT_Dataset(self._gmt_session)
        d.register_input( input )
        d.register_output()

        module_options = ' '.join([d.in_str, options, d.out_str])
        self._gmt_session.call_module('triangulate', module_options)
        return d
         


