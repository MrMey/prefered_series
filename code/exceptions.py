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
    """ manages the errors linked to API requests"""
    pass


class MissingCrucialInformationAPI(APIError):
    """error when the API database misses some crucial information like the name or id of a series"""
    pass

class UnavailableService(APIError):
    pass

class NoMatchInAPIDatabase(APIError):
    """error when the wanted series in not in tha API Database"""
    pass


class SeriesIdAreIntegers(APIError):
    """error if functions are called with a series id that is not of type int"""
    pass


class UserError(Error):
    """ manages the errors linked to API requests
    """
    pass


class UndefinedUserError(UserError):
    pass


class InvalidFieldError(DataBaseError):
    pass

class AlreadyExistingInstanceError(DataBaseError):
    pass