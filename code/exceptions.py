# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-

class DataBaseError(Exception):
    """ manages the database errors

    **Parameters**
     error message

     ** Atributes**
     message

     **Methods**
    """
    def __init__(self, message):
        """On se contente de stocker le message d'erreur"""
        self.message = message
        
    def __str__(self):
        """On renvoie le message"""
        return self.message