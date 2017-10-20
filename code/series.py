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
        if(params[0] == None):
            self._name = 'missing name'
        else:
            self._name = params[0]
        if(params[1] == None):
            self._image = "http://www.clker.com/cliparts/n/T/5/z/f/Y/image-missing-md.png"
        else:
            self._image = params[1]
        if(params[2] == None):
            self._summary = "missing summary"
        else:
            self._summary = params[2]
        if(params[3] == None):
            self._rating = "missing rating"
        else:
            self._rating = params[3]
        if(params[4] == None):
            self._genre = []
        else:
            self._genre = params[4]
        if(params[5] == None):
            self._status = "missing status"
        else:
            self._status = params[5]
        if(params[6] == None):
            self._runtime = "missing runtime"
        else:
            self._runtime = params[6]
        if(params[7] == None):
            self._premiered = "missing premiered"
        else:
            self._premiered = params[7]
        if(params[8] == None):
            self._website = "missing website"
        else:
            self._website = params[8]
    
    def get_basics(self):
        return([self._name,self._image,self._id])

    def missing_basic(series_list):
        for series in series_list:
            if(series[0] == None):
                series[0] = "missing name"
            if(series[1] == None):
                series[1] = "http://www.clker.com/cliparts/n/T/5/z/f/Y/image-missing-md.png"
            if(series[2] == None):
                series[2] = "missing name"
        return(series_list)