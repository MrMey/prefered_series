# -*- coding: utf-8 -*-

import unittest

import request_database as r_db
import exceptions


class MyTestCase(unittest.TestCase):
    """Using Travis CI to run the tests automatically"""
    def test_request_database(self):
        print("Tests for the class Database: \n")
        r = r_db.RequestDB()
        
        print("Test 1: method insert")
        self.assertRaises(TypeError,r.insert,"user",[])
        self.assertRaises(exceptions.DataBaseError,r.insert,"user",{"login":"paul","name":"paul"})
        self.assertRaises(exceptions.DataBaseError,r.insert,"users",{"logi":"paul","name":"paul"})