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

class WebSite(Flask):
    """ class which manages the web routes definition. It is basicially
    equivalent to the Flask class
    """
    def __init__(self):
        """
        Every route must be defined here with the endpoint, the corresponding
        function and the authorized methods
        """
        Flask.__init__(self,__name__)
        self.secret_key = 'super secret key'
        self.add_url_rule(rule = '/main',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/login',endpoint = 'login',view_func = self.login, methods=['GET','POST'])
        self.add_url_rule(rule = '/signup',endpoint = 'signup',view_func = self.signup, methods=['GET','POST'])
        self.add_url_rule(rule = '/details/<serie>',endpoint = 'details',view_func = self.details, methods=['GET','POST'])
        self.add_url_rule(rule = '/search_serie',endpoint = 'search_serie',view_func = self.search_serie, methods=['POST'])

class Controler():
    """ Class which creates and manages the non-web object (RequestDB, Series,
    User)
    
    **Parameters**

     **Attributes**
     req_database : RequestDB object
     series : Series object
     user : User object

    **Methods**
    act_series: 
        set the user.series to the the values currently stored in the 
        DB. user.series is a list of 3-element lists containing the api_id,name,
        image url of the user's favorite series
    add_series:
        Add a series and bind it to the user
    remove_series:
        Unbind a series from a user
     """
    
    def __init__(self):
        self.req_database = request_database.RequestDB()
        self.series = series.Series()
        self.user = User()
        
    def act_series(self):
        self.user.series = self.req_database.select_series_from_user(self.user.id)

    def add_series(self,user_id):
        [name,image,id] = self.series.get_basics()
        try:
            serie_id = self.req_database.add_series(name,image,id)
        except e.AlreadyExistingInstanceError:
            serie_id = self.req_database.get_series_id_by_name(name)

        try:
            self.req_database.add_series_to_user(user_id,serie_id)
        except:
            True

    def remove_series(self,user_id):
        try:
            serie_id = self.req_database.get_series_id_by_name(self.series.name)
            self.req_database.delete_users_series(user_id,serie_id)
        except:
            return(False)

class User:
    """class we use to manage the session we settled in the user browser.

    **Parameters**
    

    **Attributes**
     session : a flask-session

    **Methods**
    is_logged : return true if the key 'login' is in the user session
    order_schedule : orders the schedule by hour and by day
     """
    def __init__(self):
        self._session = session
        self._series = []
        self._schedule = {}
        
    def is_logged(self):
        return('login' in self._session)
    
    def log_out(self):
        keys = list(self._session.keys())
        for key in keys:
            del(self._session[key])
    
    def log_in(self,login,user_id):
        self._session['login'] = login
        self._session['user_id'] = user_id
    
    def _get_user_id(self):
        return(self._session['user_id'])
    user_id = property(_get_user_id)
    
    def _get_login(self):
        return(self._session['login'])
    login = property(_get_login)
    
    def _get_series(self):
        return(self._series)
    
    def _set_series(self,series):
        if not isinstance(series,list):
            raise(TypeError("series must be a list of 3-element lists"))
        
        # for now we don't check the size of the inner lists
        self._series = sorted(series, key = lambda k : k[1])
    series = property(_get_series,_set_series)
    
    def _get_schedule(self):
        return(self._schedule)
    
    def _set_schedule(self, schedule):
        self._schedule = schedule
        self.order_schedule()
    schedule = property(_get_schedule,_set_schedule)
    
    def order_schedule(self):
        """ order schedule by hour
        """
        for day in self._schedule.keys():
            self._schedule[day] = sorted(self._schedule[day],key = lambda k:datetime.datetime.strptime(k['time'],'%H:%M').time())
     
    def is_subscribed(self, api_id):
        for series in self._series:
            if series[0] == api_id:
                return(True)
        return(False)
        
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
    
    def __init__(self):
        Controler.__init__(self)
        WebSite.__init__(self)
        self.user = User()
        
    def main(self):
        """ **routes**
            '/main'
        """

        if not self.user.is_logged():
            return(redirect(url_for('login')))
        else:
            self.user.series = self.req_database.select_series_from_user(self.user.user_id)

            id_list = []
            for item in self.user.series:
                id_list.append(item[0])
            self.user.schedule = request_api.RequestAPI.schedule(id_list)
            
            return(render_template('main.html',series_list=self.user.series,
                                   schedule=self.user.schedule,
                                   logged=self.user.is_logged()))

    def search_serie(self):
        """ **routes**
            '/search_serie'
        """
        if request.method == 'POST':
            try:
                series_list = series.Series.missing_basic(request_api.RequestAPI.research(request.form['serie']))
                return(render_template('search.html',series_list = series_list))
            except e.APIError:
                message = " missing search field"
                return(render_template('search.html',series_list = [],
                                       message = message))
        else:
            return(redirect(url_for('login')))
    

    def login(self):
        """ **routes**
            '/login'
        """
        

        if request.method == 'POST':
            if 'login' in request.form.keys():
                if self.req_database.is_in_table("users","login",request.form["login"]):
                    self.user.log_in(request.form["login"],
                                       self.req_database.get_users_by_login('id',request.form["login"]))
                    return(redirect(url_for('main')))
                else:
                    return(render_template('login.html', message = "invalid login"))
            else:
                self.user.log_out()

                
        return(render_template('login.html', message = "please login or sign in"))

    def signup(self):
        """ **routes**
            '/signup'
        """
        if request.method == 'POST':
            if self.req_database.is_in_table("users","login",request.form["login"]):
                return(render_template('signup.html',message = "Login not available"))
            if request.form["login"] != request.form["login_confirmation"]:
                return(render_template('signup.html',message = "Login confirmation does not match"))

            self.req_database.add_user(request.form['login'],request.form['last_name'])
            self.user.log_in(request.form["login"],
                               self.req_database.get_users_by_login('id',request.form["login"]))
            return(redirect(url_for('main')))

        return(render_template('signup.html'))

    def details(self, serie = ""):
        """ **routes**
            '/details/<serie>'
        """
        try:
            serie = int(serie)
        except:
            raise(TypeError("serie id must be an int"))

        # add/remove from favorites buttons
        if request.method == "POST":
            if not self.user.is_logged():
                return(redirect(url_for('login')))
            if(request.form['submit'] == "Add to favorites"):
                self.add_series(session['user_id'])
            if(request.form['submit'] == "Remove from favorites"):
                self.remove_series(session['user_id'])

        else:
            # set the current serie_id in the series class
            self.series.id = serie
            # set the rest of the attributes
            self.series.initiate_from_details(request_api.RequestAPI.get_details(serie))
        if self.user.is_logged():
            self.user.series = self.req_database.select_series_from_user(self.user.user_id)
        return(render_template('details.html',series = self.series,
                               episodes=request_api.RequestAPI.get_episodes(serie),
                               logged = self.user.is_logged(),
                               subscribed = self.user.is_subscribed(serie)))
    

if __name__ == '__main__':
    app = FullControler()
    app.run(debug=True)
