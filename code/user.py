import exceptions

class User:
    """Stores the info about the users of the website

     ** Attributes**
     _login
     _user_id
     _series : 
         series is a list of 3-element lists containing id, name and image
     tables
     """
     

    def __init__(self, login, id):

        if not isinstance(login, str):
            print ("Error : Login must be a string")
        if login == "":
            print ("Error : Enter a correct login")
        if not isinstance(id, int):
            print ("Error : Your ID must be a integer")

        # Propriétés
        self._login = login
        self._id = id
        self._series = []

    def _get_id(self):
        return(self._id)
    id = property(_get_id)

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
        
    