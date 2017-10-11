# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 15:42:05 2017

@author: Mr_Mey
"""

from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
    return(render_template('main.html',series = [[1,"breaking bad"],[2,"howimetyourmother"]]))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return(render_template('login.html'))

@app.route('/details')
@app.route('/details/<serie>')
def details(serie = ""):
    if serie == "":
        serie = "Veuillez choisir une serie"
    return(render_template('details.html',serie_name = serie))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return "Vous avez envoyé : {msg}".format(msg=request.form['msg'])
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

@app.route('/search_serie', methods=['GET', 'POST'])
def search_serie():
    if request.method == 'POST':
        return(render_template('search.html',serie = request.form['serie'],series_id =str(1)))
    return(0)


if __name__ == '__main__':
    app.run(debug=True)
