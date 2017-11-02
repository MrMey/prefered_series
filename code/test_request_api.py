import unittest

import request_api as r_api
import exceptions


class MyTestCase(unittest.TestCase):
    """Using Travis CI to run the tests automatically"""
    def test_request_api(self):
        print("Tests for the class RequestAPI: \n")

        print("Test 1: method research")
        self.assertRaises(exceptions.NoMatchInAPIDatabase, r_api.RequestAPI.research, "miyflioubiugytfdrxdyvhxlizhab")
        self.assertTrue(isinstance(r_api.RequestAPI.research("game"), list))
        test_series = [r_api.RequestAPI.research("game"),
                       r_api.RequestAPI.research("game of thrones"),
                       r_api.RequestAPI.research("breaking bad")]
        for list_series in test_series:
            for series in list_series:
                self.assertTrue(isinstance(series, list))
                self.assertEquals(len(series), 3)
                self.assertTrue(isinstance(series[0], str))  # the name is always given
                self.assertTrue((isinstance(series[1], str)) or (series[1] is None))  # the image is optional
                self.assertTrue((isinstance(series[2], int)))  # the id is always given

        print("Test 2: method get_details")
        self.assertRaises(exceptions.SeriesIdAreIntegers, r_api.RequestAPI.get_details, "12")
        self.assertTrue(isinstance(r_api.RequestAPI.get_details(12), list))
        test_series = [r_api.RequestAPI.get_details(27845), r_api.RequestAPI.get_details(120)]
        for series in test_series:
            self.assertEquals(len(series), 11)
            self.assertTrue(isinstance(series[0], str))
            self.assertTrue((isinstance(series[1], str)) or (series[1] is None))
            self.assertTrue((isinstance(series[2], str)) or (series[2] is None))
            self.assertTrue((isinstance(series[3], float)) or (series[3] is None))
            self.assertTrue((isinstance(series[4], list)) or (series[4] is None))
            self.assertTrue((isinstance(series[5], str)) or (series[5] is None))
            self.assertTrue((isinstance(series[6], int)) or (series[6] is None))
            self.assertTrue((isinstance(series[7], str)) or (series[7] is None))
            self.assertTrue((isinstance(series[8], str)) or (series[8] is None))
            self.assertTrue((isinstance(series[9], list)) or (series[9] is None))
            self.assertTrue((isinstance(series[10], str)) or (series[10] is None))

        print("Test 3: method get_cast")
        self.assertTrue(isinstance(r_api.RequestAPI.get_cast(120), list))
        test_series = [r_api.RequestAPI.get_cast(27845), r_api.RequestAPI.get_cast(120)]
        for series in test_series:
            for person in series:
                self.assertTrue((isinstance(person, tuple)))
                self.assertEquals(len(person), 3)
                self.assertTrue(isinstance(person[0], str))
                self.assertTrue(isinstance(person[1], str))
                self.assertTrue((isinstance(person[2], str)) or (person[2] is None))

        print("Test 4: method get_crew")
        self.assertTrue(isinstance(r_api.RequestAPI.get_crew(120), list))
        test_series = [r_api.RequestAPI.get_crew(27845), r_api.RequestAPI.get_crew(120)]
        for series in test_series:
            for person in series:
                self.assertTrue((isinstance(person, tuple)))
                self.assertEquals(len(person), 3)
                self.assertTrue(isinstance(person[0], str))
                self.assertTrue(isinstance(person[1], str))
                self.assertTrue((isinstance(person[2], str)) or (person[2] is None))

        print("Test 5: method get_seasons")
        self.assertTrue(isinstance(r_api.RequestAPI.get_seasons(597), list))
        test_series = [r_api.RequestAPI.get_seasons(27845), r_api.RequestAPI.get_seasons(120)]
        for series in test_series:
            for season in series:
                self.assertTrue((isinstance(season, list)))
                self.assertEquals(len(season), 5)
                self.assertTrue((isinstance(season[0], int)) or (season[2] is None))
                self.assertTrue((isinstance(season[1], str)) or (season[2] is None))
                self.assertTrue((isinstance(season[2], str)) or (season[2] is None))
                self.assertTrue((isinstance(season[3], str)) or (season[3] is None))
                self.assertTrue((isinstance(season[4], str)) or (season[4] is None))

        print("Test 6: method get_episodes")
        self.assertTrue(isinstance(r_api.RequestAPI.get_episodes(12), list))
        test_series = [r_api.RequestAPI.get_episodes(27845), r_api.RequestAPI.get_episodes(120)]
        for series in test_series:
            for episode in series:
                self.assertEquals(len(episode), 7)
                self.assertTrue(isinstance(episode[0], int))
                self.assertTrue(isinstance(episode[1], int))
                self.assertTrue((isinstance(episode[2], str)) or (episode[2] is None))
                self.assertTrue((isinstance(episode[3], str)) or (episode[3] is None))
                self.assertTrue((isinstance(episode[4], str)) or (episode[4] is None))
                self.assertTrue((isinstance(episode[5], int)) or (episode[5] is None))
                self.assertTrue((isinstance(episode[6], str)) or (episode[6] is None))

        print("Test 7: method schedule")
        dict_schedule = r_api.RequestAPI.schedule([45, 49, 48, 43])
        self.assertTrue(isinstance(dict_schedule, dict))
        for key in dict_schedule:
            self.assertTrue(key in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            self.assertTrue(isinstance(dict_schedule[key], list))
            for series in dict_schedule[key]:
                self.assertTrue(isinstance(series, dict))
                for key_series in series:
                    self.assertTrue(key_series in ["name", "time"])
                    self.assertTrue(isinstance(series[key_series], str))