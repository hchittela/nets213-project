import csv
import os
import time
import math
import random
import requests

from flask import Flask, redirect, render_template, request, session, url_for
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, confirm_login, fresh_login_required)
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from sqlalchemy.dialects.mysql import *


# APP CONFIGURATION ###############################################################
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# DATABASE MODELS #################################################################
class Challenges(db.Model):
	__tablename__ = 'challenges'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	user_email = db.Column(db.String(200))
	url_1 = db.Column(db.String(200))
	url_2 = db.Column(db.String(200))
	task1_id = db.Column(db.Integer)
	num_voters = db.Column(db.Integer)
	task1_completed = db.Column(db.Boolean, default=False)

	def __init__(self, name, url_1, url_2, num_voters, email):
		self.name = name
		self.url_1 = url_1
		self.url_2 = url_2
		self.num_voters = num_voters
		self.user_email = email

class User(db.Model):
	__tablename__ = 'users'
	email = db.Column(db.String, primary_key=True)
	password = db.Column(db.String)
	name = db.Column(db.String)
		
	def __init__(self, email, password, name):
		self.email = email
		self.password = password
		self.name = name

	def is_active(self):
		return True

	def get_id(self):
		return self.email

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

# HELPER FUNCTIONS ################################################################
def get_session_error():
	error = ""
	if 'error' in session:
		error = session['error']
	session[error] = ""
	return error

def is_valid_url(url):
	try:
		request = requests.get(url)
		if request.status_code == 200:
			return True
		else:
			return False 
	except requests.exceptions.RequestException as e:
		return False


# USER LOADER #####################################################################
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


# APP ROUTES ######################################################################
@app.route('/', methods = ['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('responses'))
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if not email or not password:
			session['error'] = "Please enter an email and password."
			return redirect(url_for('index'))
		user = User.query.get(email)
		if user:
			if login_user(user):
				return redirect(url_for('responses'))
		else:
			session['error'] = "Invalid email or password. Please try again."
			return redirect(url_for('index'))
	return render_template('index.html', error = get_session_error())

@app.route('/logout', methods=['GET','POST'])
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/signup', methods = ['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		if not name or not email or not password:
			session['error'] = "Please enter a name, email, and password."
			return redirect(url_for('signup'))
		if User.query.get(email):
			session['error'] = "Sorry, this email address already exists."
			return render_template('signup.html', error = get_session_error())
		new_user = User(email, password, name)
		db.session.add(new_user)
		db.session.commit()
		if login_user(new_user):
			return redirect(url_for('responses'))
		else:
			return redirect(url_for('index'))
	return render_template('signup.html', error = get_session_error())

@app.route('/responses')
def responses():
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	return render_template('responses.html', error = get_session_error())

@app.route('/upload', methods=['GET','POST'])
def upload():
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	if request.method == 'POST':
		name = request.form['name']
		
		# Check first url
		url1 = request.form['url1']
		if not is_valid_url(url1):
			session['error'] = "Sorry, the first URL was not valid. Please enter a valid URL."
			return render_template('upload.html', error = error)
		
		# Check second url
		url2 = request.form['url2']
		if not is_valid_url(url2):
			session['error'] = "Sorry, the second URL was not valid. Please enter a valid URL."
			return render_template('upload.html', error = error)
		
		num_voters = request.form['num-voters']
		new_challenge = Challenges(name, url1, url2, num_voters, current_user.email)
		db.session.add(new_challenge)
		db.session.commit()
	return render_template('upload.html', error = get_session_error())

if __name__ == '__main__':
	app.run(debug=True)