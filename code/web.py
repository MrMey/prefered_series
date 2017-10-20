# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-


from flask import Flask,request,render_template
import request_database
import request_api
import user
import series

class WebSite(Flask):
    def __init__(self):
        Flask.__init__(self,__name__)
        self.add_url_rule(rule = '/main',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/login',endpoint = 'login',view_func = self.login, methods=['POST'])
        self.add_url_rule(rule = '/details/<serie>',endpoint = 'details',view_func = self.details, methods=['GET','POST'])
        self.add_url_rule(rule = '/search_serie',endpoint = 'search_serie',view_func = self.search_serie, methods=['POST'])

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

class Controler():
    def __init__(self):
        self.req_database = request_database.DataBase()
        self.series = series.Series()
        self.add_user()
        self.act_series()
        self.series = series.Series()
        
    def add_user(self):
        self.user = user.User("paul",1)
    
    def act_series(self):
        self.user.series = self.req_database.select_series_from_user(self.user.user_id)
    
    def add_series(self):
        try:
            [name,image,id] = self.series.get_basics()
            serie_id = self.req_database.add_series(name,image,id)
        except:
            True
        try:
            self.req_database.add_series_to_user(self.user.user_id,serie_id)
        except:
            True
        
class FullControler(WebSite,Controler):
    def __init__(self):
        Controler.__init__(self)
        WebSite.__init__(self)
        
    def main(self):
        """ **routes**
            '/main'
        """ 
        self.act_series()
        return(render_template('main.html',**{"series_list":self.user.series}))

    def search_serie(self):
        """ **routes**
            '/search_serie'
        """
        if request.method == 'POST':
            series_list = request_api.RequestAPI.research(request.form['serie'])
            return(render_template('search.html',series_list = series_list))
        return(0)

    def details(self, serie = ""):
        """ **routes**
            '/details/<serie>'
        """
        try:
            serie = int(serie)
        except:
            raise(TypeError("serie id must be an int"))

            
        if request.method == "POST":
            self.add_series()
        else:
            self.series.id = serie
            self.series.initiate_from_details(request_api.RequestAPI.get_details(serie))
        return(render_template('details.html',series = self.series))
    
if __name__ == '__main__':
    app = FullControler()
    app.run(debug=True)
