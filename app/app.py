from flask import Flask, redirect, render_template, request, session, url_for
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, confirm_login, fresh_login_required)
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_
from sqlalchemy.dialects.mysql import *


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# DATABASE MODELS #################################################################
class Challenges(db.Model):
	__tablename__ = 'challenges'
	id = db.Column(db.Integer, primary_key=True)
	
	def __init__(self, id):
		self.id = id

class DbUser(object):
	def __init__(self, user, userid, urole):
		self.user = user
		self.userid = userid
		self.role = urole
		self.error = ''
	def get_id(self):
		return unicode(self.userid)

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def get_role(self):
		return self.role


# APP ROUTES ######################################################################
@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()