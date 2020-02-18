from flask_restful import abort
from ..ignore import hostname, username, database, password, port
from ..sql.players_sql import get_all_player_ids_sql
from ..sql.goalies_sql import get_all_goalie_ids_sql
from ..sql.teams_sql import get_team_id_sql
from sqlalchemy import create_engine
import pandas as pd
import os


if 'RDS_HOSTNAME' in os.environ:
    database = os.environ['RDS_DB_NAME']
    username = os.environ['RDS_USERNAME']
    password = os.environ['RDS_PASSWORD']
    hostname = os.environ['RDS_HOSTNAME']
    port = os.environ['RDS_PORT']
else:
    hostname = hostname
    username = username
    password = password
    database = database
    port = port

    # hostname = ''  # Used in production
    # username = ''  # Used in production
    # password = ''  # Used in production
    # database = ''  # Used in production
    # port = ''  # Used in production


def engine():
    engstr = 'postgresql://{}:{}@{}:{}/{}'.format(username, password, hostname, port, database)
    e = create_engine(engstr)
    return e


def abort_if_player_doesnt_exist(player_id):
    e = engine()
    sql = get_all_player_ids_sql.format(player_id)
    pid = pd.read_sql_query(sql, con=e)

    if pid.size == 0:
        abort(404, message="Player {} doesn't exist".format(player_id))


def abort_if_goalie_doesnt_exist(id):
    e = engine()
    sql = get_all_goalie_ids_sql.format(id)
    pid = pd.read_sql_query(sql, con=e)

    if pid.size == 0:
        abort(404, message="Goalie {} doesn't exist".format(id))


def abort_if_team_doesnt_exist(id):
    e = engine()
    sql = get_team_id_sql.format(id)
    pid = pd.read_sql_query(sql, con=e)

    if pid.size == 0:
        abort(404, message="Team {} doesn't exist".format(id))