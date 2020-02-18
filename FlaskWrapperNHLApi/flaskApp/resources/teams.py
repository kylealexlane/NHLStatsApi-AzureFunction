from flask_restful import Resource, reqparse
from ..sql.teams_sql import select_yearly_team_for_summaries, select_yearly_team_for_summaries_basic_ranks, select_yearly_team_against_summaries, select_yearly_team_against_summaries_basic_ranks
from ..sql.filters_sql import year_code_sql, order_by_goals_sql, game_type_sql, where_sql, month_sql
import pandas as pd
from ..common.utils import engine


# Teams list
# Resturns list of team stats - need year and gametype arguments passed
class Teams(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('season', type=int, required=True, help='Valid season argument required (example: season=20182019)')
        parser.add_argument('gametype', type=str, required=True, help="Valid gametype argument required - either 'R' or 'P' ")
        parser.add_argument('month', type=str, help='Invalid month argument, must be string')
        parser.add_argument('depth', type=str, help='Invalid depth argument, must be string')
        parser.add_argument('returntype', type=str, help='Invalid return type argument, must be string')
        args = parser.parse_args()

        gt = args['gametype']  # Required
        s = args['season']  # Required

        ### Get team for stats - shooter stats ###
        if args['depth'] is not None:
            if args['depth'] == 'allsummaries':
                sql = select_yearly_team_for_summaries
            elif args['depth'] == 'basicranks':
                sql = select_yearly_team_for_summaries_basic_ranks
            else:
                sql = select_yearly_team_for_summaries_basic_ranks  # Default
        else:
            sql = select_yearly_team_for_summaries_basic_ranks  # Default

        sql += where_sql
        sql += year_code_sql
        sql += game_type_sql
        sql = sql.format(s, gt)

        # Add month filter - default is year
        if args['month'] is not None:
            sql += month_sql.format(args['month'])
        else:
            sql += month_sql.format("year")

        # Add order by sql to the end
        sql += order_by_goals_sql

        e = engine()
        teamStats = pd.read_sql_query(sql, con=e)

        if args['returntype'] is not None:
            if args['returntype'] == 'list':
                tfs = teamStats.to_dict(orient='records')
            else:
                tfs = teamStats.set_index(['id']).to_dict('index')
        else:
            tfs = teamStats.set_index(['id']).to_dict('index')

        ### Get team against stats - goalie stats ###
        if args['depth'] is not None:
            if args['depth'] == 'allsummaries':
                sql = select_yearly_team_against_summaries
            elif args['depth'] == 'basicranks':
                sql = select_yearly_team_against_summaries_basic_ranks
            else:
                sql = select_yearly_team_against_summaries_basic_ranks
        else:
            sql = select_yearly_team_against_summaries_basic_ranks

        sql += where_sql
        sql += year_code_sql
        sql += game_type_sql
        sql = sql.format(s, gt)

        # Add month filter - default is year
        if args['month'] is not None:
            sql += month_sql.format(args['month'])
        else:
            sql += month_sql.format("year")

        # Add order by sql to the end
        sql += order_by_goals_sql

        goalieStats = pd.read_sql_query(sql, con=e)

        if args['returntype'] is not None:
            if args['returntype'] == 'list':
                tas = goalieStats.to_dict(orient='records')
            else:
                tas = goalieStats.set_index(['id']).to_dict('index')
        else:
            tas = goalieStats.set_index(['id']).to_dict('index')

        return {'team_for_stats': tfs,
                'team_against_stats': tas}