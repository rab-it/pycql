__author__ = 'nahid'


#pycql exceptions

class PycqlException(Exception):
    pass


class ModelException(PycqlException):
    pass


class ValidationError(PycqlException):
    pass
