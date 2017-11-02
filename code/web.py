# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-


from flask import Flask,request,render_template,session
import request_database
import request_api
import user
import series

class WebSite(Flask):
    def __init__(self):
        Flask.__init__(self,__name__)
        self.secret_key = 'super secret key'
        self.add_url_rule(rule = '/main',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/login',endpoint = 'login',view_func = self.login, methods=['GET','POST'])
        self.add_url_rule(rule = '/signup',endpoint = 'signup',view_func = self.signup, methods=['GET','POST'])
        self.add_url_rule(rule = '/details/<serie>',endpoint = 'details',view_func = self.details, methods=['GET','POST'])
        self.add_url_rule(rule = '/search_serie',endpoint = 'search_serie',view_func = self.search_serie, methods=['POST'])
        self.add_url_rule(rule = '/browse',endpoint = 'browse',view_func = self.browse)

    def main(self):
        """ **routes**
            '/main'
        """
        test = {"series_list":[[1,"breaking bad"],[2,"howimetyourmother"]]}
        return(render_template('main.html',**test))

    def login(self):
        """ **routes**
            '/login'
        """
        return(render_template('login.html'))

    def details(self, serie = ""):
        """ **routes**
            '/details'
            '/details/<serie>'
        """
        if serie == "":
            serie = "Veuillez choisir une serie"
        return(render_template('details.html',serie_name = serie))

    def search_serie(self):
        """ **routes**
            '/search_serie'
        """
        if request.method == 'POST':
            return(render_template('search.html',serie = request.form['serie'],series_id =str(1)))
        return(0)

    def browse(self):
        """ **routes**
            '/browse'
        """
        return(render_template('browse.html'))

    def signup(self):
        """ **routes**
            '/signup'
        """
        return(render_template('signup.html'))

class Controler():
    def __init__(self):
        self.req_database = request_database.RequestDB()
        self.series = series.Series()
        self.user = user.User()

    def act_series(self):
        self.user.series = self.req_database.select_series_from_user(self.user.id)

    def add_series(self,user_id):
        [name,image,id] = self.series.get_basics()
        try:
            serie_id = self.req_database.add_series(name,image,id)
        except:
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

class FullControler(WebSite,Controler):
    def __init__(self):
        Controler.__init__(self)
        WebSite.__init__(self)

    def main(self):
        """ **routes**
            '/main'
        """

        if 'login' not in session:
            return(render_template('login.html'))
        else:
            return(render_template('main.html',**{"series_list":
                self.req_database.select_series_from_user(session['user_id'])}))

    def search_serie(self):
        """ **routes**
            '/search_serie'
        """
        if request.method == 'POST':
            series_list = series.Series.missing_basic(request_api.RequestAPI.research(request.form['serie']))
            return(render_template('search.html',series_list = series_list))
        return(0)

    def login(self):
        """ **routes**
            '/login'
        """
        if request.method == 'POST':
            if self.req_database.is_in_table("users","login",request.form["login"]):
                session['login'] = request.form["login"]
                session['user_id'] = self.req_database.get_users_by_login('id',session['login'])
                self.user.initiate(session['login'],session['user_id'])
                return(render_template('main.html'))
            else:
                return(render_template('login.html', message = "invalid login"))
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
            session['login'] = request.form["login"]
            session['user_id'] = self.req_database.get_users_by_login('id',session['login'])
            self.user.initiate(session['login'],session['user_id'])
            return(render_template('main.html'))

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
            if('login' not in session):
                return(render_template('login.html'))
            if(request.form['submit'] == "Add to favorites"):
                self.add_series(session['user_id'])
            if(request.form['submit'] == "Remove from favorites"):
                self.remove_series(session['user_id'])
        else:
            # set the current serie_id in the series class
            self.series.id = serie
            # set the rest of the attributes
            self.series.initiate_from_details(request_api.RequestAPI.get_details(serie))
        return(render_template('details.html',series = self.series))

if __name__ == '__main__':
    app = FullControler()
    app.run(debug=True)
