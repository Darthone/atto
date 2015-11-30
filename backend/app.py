from flask import Flask
from flask.ext.cors import CORS
from peewee import *

# config - aside from our database, the rest is for use by Flask
DATABASE = 'atto.db'
DEBUG = True
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'


app = Flask(__name__)
app.config.from_object('config.Configuration')
CORS(app)

database = SqliteDatabase(DATABASE)

