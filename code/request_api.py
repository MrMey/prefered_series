# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-
import requests
import exceptions as e
import re 

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
            raise e.NoMatchInAPIDatabase("no match for this name")
        else:
            list_series = []
            for tvshow in id:
                name = None
                id_api = None
                image = None
                try:
                    name = tvshow['show']['name']
                    id_api = int(tvshow['show']['id'])
                    image = tvshow['show']['image']['medium']
                except:
                    pass
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
            - the days of diffusion (list)
            - the time of diffusion
        """
        if not isinstance(id_series, int):
            raise e.SeriesIdAreIntegers("")
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series))
        assert response.status_code == 200
        response = response.json()

        try:
            name = response['name']
        except Exception:
            raise e.MissingCrucialInformationAPI("all series must have a name in the API database")
        image = None
        summary = None
        rating = None
        genres = None
        status = None
        runtime = None
        premiered = None
        website = None
        schedule_days = None
        schedule_time = None
        try:
            image = response['image']['medium']  # we chose medium so that all images have the same size
            summary = response['summary']  # Watch out! there are some tags!
            rating = response['rating']['average']  # out of 10
            genres = response['genres']  # Watch out! It's a list!
            status = response['status']
            runtime = response['runtime']
            premiered = response['premiered'][:4]  # only the year
            website = response['officialSite']
            if status == "Running":
                schedule_days = response['schedule']['days'] #  it's a list
                schedule_time = response['schedule']['time']
        except Exception:
            pass
        attributes = [name,
                      image,
                      summary,
                      rating,
                      genres,
                      status,
                      runtime,
                      premiered,
                      website,
                      schedule_days,
                      schedule_time]
        return attributes

    @staticmethod
    def get_cast(id_series):
        """ Gets the cast for the series

        **Parameters**
        id_series is the id of the series in the API database (int)

        **Returns**
        a list of the characters in a series described by a tuple with the name of the actor, the name of the
        character and an image of the actor
        """
        if not isinstance(id_series, int):
            raise e.SeriesIdAreIntegers("")
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series) + '/cast')
        assert response.status_code == 200
        response = response.json()
        list_characters = []
        for character in response:
            try:
                a = character['person']['name']
                b = character['character']['name']
            except Exception:
                raise e.MissingCrucialInformationAPI("characters mentionned has a name and a role")
            try:
                c = character['person']['image']['medium']
            except Exception:
                c = None
            character_tuple = (a, b, c)
            list_characters.append(character_tuple)
        return list_characters

    @staticmethod
    def get_crew(id_series):
        """ Gets the crew for the series

        **Parameters**
        id_series is the id of the series in the API database (int)

        **Returns**
        a list of the crew for a series described by a tuple with the name of the crew member, his or her job and
        an image
        """
        if not isinstance(id_series, int):
            raise e.SeriesIdAreIntegers("")
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series) + '/crew')
        assert response.status_code == 200
        response = response.json()
        list_crew = []
        for person in response:
            try:
                a = person['person']['name']
                b = person['type']
            except Exception:
                raise e.MissingCrucialInformationAPI("crew members have a name and a job")
            try:
                c = person['person']['image']['medium']
            except Exception:
                c = None
            crew_tuple = (a, b, c)
            list_crew.append(crew_tuple)
        return list_crew

    @staticmethod
    def get_seasons(id_series):
        """ Gets the seasons list for the series, with the number, the name, the summary and the dates

        **Parameters**
        id_series is the id of the series in the API database (int)

        **Returns**
        a list of the seasons of a series described by a list with
        - the number
        - the name
        - the summary of the season
        - the date of the beginning of the season
        - the date of the end of the season
        """
        if not isinstance(id_series, int):
            raise e.SeriesIdAreIntegers("")
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series) + '/seasons')
        assert response.status_code == 200
        response = response.json()
        list_seasons = []
        for season in response:
            number = None
            name = None
            summary = None
            beginning = None
            end = None
            try:
                number = season['number']
                name = season['name']
                if name == '':
                    name = None
                summary = season['summary']
                if summary == '':
                    summary = None
                beginning = season['premiereDate']
                end = season['endDate']
            except Exception:
                pass
            s = [number, name, summary, beginning, end]
            list_seasons.append(s)
        return list_seasons

    @staticmethod
    def get_episodes(id_series):
        """ Gets the episodes list for the series, with the number of the season, the number of the episode, the name,
        the summary, an image, the air date and the runtime

        **Parameters**
        id_series is the id of the series in the API database (int)

        **Returns**
        a list of the episodes of a series described by a list with
        - the number of the season
        - the number of the episode
        - the name
        - the summary
        - an image
        - the air date
        - the runtime
        """
        if not isinstance(id_series, int):
            raise e.SeriesIdAreIntegers("")
        response = requests.get('http://api.tvmaze.com/shows/' + str(id_series) + '/episodes')
        assert response.status_code == 200
        response = response.json()
        list_episodes = []
        dict_episodes = {}
        
        for episode in response:
            number_season = None
            number_episode = None
            name = None
            summary = None
            airdate = None
            runtime = None
            image = None
            try:
                number_season = episode['season']
                number_episode = episode['number']
                if episode['season'] not in dict_episodes.keys():
                    dict_episodes[episode['season']] = {}
                if episode['number'] not in dict_episodes[episode['season']].keys():
                    dict_episodes[episode['season']][episode['number']] = {}
                
                # Watch out! Sometimes the episode's number includes the season's number : episode 101 = first episode
            except Exception:
                raise e.MissingCrucialInformationAPI("all episodes have a number and belong to a season")
            try:
                name = episode['name']
                if name == '':
                    name = None
                summary = re.sub("(?s)<[^>]*>|&#?\w+;", "", episode['summary'])
                if summary == '':
                    summary = None
                airdate = episode['airdate']
                runtime = episode['runtime']
                image = episode['image']['medium']

                dict_episodes[episode['season']][episode['number']]['name'] = name
                dict_episodes[episode['season']][episode['number']]['summary'] = summary
                dict_episodes[episode['season']][episode['number']]['airdate'] = airdate
                dict_episodes[episode['season']][episode['number']]['runtime'] = runtime
                dict_episodes[episode['season']][episode['number']]['image'] = image
            except Exception:
                pass
            s = [number_season, number_episode, name, summary, airdate, runtime, image]
            list_episodes.append(s)
        return dict_episodes

    @staticmethod
    def schedule(list_ids):
        """
        For a list of series identified by their id in the API database, the schedule of the week is build.

        **Parameters**
            - list_ids : list of the series' id

        **Returns**
            - dictionary of the diffusion in the week : {"monday" : [{"name": "Bones", "time" : "22:00"}, ... ], ...}
        """
        schedule_dictionary = {"Monday": [],
                               "Tuesday": [],
                               "Wednesday": [],
                               "Thursday": [],
                               "Friday": [],
                               "Saturday": [],
                               "Sunday": []}
        for series in list_ids:
            if not isinstance(series, int):
                raise e.SeriesIdAreIntegers("")
            response = requests.get('http://api.tvmaze.com/shows/' + str(series))
            assert response.status_code == 200
            response = response.json()

            try:
                name = response['name']
            except Exception:
                raise e.MissingCrucialInformationAPI("all series must have a name in the API database")
            name = None
            status = None
            schedule_days = None
            schedule_time = None
            try:
                name = response['name']
                status = response['status']
                if status == "Running":
                    if len(response['schedule']['time'])>0:
                        schedule_days = response['schedule']['days']  # it's a list
                        schedule_time = response['schedule']['time']

                        dict_series = {'name': name, 'time': schedule_time}
    
                        for day in schedule_days:
                            schedule_dictionary[day].append(dict_series)
            except Exception:
                pass

        return schedule_dictionary



if __name__ == '__main__':
    # RequestAPI.research('game')
    # RequestAPI.get_details(48)
    # RequestAPI.get_cast(120)
    # RequestAPI.get_crew(120)
    # RequestAPI.get_seasons(568)
    # RequestAPI.get_episodes
    RequestAPI.schedule([45, 49, 48, 43, 1])

