from flask_restful import Resource, reqparse, abort
from ..sql.filters_sql import year_code_sql, order_by_season_sql, playerid_sql, game_type_sql, where_sql, month_sql
from ..sql.teams_sql import select_yearly_team_for_summaries, select_yearly_team_for_summaries_basic_ranks, select_yearly_team_against_summaries, select_yearly_team_against_summaries_basic_ranks
import pandas as pd
from ..common.utils import abort_if_team_doesnt_exist, engine


# Team
# shows a single team's statistics
class Team(Resource):
    def get(self, id):  # id is player id
        if len(str(id)) == 0 | len(str(id)) > 15:  # quick check for validation
            abort(404, message="Player {} doesn't exist".format(id))
        abort_if_team_doesnt_exist(id)  # Make sure player exists
        parser = reqparse.RequestParser()
        parser.add_argument('season', type=int, help='Valid season argument required (example: season=20182019)')
        parser.add_argument('gametype', type=str, help="Valid gametype argument required - either R or P ")
        parser.add_argument('month', type=str, help='Invalid month argument, must be string')
        parser.add_argument('depth', type=str, help='Invalid depth argument, must be string')
        parser.add_argument('returntype', type=str, help='Invalid return type argument, must be string')
        args = parser.parse_args()

        # Team For Summaries - Shooter stats
        if args['depth'] is not None:
            if args['depth'] == 'allsummaries':
                sql = select_yearly_team_for_summaries
            elif args['depth'] == 'basicranks':
                sql = select_yearly_team_for_summaries_basic_ranks
            else:
                sql = select_yearly_team_for_summaries_basic_ranks
        else:
            sql = select_yearly_team_for_summaries_basic_ranks

        sql += where_sql
        sql += playerid_sql
        sql = sql.format(id)

        # Add season filter
        if args['season'] is not None:
            sql += year_code_sql.format(args['season'])

        # Add game type filter
        if args['gametype'] is not None:
            sql += game_type_sql.format(args['gametype'])

        # Add month filter - default is year
        if args['month'] is not None:
            sql += month_sql.format(args['month'])

        # Add order by sql to the end
        sql += order_by_season_sql

        e = engine()
        teamStats = pd.read_sql_query(sql, con=e)

        if args['returntype'] is not None:
            if args['returntype'] == 'list':
                tfs = teamStats.to_dict(orient='records')
            else:
                teamStats = teamStats.set_index(['year_code', 'month'])
                tfs = {level: teamStats.xs(level).to_dict('index') for level in teamStats.index.levels[0]}
        else:
            teamStats = teamStats.set_index(['year_code', 'month'])
            tfs = {level: teamStats.xs(level).to_dict('index') for level in teamStats.index.levels[0]}

        ### Team Against Summaries - Goalie stats ###
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
        sql += playerid_sql
        sql = sql.format(id)

        # Add season filter
        if args['season'] is not None:
            sql += year_code_sql.format(args['season'])

        # Add game type filter
        if args['gametype'] is not None:
            sql += game_type_sql.format(args['gametype'])

        # Add month filter - default is year
        if args['month'] is not None:
            sql += month_sql.format(args['month'])

        # Add order by sql to the end
        sql += order_by_season_sql

        e = engine()
        goalieStats = pd.read_sql_query(sql, con=e)

        if args['returntype'] is not None:
            if args['returntype'] == 'list':
                tas = goalieStats.to_dict(orient='records')
            else:
                goalieStats = goalieStats.set_index(['year_code', 'month'])
                tas = {level: goalieStats.xs(level).to_dict('index') for level in goalieStats.index.levels[0]}
        else:
            goalieStats = goalieStats.set_index(['year_code', 'month'])
            tas = {level: goalieStats.xs(level).to_dict('index') for level in goalieStats.index.levels[0]}

        return {'team_for_stats': tfs,
                'team_against_stats': tas}