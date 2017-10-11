# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-
import requests

class Request:
    """ Sends requests to the TV shows API tvmaze

    This class makes all the requests to get information about a TV show thanks to http://api.tvmaze.com.

    **Parameters**
     no parameters

     ** Atributes**
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
        print('initiating Request')

    @staticmethod
    def get_main_information(series):
        # TODO : erreurs
        # TODO : commentaire
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
        id = requests.get('http://api.tvmaze.com/search/shows?q=' + series)
        assert id.status_code == 200
        id = id.json()
        try:
            id = id[0]['show']['id']
        except:
            raise Exception ("series not in database") # TODO : create this exception properly
        response = requests.get('http://api.tvmaze.com/shows/' + str(id))
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




r = Request()
r.get_main_information('game of thrones')

