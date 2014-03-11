__author__ = 'john'

import os
from logging.handlers import RotatingFileHandler


class MakeFileHandler(RotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        super(MakeFileHandler, self).__init__(filename, *args, **kwargs)