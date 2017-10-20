# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-
import requests
import exceptions as e


class RequestAPI:

    """ Sends requests to the TV shows API tvmaze

    This class makes all the requests to get information about a TV show thanks to http://api.tvmaze.com.

    **Parameters**
     no parameters

     ** Attributes**
     no attributes

     **Methods**
     *(static methods)*

     - get_main_information(series):
        gets the main information about a series, to be displayed when the series is selected. Other methods will
        return some more specific piece of information concerning the series.

        returns:
            - the name of the series
            - an image to be displayed (url)
            - the global summary
            - rating
            - the main genres of the series
            - the status for example 'ended'
            - the average runtime for episodes
            - the year of the first diffusion
            - the official website

    """
    def __init__(self):
        print('initiating RequestAPI')

    @staticmethod
    def research(series):
        """
        Search in the API database all the series with a name close to the one specified, for the user to search
        for an unknown series

        **Parameters**
            - series : the alledged name of the series

        **Returns**
            - the list of series with a name that could correspond to the users request and a corresponding image
        """
        id = requests.get('http://api.tvmaze.com/search/shows?q=' + series)
        assert id.status_code == 200
        id = id.json()
        if id == []:
            raise e.APIError("no match for this name")
        else:
            list_series = []
            for tvshow in id:
                list_series.append((tvshow['show']['name'], tvshow['show']['image']['medium']))
        return list_series

    @staticmethod
    def get_id_API(series):
        """
        Gets the id of the series in the API database in order the make the correct requests

        **Parameters**
            - series : the series name

        **Returns**
            - the series id in the API database
        """
        id = requests.get('http://api.tvmaze.com/search/shows?q=' + series)
        assert id.status_code == 200
        id = id.json()
        try:
            id = id[0]['show']['id']
        except:
            raise e.APIError("series not in database")
        return (str(id))

    @staticmethod
    def get_basics(series):
        """
        Gathers basic information about a series, to be stored in the database.

        **Parameters**
            - series : name of the selected TV show

        **Returns**
            - name
            - image : it's the URL of the selected TV show
        """
        response = requests.get('http://api.tvmaze.com/search/shows?q=' + series)
        assert response.status_code == 200
        response = response.json()
        try:
            name = response[0]['show']['name']
            image = response[0]['show']['image']['medium']
        except:
            raise e.APIError("series not in database")
        return ([name, image])

    @staticmethod
    def get_details(series):
        """
        Gathers the main information about a series. It will be displayed when a series is selected by the user

        **Parameters**
            - series : name of the selected TV show

        **Returns**
         attributes :
         it is a list with :
            - the name of the series
            - an image to be displayed (url)
            - the global summary
            - rating
            - the main genres of the series
            - the status for example 'ended'
            - the average runtime for episodes
            - the year of the first diffusion
            - the official website
        """
        id = RequestAPI.get_id_API(series)
        response = requests.get('http://api.tvmaze.com/shows/' + id)
        assert response.status_code == 200
        response = response.json()

        name = response['name']
        image = response['image']['medium']  # we chose medium so that all images have the same size
        summary = response['summary']  # Watch out! there are some tags!
        rating = response['rating']['average']  # out of 10
        genres = response['genres']  # Watch out! It's a list!
        status = response['status']
        runtime = response['runtime']
        premiered = response['premiered'][:4]  # only the year
        website = response['officialSite']

        attributes = [name, image, summary, rating, genres, status, runtime, premiered, website]
        return(attributes)

    @staticmethod
    def get_cast(series):
        """ Gets the cast for the series"""
        id = RequestAPI.get_id_API(series)
        response = requests.get('http://api.tvmaze.com/shows/' + id + '/cast')
        assert response.status_code == 200
        response = response.json()
        list_characters = []
        for character in response:
            a = character['person']['name']
            b = character['character']['name']
            c = character['character']['image']['medium']
            list_characters.append((a,b,c))
        return(list_characters)




r = RequestAPI()
r.research('game')
r.get_details('Game of Thrones')
r.get_basics('game')
r.get_cast('game of thrones')

