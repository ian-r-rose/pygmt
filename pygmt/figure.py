import api
import gmt_types
from flags import *
import numpy as np
import ctypes


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

    def register_input(self, input):
        '''
        Determine what kind of input has been given to a module,
        register it, and return the id and id_str to which it corresponds
        '''

        #first check if it is a string.  if so, try to open
        #the file with that 
        id = -1
        if isinstance(input, str) == True:
            id = self._gmt_session.register_io(io_family['dataset'], io_method['file'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, input)
        #if instead it is a python file object, get the file descriptor
        #number and open with that
        elif isinstance(input, file) == True:
            fd =input.fileno()
            id = self._gmt_session.register_io(io_family['dataset'], io_method['fdesc'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, ctypes.pointer(ctypes.c_uint(fd)))

        #If it is a GMT_vector, register that.
        elif isinstance(input, gmt_types.GMT_Vector):
            id = self._gmt_session.register_io(io_family['dataset'], io_method['reference']+io_approach['via_vector'],\
                                               io_geometry['point'], io_direction['in'],\
                                               None, input.ptr)

        else:
            raise gmt_types.GMT_Error("Unsupported input type") 
            
        id_str = self._gmt_session.encode_id(id)
        return id, id_str


    def psxy(self, options, input):
        '''
        Call the GMT psxy module with the text string "options" and the input "input"
        options is a text string of the flags to be given to psxy.
        '''
        id, id_str = self.register_input(input)
        input_opt = '-<'+id_str
        module_options = ' '.join([input_opt, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
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

    def pswiggle(self,options,input):
        '''
        Call the GMT pswiggle module with the text string "options"
        '''
        id, id_str = self.register_input(input)
        input_opt = '-<'+id_str
        module_options = ' '.join([input_opt, self.proj_opt, self.range_opt, options, self.ko_opt, self.ps_output])
        self._print_call('pswiggle '+module_options)
        self._gmt_session.call_module('pswiggle', module_options)



if __name__ == "__main__":
    lats = np.linspace(0,45, 100)
    lons = np.linspace(0,45, 100)
    size = np.linspace(0.0,np.pi*10, 100)
    size = np.sin(size)

    fig = GMT_Figure("output.ps", range='g', projection='H7i', verbose=True)
    fig.pscoast('-Glightgray -A500')
    fig.psbasemap('-B30g30/15g15') 
    fig.pswiggle('-Gblack -Z10c', gmt_types.GMT_Vector([lons,lats,size]))
    fig.pswiggle('-G-red -Z10c', gmt_types.GMT_Vector([lons,lats,size]))
    lons = lons+100
    fig.psxy('', gmt_types.GMT_Vector([lons,lats,size]))

    fig.close()
