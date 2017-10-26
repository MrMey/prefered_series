# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-

class Error(Exception):
    def __init__(self, message):
        """We simply store the error message"""
        self.message = message
        
    def __str__(self):
        """Sends the error message"""
        return self.message
    
class DataBaseError(Error):
    """ manages the database errors
    """
    pass

class APIError(Error):
    """ manages the errors linked to API requests
        """
    pass

class UserError(Error):
    """ manages the errors linked to API requests
    """
    pass

class UndefinedUserError(UserError):
    pass