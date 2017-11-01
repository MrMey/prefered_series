# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-

import sqlite3
import exceptions as e
import re

class RequestDB:
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

    -add_series(name, image, id_api):
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
        self.__connector = sqlite3.connect('../storage/series.db', check_same_thread=False)
        self.__cursor = self.__connector.cursor()
        self.tables = {}

        self.tables["series"] = Table(["name", "image", "id_api"])
        self.tables["users"] = Table(["login", "name"])
        self.tables["users_series"] = Table(["user_id", "series_id"])

    def __del__(self):
        """ when you del the table, makes sure the connection is closed, at
        the end of the db call you should delete the database"""
        self.__connector.close()
        del (self)

    # General methods

    def __commit(self):
        """ apply on the database the instruction that was send to the cursor
        """
        self.__connector.commit()

    def execute(self, instruction):
        """
        sends an SQL request to the connector
        Warning any sql is accepted for now (DROP...)
        
        Parameters:
            instruction : sql request
        """
        if(not isinstance(instruction,str)):
            raise(e.DataBaseError("instruction must be a sql string in execute"))
        print(instruction)
        self.__cursor.execute(instruction)
        self.__commit()

    def insert(self, table, insert_dict):
        """ insert a row in the chosen table with the values from insert_dict
        
        Parameters:
            table(string):
                table from the database
            insert_dict (dict):
                dictionary where the keys are the columns of the database and
                the values are the values you want to insert
        """
        if not isinstance(insert_dict,dict):
            raise(TypeError("insert_dict must be a dict"))
        if not table in self.tables:
            raise(e.DataBaseError("table is not set in DataBase.tables"))
        if not table in self.get_tables_name():
            raise(e.DataBaseError("table does not exist"))
        if not self.tables[table].is_same_columns(list(insert_dict.keys())):
            raise (e.DataBaseError("wrong columns for the table {}".format(table)))
        keys = self.tables[table].comma_columns
        self.execute("INSERT INTO " + table + " (" + keys + ") VALUES(" +
                     ",".join(map(str, ["'" + str(x) + "'" for x in insert_dict.values()])) +
                     ")")

    def select(self, sql):
        """ execute a SELECT sql query
        """
        if re.match("^[Ss][Ee][Ll][Ee][Cc][Tt]",sql) == None:
            raise(e.DataBaseError("invalid SELECT request"))
        self.execute(sql)

    def fetchall(self):
        """ returns all the result rows from the last execute command
        """
        return (self.__cursor.fetchall())

    def fetchone(self):
        """ returns the first result rows from the last execute command
        """
        return (self.__cursor.fetchone())

    def __drop(self, table):
        """drop table - DO NOT EXECUTE THIS WITHOUT BEING SURE"""
        if not isinstance(table,str):
            raise(TypeError('table must be a string'))
        self.execute("""DROP TABLE """ + table)

    def get_tables_name(self):
        """ returns the name of the existing tables in the .db file
        """
        
        self.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
        tables_name = self.fetchall()
        return ([x[0] for x in tables_name[1:]])

    def is_in_table(self, table, attr, value):
        self.execute("""
                     SELECT * FROM {0} 
                     WHERE {1} = '{2}'
                     """.format(table, attr, value))
        return (len(self.fetchall()) != 0)
    
    def is_not_empty(self,sql):
        self.execute(sql)
        return (len(self.fetchall()) != 0)

    def get_last_insert_id(self):
        return (self.__cursor.lastrowid)

    def count_rows(self, table, attr):
        self.execute("""SELECT COUNT({0}) FROM {1}""".format(attr, table))
        return (self.fetchall()[0][0])

    # table Specific methods
    def create_series_table(self):
        """create a series table which contains all details about series"""
        if "series" in self.get_tables_name():
            raise(e.DataBaseError("series table already exists"))
        self.execute("""
                     CREATE TABLE IF NOT EXISTS series(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             name TEXT,
                             image TEXT,
                             id_api INT
                             )
                     """)

    def drop_series(self):
        self.__drop("series")

    def create_users_table(self):
        """create a users table which contains all details about users and 
        link to the series they watch
        primary key : login
        """
        if "users" in self.get_tables_name():
            raise(e.DataBaseError("users table already exists"))
        self.execute("""
                     CREATE TABLE IF NOT EXISTS users(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             login  TEXT,
                             name TEXT
                             )
                     """)

    def drop_users(self):
        self.__drop("users")

    def create_users_series_table(self):
        """create a users-series relation table"""
        if "users_series" in self.get_tables_name():
            raise(e.DataBaseError("users_series table already exists"))
        self.execute("""
                     CREATE TABLE IF NOT EXISTS users_series(
                             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                             user_id TEXT,
                             series_id TEXT
                             )
                     """)

    def drop_users_series(self):
        self.__drop("users_series")

    def delete_users_series(self, user_id, series_id):
        try:
            user_id = int(user_id)
        except:
            raise(ValueError("user_id must be an int or a string that could be\
                             cast into an int"))
        try:
            series_id = int(series_id)
        except:
            raise(ValueError("series_id must be an int or a string that could be\
                             cast into an int"))
        self.execute("""DELETE FROM users_series 
                     WHERE user_id = {} 
                     AND series_id = {}
                     """.format(user_id,series_id))

    def add_user(self, login, name):
        if not isinstance(login,str):
            raise(TypeError('login must be a string'))
        if not isinstance(name, str):
            raise(TypeError('name must be a string'))
        if self.is_in_table("users", "login", login):
            raise (e.DataBaseError("instance already in user table"))
        else:
            self.insert("users", {"login": login, "name": name})
        return (self.__cursor.lastrowid)
    
    def delete_users(self, login):
        if not isinstance(login,str):
            raise(TypeError('login must be a string'))
        if not self.is_in_table("users", "login", login):
            raise (e.DataBaseError("this user does not exist in the table"))

        self.execute("""DELETE FROM users 
                     WHERE login = '{}'
                     """.format(login))

    def add_series(self, name, image, id_api):
        if not isinstance(name,str):
            raise(TypeError('name must be a string'))
        if not isinstance(image, str):
            raise(TypeError('image must be a string'))
        try:
            id_api = int(id_api)
        except:
            raise(ValueError("id_api must be an int or a string that could be\
                             cast into an int"))
        if (self.is_in_table("series", "name", name)):
            raise (e.DataBaseError("instance already in series table"))
        else:
            self.insert("series", {"name": name, "image": image, "id_api": id_api})
        return (self.__cursor.lastrowid)

    def add_series_to_user(self, user_id, series_id):
        if not isinstance(user_id,int):
            raise(TypeError('user_id must be an int'))
        if not isinstance(series_id,int):
            raise(TypeError('series_id must be an int'))
        if(self.is_not_empty("""SELECT * FROM users_series 
                             WHERE user_id = {}
                             AND series_id = {}
                             """.format(user_id,series_id))):
            raise(e.DataBaseError('instance already in user_series table'))
        else:
            self.insert("users_series", {"user_id": user_id, "series_id": series_id})
        return (self.__cursor.lastrowid)

    def select_series_from_user(self, user_id):
        if not isinstance(user_id,int):
            raise(TypeError('user_id must be an int'))
        self.execute("""SELECT S.id_api,S.name,S.image FROM 
                     series S JOIN
                     (SELECT * FROM users_series U WHERE U.user_id = {}) U
                     ON
                     U.series_id = S.id
                     """.format(user_id))
        return (self.fetchall())
    
    def get_series_id_by_name(self,name):
        if not isinstance(name,str):
            raise(TypeError('name must be an string'))
        self.execute("""SELECT id from series 
                     WHERE name = '{}'
                     """.format(name))
        result = self.fetchall()
        if(len(result) > 1):
            raise(e.DataBaseError('Multiple series with the same name'))
        if(len(result) < 1):
            raise(e.DataBaseError('No instance with this name'))
        return(result[0][0])
    
    def get_users_by_login(self,attr,login):
        if not attr in self.tables['users'].columns:
            raise(e.InvalidFieldError('attr must be a column in users'))
        if not isinstance(login,str):
            raise(e.DataBaseError('login must be a string'))
        self.execute("""SELECT {} from users 
                     WHERE login = '{}'
                     """.format(attr,login))
        result = self.fetchall()
        if(len(result) > 1):
            raise(e.DataBaseError("Multiple series with the same name"))
        if(len(result) < 1):
            raise(e.DataBaseError("User doesn't exist"))
        return(result[0][0])
    
    def tuple_to_list(self,list_tuples):
        return([[x[y] for y in range(len(x))] for x in list_tuples])


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
        if(not(isinstance(columns,list))):
            raise(e.DataBaseError("columns must be a list in Table.__init__"))
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
        if(not(isinstance(columns,list))):
            raise(e.DataBaseError("columns must be a list in is_same_columns parameters"))
        return (sorted(columns) == sorted(self._columns))

if __name__ == '__main__':
    a = RequestDB()
