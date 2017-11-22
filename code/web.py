# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-


from flask import Flask,request,render_template,session,redirect,url_for
import datetime

import request_database
import request_api
import series
import exceptions as e
from wtforms import Form, BooleanField, TextField, validators
from threading import Thread
import time

class User:
    """class we use to manage the session we settled in the user browser.

    **Parameters**


    **Attributes**
     session : a flask-session

    **Methods**
    is_logged : return true if the key 'login' is in the user session
    log_in(login,user_id) : store user login and user_id in the session
    log_out : remove everything from the session
    is_subscribed(api_id) : returns true if the user is subscribed to the series
    order_schedule : orders the schedule by hour and by day
     """
    def __init__(self):
        """
        the browser session (see session in Flask) is defined as an attribute
        of user object. It is a dict linked to the browser session.
        """
        self._session = session
        self._series = []
        self._schedule = {}

    def is_logged(self):
        """
        if the user is logged in then the key login must be in session
        """
        return('login' in self._session)

    def log_out(self):
        """
        delete all keys from the session attribute
        """
        keys = list(self._session.keys())
        for key in keys:
            del(self._session[key])

    def log_in(self,login,user_id):
        """
        add login and user_id in the session attribute
        """
        self._session['login'] = login
        self._session['user_id'] = user_id

    def _get_user_id(self):
        return(self._session['user_id'])
    user_id = property(_get_user_id)

    def _get_login(self):
        return(self._session['login'])
    login = property(_get_login)

    def _get_series(self):
        """
        note : series must be actualized at each change in the user_series tables
        """
        return(self._series)

    def _set_series(self,series):
        if not isinstance(series,list):
            raise(TypeError("series must be a list"))
        # we sort the series list by alphabetical order for the name
        self._series = sorted(series, key = lambda k : k[1])
    series = property(_get_series,_set_series)

    def _get_schedule(self):
        return(self._schedule)

    def _set_schedule(self, schedule):
        """
        schedule as a format :
            [(id_api,name,image,status,episode,season,image_episode,
            next_date,next_time) for each series
            ]
        The format is changed before storing to:
            {'today':[[id_api,name,image,status,episode,season,image_episode,
            next_date,next_time for each series]],
            'today+1':[[]],
            'today+2':[[]]} for the next 7 days.
        Then for each day, the series are sorted by time.
        """
        self._schedule = {}
        
        #create next 7 days keys
        for d in range(0, 7):
            date =str(datetime.date.today() + datetime.timedelta(days = d))
            self._schedule[date] = []
        
        #change format
        for diff in schedule:
            if diff[7] in self._schedule.keys():
                self._schedule[diff[7]].append([diff[0],
                                           diff[1],
                                           diff[2],
                                           diff[4],
                                           diff[5],
                                           diff[6],
                                           diff[8]])
        #sort by time
        for day in self._schedule.keys():
            if len(self._schedule[day]) > 1:
                self._schedule[day] = sorted(self._schedule[day], key = lambda k:k[6])
    schedule = property(_get_schedule,_set_schedule)


    def is_subscribed(self, api_id):
        """
        return true if the api_id of the series is in self.series
        """
        for series in self._series:
            if series[0] == api_id:
                return(True)
        return(False)


class WebSite(Flask):
    """ class which manages the web routes definition. It is basicially
    equivalent to the Flask class
    """
    def __init__(self):
        """
        Every route must be defined here with the endpoint, the corresponding
        function and the authorized methods. It's the equivalent of the usual
        @app.route decorator.
        """
        Flask.__init__(self,__name__)
        self.secret_key = 'super secret key'
        self.add_url_rule(rule = '/main',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/login',endpoint = 'login',view_func = self.login, methods=['GET','POST'])
        self.add_url_rule(rule = '/signup',endpoint = 'signup',view_func = self.signup, methods=['GET','POST'])
        self.add_url_rule(rule = '/details/<serie>',endpoint = 'details',view_func = self.details, methods=['GET','POST'])
        self.add_url_rule(rule = '/search_serie',endpoint = 'search_serie',view_func = self.search_serie, methods=['POST'])


class Controler():
    """ Class which creates and manages the non-web object (RequestDB,
    User,Series)

    **Parameters**

     **Attributes**
     req_database : RequestDB object
     series : Series object
     user : User object

    **Methods**
    add_series:
        Add a series and bind it to the user
    remove_series:
        Unbind a series from a user
     """

    def __init__(self,req_database):
        self.req_database = req_database
        self.series = series.Series()
        self.user = User()
        
    def add_series(self,user_id):
        """
        first it tries to add a series in the series database
        then it tries to add a entry in the user_series relation table
        if the series is still running then it updates the next diffusion
        information
        """
        
        [name,image,id,status] = self.series.get_basics()
        # tries to add a entry in the series db
        try:
            serie_id = self.req_database.add_series(name,image,id,status)
        except e.AlreadyExistingInstanceError:
            serie_id = self.req_database.get_series_id_by_name(name)
        
        #tries to add a entry in the user_series relationship
        try:
            self.req_database.add_series_to_user(user_id,serie_id)
        except e.AlreadyExistingInstanceError:
            pass
        
        #if still running then tries to update next diff info
        if status == 'Running':
            self.req_database.update_series(name,request_api.RequestAPI.get_next_diff(id,7))

    def remove_series(self,user_id):
        serie_id = self.req_database.get_series_id_by_name(self.series.name)
        self.req_database.delete_users_series(user_id,serie_id)


class RegistrationForm(Form):
    login = TextField('Login',[validators.Length(min=4,max=20)])
    lastname = TextField('Last Name',[validators.Length(min=6,max=50)])

class FullControler(WebSite,Controler):
    """class we use to manage all the objects.

    **Parameters**


    **Attributes**
     user : User object

    **Methods**
    main :
    calendar :
    search_serie :
    login :
    signup :
    details :
    """

    def __init__(self,req_database):
        Controler.__init__(self,req_database)
        WebSite.__init__(self)
        self.user = User()
        self.form = RegistrationForm()

        
    def main(self):
        """ **routes**
            '/main'
        """
        message = ""
        if not self.user.is_logged():
            return(redirect(url_for('login')))
        else:
            self.user.series = self.req_database.select_series_from_user(self.user.user_id)

            self.user.schedule = self.req_database.select_next_diff_series_from_user(self.user.user_id)
    
            return(render_template('main.html',series_list=self.user.series,
                                   schedule=self.user.schedule,
                                   logged=self.user.is_logged(),
                                   message=message))

    def search_serie(self):
        """ **routes**
            '/search_serie'
        """
        if request.method == 'POST':
            try:
                series_list = series.Series.missing_basic(request_api.RequestAPI.research(request.form['serie']))
                return(render_template('search.html',series_list = series_list,
                                       logged = self.user.is_logged()))
            except e.APIError:
                message = " missing search field"
                return(render_template('search.html',series_list = [],
                                       message = message,
                                       logged = self.user.is_logged()))
        else:
            return(redirect(url_for('login')))

    def login(self):
        """ **routes**
            '/login'
        """
        if request.method == 'POST':
            # if the 'login' button is activated we login else we try to logout
            if 'login' in request.form.keys():
                #check if the login exists in the database
                if self.req_database.is_in_table("users","login",request.form["login"]):
                    self.user.log_in(request.form["login"],
                                       self.req_database.get_users_by_login('id',request.form["login"]))
                    return(redirect(url_for('main')))
                else:
                    return(render_template('login.html', message = "Invalid login, try to login again or sign in"))
            else:
                self.user.log_out()
        return(render_template('login.html', message = "Please login or sign in"))

    def signup(self):
        """ **routes**
            '/signup'
        """
        message = "Please signup"
        if request.method == 'POST':
            #check in the database if the login is available
            if len(request.form['login']) < 3:
                message = "Enter a login with at least 4 characters"
            elif len(request.form['username']) < 3:
                message = "Enter a username with at least 4 characters"
            elif self.req_database.is_in_table("users","login",request.form['login']):
                message = "Login not available"
            else:
                self.req_database.add_user(request.form['login'],request.form['username'])
                self.user.log_in(request.form['login'],
                                   self.req_database.get_users_by_login('id',request.form['login']))
                return(redirect(url_for('main')))

        return(render_template('signup.html',
                               message = message,
                               form = self.form))


    def details(self, serie = ""):
        """ **routes**
            '/details/<serie>'
        """
        message = ""
        try:
            serie = int(serie)
        except:
            raise(TypeError("serie id must be an int"))

        # add/remove from favorites buttons
        if request.method == "POST":
            if not self.user.is_logged():
                return(redirect(url_for('login')))
            if(request.form['submit'] == "Add to favorites"):
                try:
                    self.add_series(session['user_id'])
                except:
                    message = "sorry we couldn't link this series with your \
                    account"
            if(request.form['submit'] == "Remove from favorites"):
                try:
                    self.remove_series(session['user_id'])
                except:
                    message = "sorry we couldn't remove this series from \
                    your account"
        else:
            # set the current serie_id in the series class
            self.series.id = serie
            # set the rest of the attributes
            try:
                self.series.initiate_from_details(request_api.RequestAPI.get_details(serie))
            except e.UnavailableService:
                message = "API is unavailable, please try later"
        if self.user.is_logged():
            self.user.series = self.req_database.select_series_from_user(self.user.user_id)
        return(render_template('details.html',series = self.series,
                               dict_episodes=request_api.RequestAPI.get_episodes(serie),
                               seasons=request_api.RequestAPI.get_seasons(serie),
                               crew=request_api.RequestAPI.get_crew(serie),
                               cast=request_api.RequestAPI.get_cast(serie),
                               logged = self.user.is_logged(),
                               subscribed = self.user.is_subscribed(serie),
                               message = message))

class ThreadDB(Thread):
    """class which contains a second thread which updates the next TV shows.
    At the launch of the project and every day, it tries to update all the
    databases.

    **Parameters**
    req_database

    **Attributes**
     req_database : User object

    **Methods**
    run : every 12 hours it tries to update the 'running' tv shows in the database 
    """
    def __init__(self,req_database):
        Thread.__init__(self)
        self.req_database = req_database
        
    def run(self):
        next_update = datetime.datetime(datetime.datetime.now().year,
                                        datetime.datetime.now().month,
                                        datetime.datetime.now().day)        
        while True:
            if datetime.datetime.now() >= next_update:
                print('starting update')
                # update only the running tv shows
                for item in self.req_database.select_running_series():
                    self.req_database.update_series(item[1],request_api.RequestAPI.get_next_diff(item[0],7))
                    #waiting to avoid reaching the api limit
                    time.sleep(10)
                # postpone the next_update of one day
                next_update = next_update + datetime.timedelta(days = 1)
                print('update done')
            # wait 12 hours before triying to update the database
            time.sleep(3600*12)

if __name__ == '__main__':
    # req_database is created outside to be accessible by both threads
    req_database = request_database.RequestDB()
    thread = ThreadDB(req_database)
    app = FullControler(req_database)
    thread.start()
    app.run(debug=True)

