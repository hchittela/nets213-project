import csv
import os
import time
import json
import math
import random
import requests
import crowdflower

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
	description = db.Column(db.String(200))
	num_voters = db.Column(db.Integer)
	task1_id = db.Column(db.Integer)
	task1_completed = db.Column(db.Boolean, default=False)
	votes_1 = db.Column(db.Integer)
	votes_2 = db.Column(db.Integer)

	def __init__(self, name, url_1, url_2, num_voters, email, description):
		self.name = name
		self.url_1 = url_1
		self.url_2 = url_2
		self.num_voters = num_voters
		self.user_email = email
		self.description = description

class Comments(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	challenge_id = db.Column(db.Integer)
	individual_id = db.Column(db.Integer)
	img = db.Column(db.Integer)
	img_url = db.Column(db.String(200))
	comment = db.Column(db.String(500))
	score = db.Column(db.Float)
	task2_id = db.Column(db.Integer)
	task2_completed = db.Column(db.Boolean, default=False)

	def __init__(self, challenge_id, individual_id, img, img_url, comment):
		self.challenge_id = challenge_id
		self.individual_id = individual_id
		self.img = img
		self.img_url = img_url
		self.comment = comment

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


# CROWDFLOWER FUNCTIONS ###########################################################
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
	if len(challenge) < 10: return False
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

	# job.launch(len(data), channels=['cf_internal'])
	job.launch(len(data))
	return True

def create_crowdflower_task2():
	data = []
	
	comments = Comments.query.filter_by(task2_id = None).all()
	if len(comments) == 0: return False
	for comment in comments:
		data.append({
			'challenge_id': comment.challenge_id,
			'individual_id': comment.individual_id,
			'comment': comment.comment,
			'img_url': comment.img_url,
			'_golden': '',
			'better_gold': '',
			'better_gold_reason': '',
		})

	job = conn.upload(data)
	update_result = job.update({
		'title': 'Evaluate Comments on Graphic Design - %s' % job.id,
		'included_countries': ['US', 'GB'],
		'payment_cents': 5,
		'judgments_per_unit': 5,
		'units_per_assignment': 25,
		'instructions': '<h1>Evaluate Comments on Each Picture</h1><p>Help our designers determine which of the comments is the best.</p><p>Bonuses will be awarded for high quality answers and workers will be banned for randomly selecting answers.</p>',
		'cml': '''
			<img src="{{img_url}}" alt="Image not found." style="max-height: 350px;"/>
			<p class="description">
			  <strong>Comment: </strong>{{comment}}
			</p>
			<cml:select label="How helpful is this comment?" validates="required">
			  <cml:option label="Very Helpful - It is specific, detailed, and give suggestions for improvement." value="5"/>
			  <cml:option label="Decent - It is specific, detailed, but does not give suggestions for improvement." value="3"/>
			  <cml:option label="Okay - It relates, but is not specific or detailed." value="2"/>
			  <cml:option label="Bad - It doesn't relate to the image." value="1"/>
			  # <cml:option label="Complete Gibberish - These are not even real words." value="0"/>
			</cml:select>''',
		'css': '''
			.description {
			  font-size: 26px;
			}''',
	})

	# Update the task ID for all the rows we just uploaded to CrowdFlower
	for comment in comments:
		comment.task2_id = job.id
	db.session.commit()

	# job.launch(len(data), channels=['cf_internal'])
	job.launch(len(data))
	return True

def get_crowdflower_results_task1():
	has_new_results = False
	# Get the list of job IDs that have been uploaded but are listed as not complete in the DB
	posted = Challenges.query.filter(Challenges.task1_id != None).filter(Challenges.task1_completed == 0).group_by(Challenges.task1_id).all()
	incomplete_ids = []
	for challenge in posted:
		incomplete_ids.append(challenge.task1_id)
	# Get the job if it is now complete
	for job in conn.jobs():
		if job.properties['completed'] and job.properties['id'] in incomplete_ids:
			# Add the comments for this job to the Comments table and also store the data for the QC CrowdFlower task
			data = []
			votes = {}
			individual_id = 0
			for row in job.download():
				challenge_id = str(int(row['id']))
				# Add the first comment
				comment_img1 = Comments(challenge_id, individual_id, 1, row['url_img1'], row['comments_on_design_1'])
				db.session.add(comment_img1)
				individual_id += 1
				# Add the second comment
				comment_img2 = Comments(challenge_id, individual_id, 2, row['url_img2'], row['comments_on_design_2'])
				db.session.add(comment_img2)
				individual_id += 1
				# Add the vote to our challenge
				if challenge_id in votes:
					if row['best_design'] == "img_1":
						votes[challenge_id] = {'img_1': votes[challenge_id]['img_1'] + 1, 'img_2': votes[challenge_id]['img_2']}
					elif row['best_design'] == "img_2":
						votes[challenge_id] = {'img_1': votes[challenge_id]['img_1'], 'img_2': votes[challenge_id]['img_2'] + 1}
				else:
					if row['best_design'] == "img_1":
						votes[challenge_id] = {'img_1': 1, 'img_2': 0}
					elif row['best_design'] == "img_2":
						votes[challenge_id] = {'img_1': 0, 'img_2': 1}
			# Update the task1_complete field in the Challenges table
			challenges = Challenges.query.filter_by(task1_id = job.properties['id']).all()
			for challenge in challenges:
				challenge.task1_completed = 1
				challenge.votes_1 = votes[str(int(challenge.id))]['img_1']
				challenge.votes_2 = votes[str(int(challenge.id))]['img_2']
			# Commit to the database
			db.session.commit()
			has_new_results = True
	return has_new_results

def get_crowdflower_results_task2():
	has_new_results = False
	# Get the list of job IDs that have been uploaded but are listed as not complete in the DB
	posted = Comments.query.filter(Comments.task2_id != None).filter(Comments.task2_completed == 0).group_by(Comments.task2_id).all()
	incomplete_ids = []
	for comment in posted:
		incomplete_ids.append(comment.task2_id)
	# Get the job if it is now complete
	for job in conn.jobs():
		if job.properties['completed'] and job.properties['id'] in incomplete_ids:
			# Aggregate the comment scores for the job and save them to the DB
			votes = {}
			for row in job.download():
				challenge_id = str(int(row['challenge_id']))
				individual_id = str(int(row['individual_id']))
				if challenge_id in votes:
					if individual_id in votes[challenge_id]:
						votes[challenge_id][individual_id] = votes[challenge_id][individual_id].append(int(row['how_helpful_is_this_comment']))
					else:
						votes[challenge_id][individual_id] = [int(row['how_helpful_is_this_comment'])]
				else:
					votes[challenge_id] = {individual_id: [int(row['how_helpful_is_this_comment'])]}
			# Update the appropriate fields in the Comments table
			comments = Comments.query.filter_by(task2_id = job.properties['id']).all()
			for comment in comments:
				scores = votes[str(int(comment.challenge_id))][str(int(comment.individual_id))]
				comment.score = 1.0 * sum(scores) / len(scores)
				comment.task2_completed = 1
			# Commit to the database
			db.session.commit()
			has_new_results = True
	return has_new_results


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
	challenges = Challenges.query.filter_by(user_email = current_user.email).order_by(Challenges.id).all()
	return render_template('responses.html', success = get_session_success(), error = get_session_error(), responses = challenges)

@app.route('/response/<int:id>')
def response(id):
	if not current_user.is_authenticated:
		return redirect(url_for('index'))
	challenge = Challenges.query.get(id)
	# Check if the challenge exists
	if not challenge:
		session['error'] = "This response is not found. Please try again."
		return redirect(url_for('responses'))
	# Check if the current user posted the challenge
	if challenge.user_email != current_user.email:
		session['error'] = "You were not the poster of this challenge and are not authorized to view it."
		return redirect(url_for('responses'))
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
		session['success'] = "Success! Your images have been uploaded. The crowd will vote on your designs and we'll get back to you shortly with the results."
		return redirect(url_for('responses'))
	return render_template('upload.html')

if __name__ == '__main__':
	app.run(debug=True)