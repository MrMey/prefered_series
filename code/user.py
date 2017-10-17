import exceptions

class User:
    """Stores the info about the users of the website

    Class defining a User by :
        - Login
        - ID from database"""

    def __init__(self, login, user_id):

        if not isinstance(login, str):
            print ("Error : Login must be a string")
        if login == "":
            print ("Error : Enter a correct login")
        if not isinstance(user_id, int):
            print ("Error : Your ID must be a integer")

        # Propriétés
        self._login = login
        self._user_id = user_id
        self._series = []

    def _get_id(self):
        return(self._user_id)
    user_id = property(_get_id)

    def _get_login(self):
        return(self._login)
    login = property(_get_login)
    
    def _get_series(self):
        return(self._series)
    
    def _set_series(self,series):
        if not isinstance(series,list):
            raise(TypeError("series must be a list"))
        self._series = series
    series = property(_get_series,_set_series)
        
    