# Authors: Elodie Ikkache, Romain Meynard, Jessica Cohen
#
# version 1.0
# -*- coding: utf-8 -*-


from flask import Flask,request,render_template


class WebSite(Flask):
    def __init__(self):
        Flask.__init__(self,__name__)
        self.add_url_rule(rule = '/',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/main',endpoint = 'main',view_func = self.main)
        self.add_url_rule(rule = '/login',endpoint = 'login',view_func = self.login, methods=['GET', 'POST'])
        self.add_url_rule(rule = '/details',endpoint = 'details',view_func = self.details)
        self.add_url_rule(rule = '/details/<serie>',endpoint = 'details',view_func = self.details)
        self.add_url_rule(rule = '/search_serie',endpoint = 'search_serie',view_func = self.search_serie, methods=['POST'])

    def main(self):
        """ **routes**
            '/'
            '/main'
        """
        return(render_template('main.html',series=[[1,"breaking bad"],[2,"howimetyourmother"]]))

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

app = WebSite()
if __name__ == '__main__':
    app.run(debug=True)
