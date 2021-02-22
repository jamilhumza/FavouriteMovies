from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import requests
import json
from .models import User, Movie
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/favourites', methods=['GET', 'POST'])
def favourites():
    return render_template("favourites.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        query = request.form['title']
        url = 'http://www.omdbapi.com/?API_KEY&s={0}'.format(query)
        response = requests.get(url)
        res = response.json()
    return render_template("results.html", user=current_user, data=res)

@views.route('/addtofavourite', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        movietitle = request.form['title']
        movieposter = request.form['poster']
        new_movie = Movie(title=movietitle,pic=movieposter,user_id=current_user.id)
        db.session.add(new_movie)
        db.session.commit()
    return render_template("home.html", user=current_user, data=movietitle)