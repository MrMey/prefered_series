import unittest

import request_api as r_api
import exceptions


class MyTestCase(unittest.TestCase):

    def test_request_api(self):
        print("Tests for the class RequestAPI: \n")
        r = r_api.RequestAPI()

        print("Test 1: method research")
        self.assertRaises(exceptions.APIError, r.research, "miyflioubiugytfdrxdyvhxlizhab")
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
        self.assertRaises(exceptions.APIError, r.get_details, "12")
        self.assertTrue(isinstance(r.get_details(12), list))
        test_series = [r.get_details(27845), r.get_details(120)]
        for series in test_series:
            self.assertEquals(len(series), 9)
            self.assertTrue(isinstance(series[0], str))
            self.assertTrue((isinstance(series[1], str)) or (series[1] is None))
            self.assertTrue((isinstance(series[2], str)) or (series[2] is None))
            self.assertTrue((isinstance(series[3], float)) or (series[3] is None))
            self.assertTrue((isinstance(series[4], list)) or (series[4] is None))
            self.assertTrue((isinstance(series[5], str)) or (series[5] is None))
            self.assertTrue((isinstance(series[6], int)) or (series[6] is None))
            self.assertTrue((isinstance(series[7], str)) or (series[7] is None))
            self.assertTrue((isinstance(series[8], str)) or (series[8] is None))

        print("Test 3: method get_cast")

test = MyTestCase()
test.test_request_api()