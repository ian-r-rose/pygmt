import numpy as np
import api
from flags import *


class GMT_Resource(object):
    '''
    Abstract base class for GMT resources, defining the
    interface.  You should not need to deal directly with
    this class, it does very little.
    '''
    def __init__(self, session):
        self.in_id = -1
        self.in_str = ''
        self.out_id = -1
        self.out_str = ''
        assert( isinstance(session, api.GMT_Session) )
        self._session = session
        self.direction = io_direction['err']

    def register_input(self, input = None):
        raise api.GMT_Error("Base class method not implemented")

    def register_output(self, output = None):
        raise api.GMT_Error("Base class method not implemented")

