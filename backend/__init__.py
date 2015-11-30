from flask_peewee.rest import RestAPI

from app import app # our project's Flask app

# instantiate our api wrapper
api = RestAPI(app)

# register our models so they are exposed via /api/<model>/
api.register(User)
api.register(Relationship)
api.register(Message)

# configure the urls
api.setup()
