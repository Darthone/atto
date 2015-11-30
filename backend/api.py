from flask_restful import Api

from app import app
from views import *

api = Api(app)
api.add_resource(HostRes, '/hosts/<host>')
api.add_resource(HostsRes, '/hosts/')
api.add_resource(CPUStatsRes, '/cpu/<host>')



