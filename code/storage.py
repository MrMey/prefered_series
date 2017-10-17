# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-

import sqlite3
import exceptions as e


class DataBase:
    """ Manages requests (read and write) to the sqlite database

    **Parameters**
     no parameters

     ** Attributes**
     connector
     cursor
     tables
     

     **Methods**

    - execute(SQL):
        sends an SQL request to the connector
        
    - commit():
        sends the last executed SQL request to the database
    
    - insert(table,insert_dict)
        insert the content of the dictionary in the table. the keys of the
        dict must be the columns of the table
    
    - select(SQL):
        execute an sql request (should be used to select only - should improve 
        this)
    
    - fetchall():
        returns all the rows of the last request results
        
    - fetchone():
        returns one row of the last request results

    - drop(table):
        deletes the table in the database
    
    -get_tables_name():
        returns the name of all the existing tables in the database
    
    -is_in_table(table,value,attr):
        checks if there is a row with attr column equal value
    
    -get_last_insert_id():
        returns the row id of the last inserted row
    
    -count_rows(table,attr):
        returns the numbers of row of non-null attribute in the table
    
    -create_series_table():
        creates a series table in the database with the columns as defined in the
        Table object
    
    -drop_series():
        deletes the series table
    
    -create_user_table():
        creates a user table in the database with the columns as defined in the
        Table object
    
    -drop_user():
        deletes the series table    
        
    -create_users_series_table():
        creates the users_series relation table between user and series
    
    -drop_users_series():
        deletes the users_series table
    
    -add_users(login,name):
        adds a user row in the users table with parameters: login and name
        login is the primary key

    -add_series(name, image):
        adds a series row in the series table with parameters: name
        name is the primary key
    
    -add_series_to_user(user_id,series_id):
        adds the relation between a user and the series he watches in the 
        user_series table using both ids
    
    -select_series_from_user(user_id):
        returns the series a user watches
    
    **Comments**
    By default, IDs in the tables will start at 1
    """

    def __init__(self):
        self.connector = sqlite3.connect('../storage/series.db')
        self.cursor = self.connector.cursor()
        self.tables = {}

        self.tables["series"] = Table(["name", "image"])
        self.tables["users"] = Table(["login", "name"])
        self.tables["users_series"] = Table(["user_id", "series_id"])

    def __del__(self):
        """ when you del the table, makes sure the connection is closed, at
        the end of the db call you should delete the database"""
        self.connector.close()
        del (self)

    # General methods

    def commit(self):
        self.connector.commit()

    def execute(self, instruction):
        print(instruction)
        self.cursor.execute(instruction)
        self.commit()

    def insert(self, table, insert_dict):
        if not self.tables[table].is_same_columns(list(insert_dict.keys())):
            raise (ValueError("wrong columns for the table {}".format(table)))
        keys = self.tables[table].comma_columns
        self.execute("INSERT INTO " + table + " (" + keys + ") VALUES(" +
                     ",".join(map(str, ["'" + str(x) + "'" for x in insert_dict.values()])) +
                     ")")

    def select(self, sql):
        self.execute(sql)

    def fetchall(self):
        return (self.cursor.fetchall())

    def fetchone(self):
        return (self.cursor.fetchone())

    def drop(self, table):
        """drop one table - DO NOT EXECUTE THIS WITHOUT BEING SURE"""
        self.execute("""DROP TABLE """ + table)

    def get_tables_name(self):
        self.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        tables_name = self.fetchall()
        return ([x[0] for x in tables_name[1:]])

    def is_in_table(self, table, attr, value):
        self.execute("""SELECT * FROM {0} WHERE {1} = '{2}'""".format(table, attr, value))
        return (len(self.fetchall()) != 0)

    def get_last_insert_id(self):
        return (self.cursor.lastrowid)

    def count_rows(self, table, attr):
        self.execute("""SELECT COUNT({0}) FROM {1}""".format(attr, table))
        return (self.fetchall()[0][0])

    # table Specific methods
    def create_series_table(self):
        """create a series table which contains all details about series"""

        self.execute("""
                     CREATE TABLE IF NOT EXISTS series(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             name TEXT,
                             image TEXT
                             )
                     """)

    def drop_series(self):
        self.drop("series")

    def create_users_table(self):
        """create a users table which contains all details about users and 
        link to the series they watch
        primary key : login
        """

        self.execute("""
                     CREATE TABLE IF NOT EXISTS users(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             login  TEXT,
                             name TEXT
                             )
                     """)

    def drop_users(self):
        self.drop("users")

    def create_users_series_table(self):
        """create a users-series relation table"""
        self.execute("""
                     CREATE TABLE IF NOT EXISTS users_series(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             user_id TEXT,
                             series_id TEXT
                             )
                     """)

    def drop_users_series(self):
        self.drop("users_series")

    def add_user(self, login, name):
        if (self.is_in_table("users", "login", login)):
            raise (e.DataBaseError("instance already in user table"))
        else:
            self.insert("users", {"login": login, "name": name})
        return (self.cursor.lastrowid)

    def add_series(self, name, image):
        if (self.is_in_table("series", "name", name)):
            raise (e.DataBaseError("instance already in series table"))
        else:
            self.insert("series", {"name": name, "image": image})
        return (self.cursor.lastrowid)

    def add_series_to_user(self, user_id, series_id):
        self.insert("users_series", {"user_id": user_id, "series_id": series_id})
        return (self.cursor.lastrowid)

    def select_series_from_user(self, user_id):
        self.execute("""SELECT S.name FROM 
                     (SELECT * FROM users_series U WHERE U.id = user_id) U
                     JOIN
                     series S
                     ON
                     U.series_id = S.id
                     """)
        return (self.fetchall())


class Table:
    """ Simple class we use to manage some table methods.
    
    Especially : it keeps track of the columns of the table and can return it 
    with different format used in Database.insert

    **Parameters**
     column names of the table

     ** Attributes**
     columns : column names
     comma_columns : string build with column name : 'col1,col2,col3'
     dot_columns : string build with column name: ':col1,:col2,:col3'

     """

    def __init__(self, columns):
        self._columns = columns

    def _get_columns(self):
        return (self._columns)

    columns = property(_get_columns)

    def _get_comma_columns(self):
        return (','.join(map(str, self._columns)))

    comma_columns = property(_get_comma_columns)

    def _get_dot_columns(self):
        return (','.join(map(str, [":" + x for x in self._columns])))

    dot_columns = property(_get_dot_columns)

    def is_same_columns(self, columns):
        return (columns == self._columns)


a = DataBase()
