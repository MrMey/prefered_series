class Series:
    """Stores the info regarding the TV shows as seen on Page 1

    Class defining a TV show by :
    - ID in database
    - Title
    - Picture
    - Next episode out"""

    def __init__(self):
        
        self._name = ""
        self._image = ""
        self._series_id = None
    
    def _get_name(self):
        return(self._name)
    name = property(_get_name)
    
    def _get_image(self):
        return(self._image)
    image = property(_get_image)
    
    def _get_series_id(self):
        return(self._series_id)
    series_id = property(_get_series_id)
    
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
        return([self._name,self._image,self._id_api])