from distutils.core import setup,Extension
import numpy as np
import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read('site.cfg')
gmt_include_directory = config.get('DEFAULT' , 'gmt_include_directory')

setup ( name = 'pygmt',
        version = '0.1',
        packages = ['pygmt'],
        ext_modules = [Extension('pygmt._gmt_structs', ['pygmt/gmt_structs.c'],
                       include_dirs=[gmt_include_directory, np.get_include()] ) ],
       )
