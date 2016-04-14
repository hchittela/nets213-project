import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'SecretKeyForSessionSigning'

username = 'bf195be856ac10'
password = 'fc75324d'
uri =  'mysql://%s:%s@us-cdbr-iron-east-03.cleardb.net/heroku_8020c01508c5dac' % (username, password)
SQLALCHEMY_DATABASE_URI = uri
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"