import datetime
import ujson as json

from playhouse.shortcuts import *
from flask_restful import reqparse, abort, Api, Resource


from app import app, database
from models import *

class HostRes(Resource):
    def get(self, host):
        h = Host.get(name=host)
        return model_to_dict(h)

    def post(self, host):
        h = Host.get_or_create(name=host)
        return model_to_dict(h), 200


class HostsRes(Resource):
    def get(self):
        l = Host.select()
        return [model_to_dict(h) for h in l]


class CPUStatsRes(Resource):
    def get(self, host):
        def clean(d):
            res = model_to_dict(d)
            res['timestamp'] = str(res['timestamp'])
            res['recv'] = str(res['recv'])
            res['CPU'] = json.loads(res['CPU'])
            res['epoch'] = res['epoch_milli'] / 1000
            return res 

        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, default=20)
        args = parser.parse_args()

        l = CPUStats.select().join(Host).where(Host.name==host).order_by(CPUStats.timestamp.desc()).limit(args['limit'])
        r = l.execute()
        return [clean(i) for i in r]

    def post(self, host):
        parser = reqparse.RequestParser()
        parser.add_argument('load_1', type=float)
        parser.add_argument('load_5', type=float)
        parser.add_argument('load_15', type=float)
        parser.add_argument('CPU', type=str)
        parser.add_argument('timestamp', type=str)
        parser.add_argument('epoch_milli', type=int)
        args = parser.parse_args()
        h = Host.get_or_create(name=host)
        args['hostname'] = h[0].id
        print args
        q = CPUStats.insert(**args)
        q.execute()
        return

