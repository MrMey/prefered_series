# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-


class DataBaseError(Exception):
    """ manages the database errors

    **Parameters**
     error message

     ** Attributes**
     message

     **Methods**
    """
    def __init__(self, message):
        """We simply store the error message"""
        self.message = message
        
    def __str__(self):
        """Sends the error message"""
        return self.message


class APIError(Exception):
    """ manages the errors linked to API requests

        **Parameters**
         error message

         ** Attributes**
         message

         **Methods**
        """

    def __init__(self, message):
        """We simply store the error message"""
        self.message = message

    def __str__(self):
        """Sends the error message"""
        return self.message