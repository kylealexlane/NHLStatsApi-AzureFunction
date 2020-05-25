from flask_restful import Resource
from ..common.utils import engine


# Ping
class Ping(Resource):
    def get(self):
        
        e = engine()
        e.dispose()
        return 'successful ping'
