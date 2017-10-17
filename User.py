import Series

class User:
    """Stores the info about the users of the website

    Class defining a User by :
        - Login
        - ID from database"""

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
