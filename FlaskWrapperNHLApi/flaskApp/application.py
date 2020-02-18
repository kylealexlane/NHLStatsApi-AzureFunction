#!flask/bin/python

"""API for nhl stats"""

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
from .resources.player import Player
from .resources.players import Players
from .resources.goalie import Goalie
from .resources.goalies import Goalies
from .resources.teams import Teams
from .resources.team import Team


application = app = Flask(__name__)  # Used in production
# app = Flask(__name__)  # Used for local test development

CORS(app)
api = Api(app)

api.add_resource(Players, '/api/v1/players')  # List of players and stats
api.add_resource(Player, '/api/v1/players/<int:id>')  # Individual player stats

api.add_resource(Goalies, '/api/v1/goalies')  # List of goalies and stats
api.add_resource(Goalie, '/api/v1/goalies/<int:id>')  # Individual goalie stats

api.add_resource(Teams, '/api/v1/teams')  # List of teams and stats
api.add_resource(Team, '/api/v1/teams/<int:id>')  # Individual team stats


###
# Steps for pushing to production
# - Change app = ... to application = app = ...
# - Comment out import in utils.py
# - Comment out params in if else in utils.py
# - Run pip freeze and add to requirements.txt if necessary
# - Zip and push (including requirements.txt)
#  zip -r nhlapi.zip application.py requirements.txt sql/ resources/ common/
# - Update documentation


# For local testing
# - source flask/bin/activate
# - python application.py
###

if __name__ == '__main__':
    app.run(debug=True)