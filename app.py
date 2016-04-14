import csv
import os
import time
import math
import random

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
	url1 = db.Column(db.String(200))
	url2 = db.Column(db.String(200))
	task1_id = db.Column(db.Integer)
	num_voters = db.Column(db.Integer)
	task1_completed = db.Column(db.Boolean, default=False)

	def __init__(self, name, url1, url2, num_voters):
		self.id = id
		self.name = name
		self.url1 = url1
		self.url2 = url2
		self.num_voters = num_voters
		self.user_email = current_user.user.email

class User(db.Model):
	__tablename__ = 'users'
	email = db.Column(db.String, primary_key=True)
	password = db.Column(db.String)
	name = db.Column(db.String)
		
	def __init__(self, email, password, name, authenticated):
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


# USER LOADER #####################################################################
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


# APP ROUTES ######################################################################
@app.route('/', methods = ['GET', 'POST'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('welcome'))
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			session['error'] = "Please enter a username and password."
			return redirect(url_for('index'))
		user = User.query.get(email)
		if login_user(user):
			return redirect(url_for('welcome'))
		else:
			session['error'] = "Invalid username or password. Please try again."
			return redirect(url_for('index'))
	return render_template('index.html', error = get_session_error())

@app.route('/logout', methods=['GET','POST'])
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/signup', methods = ['GET','POST'])
def signup():
	error = None
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		if User.query.get(email):
			session['error'] = "Sorry, this email address already exists."
			return render_template('signup.html', error = error)
		new_user = User(email, password, name)
		db.session.add(new_user)
		db.session.commit()
		if login_user(new_user):
			return redirect(url_for('welcome'))
		else:
			return redirect(url_for('index'))
	return render_template('signup.html', error = get_session_error())

@app.route('/welcome')
def welcome():
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	return render_template('welcome.html', error = get_session_error())

@app.route('/upload', methods=['GET','POST'])
def upload():
	error = None
	if request.method == 'POST':
		name = request.form['name']
		url1 = request.form['url1']
		url2 = request.form['url2']
		num_voters = request.form['num-voters']
		new_challenge = Challenges(name, url1, url2, num_voters)
		db.session.add(new_challenge)
		db.session.commit()
	return render_template('upload.html', error = error)

if __name__ == '__main__':
	app.run(debug=True)