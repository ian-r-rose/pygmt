import api
import gmt_grid
import gmt_text
import gmt_data
import gmt_cpt
from flags import *
import numpy as np
from figure_base import GMT_Figure_base


class GMT_Figure(GMT_Figure_base):
    '''
    Derive from the base class, which handles all the i/o stuff, 
    setting up, and tearing down.  Here we just want to define
    all the normal GMT modules.
    ''' 
    def gmtset(self, options):
        self._gmt_session.call_module('gmtset', options)

    ### All the GMT modules for creating, writing, reading, and
    ### converting gridded data
    def xyz2grd(self, options, input, output=None):
        return self._grid_dataset('xyz2grd', options, input, output)

    def surface(self, options, input, output=None):
        return self._grid_dataset('surface', options, input, output)

    ### All the GMT modules for doing operations on gridded data
    def grdcut(self, options, input, output = None):
        g1 = gmt_grid.GMT_Grid(self._gmt_session)
        g1.register_input(input)

        g2 = gmt_grid.GMT_Grid(self._gmt_session)
        g2.register_output(output)

        module_options = ' '.join([g1.in_str, options, g2.out_str, self.v])
        self._print_call('grdcut '+module_options)
        self._gmt_session.call_module('grdcut', module_options)
        return g2

    def grdgradient(self, options, input, output = None):
        g1 = gmt_grid.GMT_Grid(self._gmt_session)
        g1.register_input(input)

        g2 = gmt_grid.GMT_Grid(self._gmt_session)
        g2.register_output(output)

        module_options = ' '.join([g1.in_str, options, '-G'+g2.out_str, self.v])
        self._print_call('grdgradient '+module_options)
        self._gmt_session.call_module('grdgradient', module_options)
        return g2
        
        
    def grdinfo(self, options, input):
        g = gmt_grid.GMT_Grid(self._gmt_session)
        g.register_input(input)

        module_options = ' '.join([g.in_str, options, self.v])
        self._print_call('grdinfo '+module_options)
        self._gmt_session.call_module('grdinfo', module_options)

    def grdmath(self, *args):
        #parse all the input operations
        module_options = ''
        for a in args:
            if isinstance(a, gmt_grid.GMT_Grid):
                a.register_input()
                module_options = " ".join([module_options, a.in_str])
            else:
                module_options = " ".join([module_options, str(a)])

        #prepare the output grid
        g = gmt_grid.GMT_Grid(self._gmt_session)
        g.register_output()
        module_options = " ".join([module_options, " = "+g.out_str])
 
        #call grdmath
        self._print_call('grdmath '+module_options)
        self._gmt_session.call_module('grdmath', module_options)
        return g

    ### All the GMT podules that plot gridded data

    def grdcontour(self,options, input):
        g = gmt_grid.GMT_Grid(self._gmt_session)
        g.register_input(input)

        module_options = ' '.join([g.in_str,  options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('grdcontour '+module_options)
        self._gmt_session.call_module('grdcontour', module_options)

    def grdview(self,options, input, cpt=None, intensity=None):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        g = gmt_grid.GMT_Grid(self._gmt_session)
        g.register_input(input)

        module_options = ' '.join([g.in_str,  options, self.ko, self.v, self.range_proj, self.ps_output])
        if intensity != None:
            g = gmt_grid.GMT_Grid(self._gmt_session)
            g.register_input(intensity)
            module_options = module_options + ' -I' + g.in_str
        if cpt != None:
            c = gmt_cpt.GMT_CPT(self._gmt_session)
            c.register_input(cpt)
            module_options = module_options + ' ' + c.in_str
        self._print_call('grdview '+module_options)
        self._gmt_session.call_module('grdview', module_options)

    def grdimage(self,options, input, cpt=None, intensity=None):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        g = gmt_grid.GMT_Grid(self._gmt_session)
        g.register_input(input)

        module_options = ' '.join([g.in_str,  options, self.ko, self.v, self.range_proj, self.ps_output])
        if intensity != None:
            g = gmt_grid.GMT_Grid(self._gmt_session)
            g.register_input(intensity)
            module_options = module_options + ' -I' + g.in_str
        if cpt != None:
            c = gmt_cpt.GMT_CPT(self._gmt_session)
            c.register_input(cpt)
            module_options = module_options + ' ' + c.in_str
        self._print_call('grdimage '+module_options)
        self._gmt_session.call_module('grdimage', module_options)

    def grdvector(self, options, grid1, grid2):
        g1 = gmt_grid.GMT_Grid(self._gmt_session)
        g2 = gmt_grid.GMT_Grid(self._gmt_session)
        g1.register_input(grid1)
        g2.register_input(grid2)

        module_options = ' '.join([g1.in_str, g2.in_str, options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('grdvector '+module_options)
        self._gmt_session.call_module('grdvector', module_options)

    ### All the GMT modules that plot without needing input data
 
    def pscoast(self,options):
        '''
        Call the GMT pscoast module with the text string "options"
        '''
        module_options = ' '.join([options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('pscoast '+module_options)
        self._gmt_session.call_module('pscoast', module_options)

    def psbasemap(self,options):
        '''
        Call the GMT psbasemap module with the text string "options"
        '''
        module_options = ' '.join([options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('psbasemap '+module_options)
        self._gmt_session.call_module('psbasemap', module_options)

    def psscale(self, options, cpt=None):
        module_options = ' '.join([options, self.ko, self.v, self.range_proj, self.ps_output])
        if cpt != None:
            c = gmt_cpt.GMT_CPT(self._gmt_session)
            c.register_input(cpt)
            module_options = module_options + ' ' + c.in_str
        self._print_call('psscale '+module_options)
        self._gmt_session.call_module('psscale', module_options)
    

    #All the GMT modules dealing with plotting text or numeric data
   
    def pstext(self, options, input):
        '''
        Call the GMT pstext module with the text string "options" and the input "input"
        options is a text string of the flags to be given to pstext.
        '''
        t = gmt_text.GMT_Text(self._gmt_session)
        t.register_input(input)
        module_options = ' '.join([t.in_str, options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('pstext '+module_options)
        self._gmt_session.call_module('pstext', module_options)

    def psxy(self, options, input, cpt=None):
        '''
        Call the GMT psxy module with the text string "options" and the input "input"
        options is a text string of the flags to be given to psxy.
        '''
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str,  options, self.ko, self.v, self.range_proj, self.ps_output])

        if cpt != None:
            c = gmt_cpt.GMT_CPT(self._gmt_session)
            c.register_input(cpt)
            module_options = module_options + ' ' + c.in_str

        self._print_call('psxy '+module_options)
        self._gmt_session.call_module('psxy', module_options)

    def psclip(self,options, input):
        '''
        Call the GMT psclip module with the text string "options"
        '''
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('psclip '+module_options)
        self._gmt_session.call_module('psclip', module_options)

    def pscontour(self,options, input):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('pscontour '+module_options)
        self._gmt_session.call_module('pscontour', module_options)

    def psmask(self,options, input):
        '''
        Call the GMT psmask module with the text string "options"
        '''
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('psmask '+module_options)
        self._gmt_session.call_module('psmask', module_options)

    def pswiggle(self,options,input):
        '''
        Call the GMT pswiggle module with the text string "options"
        '''
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        module_options = ' '.join([d.in_str, options, self.ko, self.v, self.range_proj, self.ps_output])
        self._print_call('pswiggle '+module_options)
        self._gmt_session.call_module('pswiggle', module_options)


    ### All the GMT modules that do text or data operations without plotting
    def grd2cpt(self, options, input, output = None):
        g = gmt_grid.GMT_Grid(self._gmt_session)
        g.register_input(input)
        c = gmt_cpt.GMT_CPT(self._gmt_session)
        c.register_output(output)

        module_options = ' '.join([g.in_str, options, c.out_str, self.v])
        self._print_call('grd2cpt '+module_options)
        self._gmt_session.call_module('grd2cpt', module_options)
        return c

    def makecpt(self, options, output = None):
        c = gmt_cpt.GMT_CPT(self._gmt_session)
        c.register_output(output)

        module_options = ' '.join([options, c.out_str, self.v])
        self._print_call('makecpt '+module_options)
        self._gmt_session.call_module('makecpt', module_options)

        return c
  
    def gmtconvert(self, options, input, output=None):
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input(input)
        d.register_output(output)
 
        module_options=' '.join([d.in_str, options, d.out_str, self.v])
        self._print_call('gmtconvert '+module_options)
        self._gmt_session.call_module('gmtconvert', module_options)
        return d

 

    def blockmean(self, options, input, output=None):
        d1 = gmt_data.GMT_Dataset(self._gmt_session)
        d1.register_input( input )

        d2 = gmt_data.GMT_Dataset(self._gmt_session)
        d2.register_output(output)

        module_options = ' '.join([d1.in_str, options, d2.out_str, self.v])
        self._print_call('blockmean '+module_options)
        self._gmt_session.call_module('blockmean', module_options)
        return d2

    def blockmedian(self, options, input, output=None):
        d1 = gmt_data.GMT_Dataset(self._gmt_session)
        d1.register_input( input )

        d2 = gmt_data.GMT_Dataset(self._gmt_session)
        d2.register_output(output)

        module_options = ' '.join([d1.in_str, options, d2.out_str, self.v])
        self._print_call('blockmedian '+module_options)
        self._gmt_session.call_module('blockmedian', module_options)
        return d2

    def blockmode(self, options, input, output=None):
        d1 = gmt_data.GMT_Dataset(self._gmt_session)
        d1.register_input( input )

        d2 = gmt_data.GMT_Dataset(self._gmt_session)
        d2.register_output(output)

        module_options = ' '.join([d1.in_str, options, d2.out_str, self.v])
        self._print_call('blockmode '+module_options)
        self._gmt_session.call_module('blockmode', module_options)
        return d2
         
    def project(self,options, input, output=None):
        d1 = gmt_data.GMT_Dataset(self._gmt_session)
        d1.register_input( input )

        d2 = gmt_data.GMT_Dataset(self._gmt_session)
        d2.register_output()

        module_options = ' '.join([d1.in_str, options, d2.out_str, self.v])
        self._print_call('project '+module_options)
        self._gmt_session.call_module('project', module_options)
        return d2

    def fitcircle(self,options, input, output=None):
        d = gmt_data.GMT_Dataset(self._gmt_session)
        d.register_input( input )
  
        t = gmt_text.GMT_Text(self._gmt_session)
        t.register_output(output)

        module_options = ' '.join([d.in_str, options, t.out_str, self.v])
        self._print_call('fitcircle '+module_options)
        self._gmt_session.call_module('fitcircle', module_options)
        return t

