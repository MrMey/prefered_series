# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 10:08:33 2017

@author: Mr_Mey
"""

import sqlite3

class DataBase:
    def __init__(self):
        self.connector = sqlite3.connect('series.db')
        self.cursor = self.connector.cursor()
        self.tables = {}
        
    def commit(self):
        self.connector.commit()
    
    def __del__(self):
        """ when you del the table, makes sure the connection is closed, at
        the end of the db call you should del the database"""
        self.connector.close()
        del(self)
    
    def execute(self,instruction):
        self.cursor.execute(instruction)
        self.commit()
    
    def drop(self,table):
        """drop one table - DO NOT EXECUTE THIS WITHOUT BEING SURE"""
        self.execute("""DROP TABLE """+ table)
        
    def create_series_table(self):
        """create a series table which contains all details about series"""
        self.tables["series"] = Table(["name"])
        self.execute("""
                     CREATE TABLE IF NOT EXISTS series(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             name TEXT
                             )
                     """)
    
    def drop_series(self):
        self.drop("series")
    
    def create_users_table(self):
        """create a users table which contains all details about users and 
        link to the series they watch"""
        self.tables["users"] = Table(["name"])
        self.execute("""
                     CREATE TABLE IF NOT EXISTS users(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             name TEXT
                             )
                     """)
    
    def drop_users(self):
        self.drop("users")

    def insert(self,table,insert_dict):
        if not self.tables[table].is_same_columns(list(insert_dict.keys())):
            raise(ValueError("wrong columns for the table {}".format(table)))
        keys = self.tables[table].comma_columns
        print("INSERT INTO "+ table + " (" + keys + ") VALUES(" +
                     ",".join(map(str,["'"+ str(x) + "'" for x in insert_dict.values()])) +
                     ")")
        self.execute("INSERT INTO "+ table + " (" + keys + ") VALUES(" +
                     ",".join(map(str,["'"+ str(x) + "'" for x in insert_dict.values()])) +
                     ")")
        
    def select(self,sql):
        self.execute(sql)
    
    def fetchall(self):
        return(self.cursor.fetchall())

    def fetchone(self):
        return(self.cursor.fetchone())

#for now there is still a problem(minor), Table is erased at each run while 
# the content of columns is used by Database.insert

class Table:
    def __init__(self,columns):
        self._columns = columns
    
    def _get_columns(self):
        return(self._columns)
    columns = property(_get_columns)
    
    def _get_comma_columns(self):
        return(','.join(map(str,self._columns)))
    comma_columns = property(_get_comma_columns)
    
    def _get_dot_columns(self):
        return(','.join(map(str,[":" + x for x in self._columns])))
    dot_columns = property(_get_dot_columns)
    
    def is_same_columns(self,columns):
        return(columns == self._columns)

a = DataBase()
