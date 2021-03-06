import re 

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
        self._summary = ""
        self._rating = ""
        self._genre = []
        self._status = ""
        self._runtime = ""
        self._premiered = ""
        self._website = ""
        
    
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

    def _get_summary(self):
        return(self._summary)
    summary = property(_get_summary)

    def _get_rating(self):
        return(self._rating)
    rating = property(_get_rating)

    def _get_genre(self):
        return(self._genre)
    genre = property(_get_genre)
    
    def _get_status(self):
        return(self._status)
    status = property(_get_status)

    def _get_runtime(self):
        return(self._runtime)
    runtime = property(_get_runtime)
    
    def _get_premiered(self):
        return(self._premiered)
    premiered = property(_get_premiered)

    def _get_website(self):
        return(self._website)
    website = property(_get_website)

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
            self._summary = re.sub("(?s)<[^>]*>|&#?\w+;", "", params[2])
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
        return([self._name,self._image,self._id,self._status])

    def missing_basic(series_list):
        for series in series_list:
            if(series[0] == None):
                series[0] = "missing name"
            if(series[1] == None):
                series[1] = "http://www.clker.com/cliparts/n/T/5/z/f/Y/image-missing-md.png"
            if(series[2] == None):
                series[2] = "missing name"
        return(series_list)