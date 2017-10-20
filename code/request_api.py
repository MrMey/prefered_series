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
                try:
                    name = tvshow['show']['name']
                    id_api = tvshow['show']['id']
                except:
                    raise e.APIError("all series must have a name and an id in the API database")
                try:
                    image = tvshow['show']['image']['medium']
                except:
                    image = None
                list_series.append([name, image, id_api])
        return list_series

    @staticmethod
    def get_details(id_series):
        """
        Gathers the main information about a series. It will be displayed when a series is selected by the user

        **Parameters**
            - id_series : id of the series in the API database (int)

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
        if not isinstance(id_series, int):
            raise e.APIError("series' ids must be integers")
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series))
        assert response.status_code == 200
        response = response.json()

        try:
            name = response['name']
        except Exception:
            raise e.APIError("all series must have a name in the API database")
        image = None
        summary = None
        rating = None
        genres = None
        status = None
        runtime = None
        premiered = None
        website = None
        try:
            image = response['image']['medium']  # we chose medium so that all images have the same size
            summary = response['summary']  # Watch out! there are some tags!
            rating = response['rating']['average']  # out of 10
            genres = response['genres']  # Watch out! It's a list!
            status = response['status']
            runtime = response['runtime']
            premiered = response['premiered'][:4]  # only the year
            website = response['officialSite']
        except Exception:
            print('some missing information')
        attributes = [name, image, summary, rating, genres, status, runtime, premiered, website]
        return attributes

    @staticmethod
    def get_cast(id_series):
        """ Gets the cast for the series"""
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series) + '/cast')
        assert response.status_code == 200
        response = response.json()
        list_characters = []
        for character in response:
            try:
                a = character['person']['name']
                b = character['character']['name']
            except Exception:
                raise e.APIError("characters mentionned has a name and a role")
            try:
                c = character['person']['image']['medium']
            except Exception:
                c = None
            character_tuple = (a, b, c)
            list_characters.append(character_tuple)
        return list_characters



if __name__ == '__main__':
    r = RequestAPI()
    r.research('game')
    r.get_details('88')
    r.get_cast('120')

