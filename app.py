import csv
import os
import time
import math
import random
import requests
import crowdflower
import cf_job_create_upload

from flask import Flask, redirect, render_template, request, session, url_for
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, confirm_login, fresh_login_required)
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, desc
from sqlalchemy.dialects.mysql import *
from hashlib import sha1


# APP CONFIGURATION ###############################################################
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

conn = crowdflower.Connection(api_key='Gj3sWX7wb18uHb88BsJC')


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
	description = db.Column(db.String(200))
	votes_1 = db.Column(db.Integer)
	votes_2 = db.Column(db.Integer)

	def __init__(self, name, url_1, url_2, num_voters, email, description, votes_1, votes_2):
		self.name = name
		self.url_1 = url_1
		self.url_2 = url_2
		self.num_voters = num_voters
		self.user_email = email
		self.description = description
		self.votes_1 = votes_1
		self.votes_2 = votes_2

class Comments(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	challenge_id = db.Column(db.Integer)
	individual_id = db.Column(db.Integer)
	img = db.Column(db.Integer)
	img_url = db.Column(db.String(200))
	comment = db.Column(db.String(200))
	score = db.Column(db.Integer)
	task2_id = db.Column(db.Integer)
	task2_completed = db.Column(db.Boolean, default=False)

	def __init__(self, name, challenge_id, individual_id, img, img_url, comment):
		self.name = name
		self.challenge_id = challenge_id
		self.individual_id = individual_id
		self.img = img
		self.img_url = img_url
		self.comment = comment
		self.score = score
		self.task2_id = task2_id
		self.task2_completed = task2_completed

class User(db.Model):
	__tablename__ = 'users'
	email = db.Column(db.String(100), primary_key=True)
	password = db.Column(db.String(200))
	name = db.Column(db.String(100))
		
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

	def check_password(self, password):
		return self.password == sha1(password).hexdigest()


# HELPER FUNCTIONS ################################################################
def get_session_error():
	error = ""
	if 'error' in session:
		error = session['error']
	session['error'] = ""
	return error

def get_session_success():
	success = ""
	if 'success' in session:
		success = session['success']
	session['success'] = ""
	return success

def is_valid_url(url):
	try:
		request = requests.get(url)
		if request.status_code == 200:
			return True
		else:
			return False 
	except requests.exceptions.RequestException as e:
		return False

def create_crowdflower_task1():
	data = []
	# The golden question
	data.append({
		'id': 0,
		'description': 'Which of these two poster designs would look better as a motivational graphic?',
		'url_img1': 'http://i.imgur.com/AD3DgWB.jpg',
		'url_img2': 'http://i.imgur.com/lYoObRX.jpg',
		'_golden': 'TRUE',
		'better_gold': 'img_1',
		'better_gold_reason': 'The second image shown had a typo.',
	})

	challenges = Challenges.query.filter_by(task1_id = None).all()
	for challenge in challenges:
		data.append({
			'id': challenge.id,
			'description': challenge.description,
			'url_img1': challenge.url_1,
			'url_img2': challenge.url_2,
			'_golden': '',
			'better_gold': '',
			'better_gold_reason': '',
		})

	job = conn.upload(data)
	update_result = job.update({
		'title': 'Comment on Graphic Design - %s' % job.id,
		'included_countries': ['US', 'GB'],
		'payment_cents': 3,
		'judgments_per_unit': 20,
		'units_per_assignment': 5,
		'instructions': '<h1>Pick the Best Designs</h1><p>Help our designers determine which of their two designs is more appealing by leaving comments and selecting your favorite.</p><p>Bonuses will be awarded for high quality answers and workers will be banned for gibberish or unthoughtful responses.</p>',
		'cml': '''
			<p class="description">{{description}}</p>
			<div class="graphic-divider padded">
				<h1>Design 1:</h1>
				<img src="{{url_img1}}" alt="Image not found." />
				<cml:textarea label="Comments on Design 1:" validates="required" default="What is your opinion of Design 1? What could be improved? Fonts? Colors? Image quality? Please write 1-2 sentences."/>
			</div>
			<div class="graphic-divider padded">
				<h1>Design 2:</h1>
				<img src="{{url_img2}}" alt="Image not found." />  
				<cml:textarea label="Comments on Design 2:" validates="required" default="What is your opinion of Design 2? What could be improved? Fonts? Colors? Image quality? Please write 1-2 sentences."/>
			</div>
			<div class="padded">
				<cml:select label="Best Design:" validates="required">
					<cml:option label="Design 1" value="img_1"/>
					<cml:option label="Design 2" value="img_2" />
					<cml:option label="Both Not Found" value="not_found" />
				</cml:select>
			</div>''',
		'css': '''
			.padded {
				padding: 2%;
			}
			.graphic-divider {
				display: inline-block;
				vertical-align: top;
				width: 46%;
				margin-right: -4px;
				box-sizing: border-box;
			}
			.description {
				font-size: 26px;
			}''',
	})

	# Update the task ID for all the rows we just uploaded to CrowdFlower
	for challenge in challenges:
		challenge.task1_id = job.id
	db.session.commit()

	# job.launch(5, channels=['cf_internal'])
	job.launch(5)

def get_crowdflower_results_task1():
	return ""


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
			return render_template('index.html', error = get_session_error())
		user = User.query.get(email)
		if user and user.check_password(password) and login_user(user):
			return redirect(url_for('responses'))
		else:
			session['error'] = "Invalid email or password. Please try again."
			return render_template('index.html', error = get_session_error())
	return render_template('index.html')

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
			return render_template('index.html', error = get_session_error())
		if User.query.get(email):
			session['error'] = "Sorry, this email address already exists."
			return render_template('index.html', error = get_session_error())
		new_user = User(email, sha1(password).hexdigest(), name)
		db.session.add(new_user)
		db.session.commit()
		if login_user(new_user):
			return redirect(url_for('responses'))
		else:
			session['error'] = "Sorry, something went wrong. Please try again."
			return render_template('index.html', error = get_session_error())
	return render_template('index.html')

@app.route('/responses')
def responses():
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	challenges = Challenges.query.filter_by(user_email = current_user.email).order_by(desc(Challenges.id)).all()
	get_crowdflower_results_task1()
	return render_template('responses.html', success = get_session_success(), responses = challenges)

@app.route('/response/<int:id>')
def response(id):
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	challenge = Challenges.query.get(id)
	comments_1 = Comments.query.filter_by(challenge_id=id).filter_by(img=1).order_by(desc(Comments.score)).limit(5).all()
	comments_2 = Comments.query.filter_by(challenge_id=id).filter_by(img=2).order_by(desc(Comments.score)).limit(5).all()
	return render_template('response.html', success = get_session_success(), response = challenge, comments_1 = comments_1, comments_2=comments_2)

@app.route('/upload', methods=['GET','POST'])
def upload():
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	if request.method == 'POST':
		# Check that they entered name
		name = request.form['name']
		if name == "":
			session['error'] = "Please enter a job name."
			return render_template('upload.html', error = get_session_error())
		
		# Check first url
		url1 = request.form['url1']
		if not is_valid_url(url1):
			session['error'] = "Sorry, the first URL was not valid. Please enter a valid URL."
			return render_template('upload.html', error = get_session_error())
		
		# Check second url
		url2 = request.form['url2']
		if not is_valid_url(url2):
			session['error'] = "Sorry, the second URL was not valid. Please enter a valid URL."
			return render_template('upload.html', error = get_session_error())
		
		# Check that URLs are not same
		if url1 == url2:
			session['error'] = "Sorry, both URLs cannot be the same. Please enter two different URLs."
			return render_template('upload.html', error = get_session_error())

		# Check that they entered description
		description = request.form['description']
		if description == "":
			session['error'] = "Please enter a description."
			return render_template('upload.html', error = get_session_error())

		# Check that they chose num voters
		num_voters = request.form['num-voters']
		if num_voters == "0":
			session['error'] = "Please choose the number of voters you would like."
			return render_template('upload.html', error = get_session_error())
		
		new_challenge = Challenges(name, url1, url2, num_voters, current_user.email, description)
		db.session.add(new_challenge)
		db.session.commit()
		if len(Challenges.query.filter_by(task1_id = None).all()) > 10:
			# Generate Crowd Flower task
			create_crowdflower_task1()
		session['success'] = "Success! Your images have been uploaded. The crowd will vote on your designs and we'll get back to you shortly with the results."
		return redirect(url_for('responses'))
	return render_template('upload.html')

if __name__ == '__main__':
	app.run(debug=True)