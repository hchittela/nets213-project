import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = 'SecretKeyForSessionSigning'

password = 'nets213ccb'
uri =  'mysql://admin:%s@nets213ccb.cxh68dehnct7.us-east-1.rds.amazonaws.com' %(password)
SQLALCHEMY_DATABASE_URI = uri
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"