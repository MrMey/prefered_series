class Series:
    """ Stores temporary the data of the series we are manipulating

    **Parameters**
     no parameters

     ** Attributes**
     _name
     _image
     _id
     
     Optional
    _summary
    _rating
    _genre
    _status
    _runtime
    _premiered
    _website
     

     **Methods**
     initiate_from_details:
         initiate the series with the elements returned by the 
         request_api.get_details
     get_basics:
         return the list of elements (name,image,id_api) needed to add a serie
         in the database
     """

    def __init__(self):
        
        self._name = ""
        self._image = ""
        self._id = None
    
    def _get_name(self):
        return(self._name)
    name = property(_get_name)
    
    def _get_image(self):
        return(self._image)
    image = property(_get_image)
    
    def _get_id(self):
        return(self._id)
    
    def _set_id(self,id):
        self._id = id
    id = property(_get_id,_set_id)
    
    def initiate_from_basics(self,params):
        self._name = params[0]
        self._image = params[1]

    def initiate_from_details(self,params):
        self._name = params[0]
        self._image = params[1]
        self._summary = params[2]
        self._rating = params[3]
        self._genre = params[4]
        self._status = params[5]
        self._runtime = params[6]
        self._premiered = params[7]
        self._website = params[8]
    
    def get_basics(self):
        return([self._name,self._image,self._id])