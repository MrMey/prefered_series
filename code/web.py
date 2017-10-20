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
        self.add_url_rule(rule = '/',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/main',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/login',endpoint = 'login',view_func = self.login, methods=['POST'])
        self.add_url_rule(rule = '/details',endpoint = 'details',view_func = self.details)
        self.add_url_rule(rule = '/details/<serie>',endpoint = 'details',view_func = self.details)
        self.add_url_rule(rule = '/search_serie',endpoint = 'search_serie',view_func = self.search_serie, methods=['POST'])

    def main(self):
        """ **routes**
            '/'
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
        
        self.add_user()
        self.act_series()
        
    def add_user(self):
        self.user = user.User("paul",0)
    
    def act_series(self):
        self.user.series = self.req_database.select_series_from_user(self.user.user_id)
        
class FullControler(WebSite,Controler):
    def __init__(self):
        Controler.__init__(self)
        WebSite.__init__(self)
        
    def main(self):
        """ **routes**
            '/'
            '/main'
        """ 
        return(render_template('main.html',**{"series_list":self.user.series}))

    def search_serie(self):
        """ **routes**
            '/search_serie'
        """
        if request.method == 'POST':
            series_list = [request_api.RequestAPI.get_basics(request.form['serie'])]
            return(render_template('search.html',series_list = series_list))
        return(0)

    def details(self, serie = ""):
        """ **routes**
            '/details'
            '/details/<serie>'
        """
        if serie == "":
            serie = "Veuillez choisir une serie"
        series_details = request_api.RequestAPI.get_details(serie)
        
        return(render_template('details.html',serie_name = series_details[1]))
    
if __name__ == '__main__':
    app = FullControler()
    app.run(debug=True)
