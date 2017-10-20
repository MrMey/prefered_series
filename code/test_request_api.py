import unittest

import request_api as r_api
import exceptions as e


class MyTestCase(unittest.TestCase):

    def test_request_api(self):
        print("Tests for the class RequestAPI: \n")
        r = r_api.RequestAPI()

        print("Test 1: method research")
        self.assertRaises(e.APIError, r.research, "miyflidyvhxlizhab")
        self.assertTrue(isinstance(r.research("game"), list))
        test_series = [r.research("game"), r.research("game of thrones"), r.research("breaking bad")]
        for list_series in test_series:
            for series in list_series:
                self.assertTrue(isinstance(series, tuple))
                self.assertEquals(len(series), 3)
                self.assertTrue(isinstance(series[0], str))  # the name is always given
                self.assertTrue((isinstance(series[1], str)) or (series[1] is None))  # the image is optional
                self.assertTrue((isinstance(series[2], int)))  # the id is always given

        print("Test 2: method get_details")

        print("Test 3: method get_cast")

test = MyTestCase()
test.test_request_api()