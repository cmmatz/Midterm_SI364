from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

class AppForm(FlaskForm):
	search = StringField('What is your favorite song?', validators=[Required()])
	artist = StringField('What is your favorite artist?')
	submit = SubmitField('Submit')

@app.route('/')
def home():
    searchForm = AppForm()
    return render_template('practice-form.html', form=searchForm)

@app.route('/myfav')
def fav():
    response = make_response("<h1> My favorite Song is Hey Jude by the Beatles </h1>")
    response.set_cookie("hey","jude")
    return response

@app.route('/result', methods = ['POST'])
def result():
    form = AppForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        search = form.search.data
        artist = form.artist.data
        base_url = "https://itunes.apple.com/search?term=" 
        url = base_url + search + artist
        x = requests.get(url).text
        return render_template("result.html", data = json.loads(x)["results"], numresults = len(json.loads(x)["results"]))
    flash('All fields are required!')
    return redirect(url_for('index'))

@app.route('/music/<album>')
def music(album):
	base_url = "https://itunes.apple.com/search?term=" 
	url = base_url + album
	x = requests.get(url).text
	return render_template("album.html", data = json.loads(x)["results"][0])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def internal_server_error(e):
    return render_template('405.html'), 405

#To trigger the 405 error you have to go straight /result



