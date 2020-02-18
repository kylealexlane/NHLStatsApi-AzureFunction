from flask_restful import Resource, reqparse
from ..sql.goalies_sql import select_yearly_goalie_summaries, select_yearly_goalie_summaries_basic_ranks
from ..sql.filters_sql import year_code_sql, order_by_goals_sql, game_type_sql, where_sql, pos_sql, month_sql, team_sql, first_name_not_null_sql
import pandas as pd
from ..common.utils import engine


# GoaliesList
# Resturns list of goalie stats - need year and gametype arguments passed
class Goalies(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('season', type=int, required=True, help='Valid season argument required (example: season=20182019)')
        parser.add_argument('gametype', type=str, required=True, help="Valid gametype argument required - either 'R' or 'P' ")
        parser.add_argument('month', type=str, help='Invalid month argument, must be string')
        parser.add_argument('pos', type=str, help='Invalid position argument, must be string')
        parser.add_argument('depth', type=str, help='Invalid depth argument, must be string')
        parser.add_argument('team', type=int, help='Invalid team argument, must be integer')
        parser.add_argument('returntype', type=str, help='Invalid return type argument, must be string')
        args = parser.parse_args()

        gt = args['gametype']  # Required
        s = args['season']  # Required
        if args['depth'] is not None:
            if args['depth'] == 'allsummaries':
                sql = select_yearly_goalie_summaries
            elif args['depth'] == 'basicranks':
                sql = select_yearly_goalie_summaries_basic_ranks
            else:
                sql = select_yearly_goalie_summaries_basic_ranks
        else:
            sql = select_yearly_goalie_summaries_basic_ranks

        sql += where_sql
        sql += year_code_sql
        sql += game_type_sql
        sql = sql.format(s, gt)

        # Add positional filter
        if args['pos'] is not None:
            sql += pos_sql.format(args['pos'])

        # Add team filter
        if args['team'] is not None:
            sql += team_sql.format(args['team'])

        # Add month filter - default is year
        if args['month'] is not None:
            sql += month_sql.format(args['month'])
        else:
            sql += month_sql.format("year")

        # Add order by sql to the end
        sql += first_name_not_null_sql
        sql += order_by_goals_sql

        e = engine()
        goalieStats = pd.read_sql_query(sql, con=e)

        if args['returntype'] is not None:
            if args['returntype'] == 'list':
                ps = goalieStats.to_dict(orient='records')
            else:
                ps = goalieStats.set_index(['id']).to_dict('index')
        else:
            ps = goalieStats.set_index(['id']).to_dict('index')

        return {'goalie_stats': ps}