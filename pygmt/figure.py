import api
import gmt_types
import ctypes
import numpy as np
from flags import *


class GMT_Figure:
 
    def __init__(self, ps_file, range, projection, verbose=False):
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
        self.range_opt = '-R'+range
        self.proj_opt = '-J'+projection

        #dummy call to psxy to write the header of the postscript file
        open_options = ' '.join([self.proj_opt, self.range_opt, '-T -K ->%s'%self.ps_file])
        self._gmt_session.call_module('psxy',  open_options)

        #whether to output the GMT calls
        self.verbose = verbose

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

    def psxy(self, options):
        '''
        Call the GMT psxy module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psxy '+module_options)
        self._gmt_session.call_module('psxy', module_options)
 
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

    def psclip(self,options):
        '''
        Call the GMT psclip module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psclip '+module_options)
        self._gmt_session.call_module('psclip', module_options)

    def pscontour(self,options):
        '''
        Call the GMT pscontour module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pscontour '+module_options)
        self._gmt_session.call_module('pscontour', module_options)

    def psmask(self,options):
        '''
        Call the GMT psmask module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('psmask '+module_options)
        self._gmt_session.call_module('psmask', module_options)

    def pstext(self,options):
        '''
        Call the GMT pstext module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pstext '+module_options)
        self._gmt_session.call_module('pstext', module_options)

    def pswiggle(self,options):
        '''
        Call the GMT pswiggle module with the text string "options"
        '''
        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pswiggle '+module_options)
        self._gmt_session.call_module('pswiggle', module_options)

    def psxy_test(self,options,vectors):
        
        ncols = len(vectors)
        nrows = len(vectors[0])
        for v in vectors:
          assert (len(v) == nrows)

        gmt_vector = gmt_types.gmt_vector_from_array( vectors)
         
        id = self._gmt_session.register_io(io_family['dataset'], io_method['reference']+io_approach['via_vector'],\
                                           io_geometry['surface'], io_direction['in'],\
                                           None, ctypes.cast(ctypes.byref(gmt_vector), ctypes.c_void_p))
        id_str = self._gmt_session.encode_id(id)

        module_options = ' '.join([self.proj_opt, self.range_opt, options, self.ko_opt, '-<%s'%(id_str), self.ps_output])
        self._print_call('psxy '+module_options)
        self._gmt_session.call_module('psxy', module_options)





if __name__ == "__main__":
    lats = np.linspace(0, 45, 100)
    lons = np.linspace(0, 100, 100)
    size = np.ones_like(lons)
 
    fig = GMT_Figure("output.ps", range='g', projection='H7i', verbose=True)
    fig.pscoast('-Glightgray -A500')
    fig.psbasemap('-B30g30/15g15') 
    fig.psxy_test('-Sc', [lons, lats, size])
    fig.close()
