from flask_restful import Resource, reqparse, abort
from ..sql.filters_sql import year_code_sql, order_by_season_sql, playerid_sql, game_type_sql, where_sql, pos_sql, month_sql, team_sql
from ..sql.players_sql import select_yearly_shooter_summaries, select_yearly_shooter_summaries_basic_ranks
import pandas as pd
from ..common.utils import abort_if_player_doesnt_exist, engine


# Player
# shows a single player's statistics
class Player(Resource):
    def get(self, id):  # id is player id
        if len(str(id)) == 0 | len(str(id)) > 15:  # quick check for validation
            abort(404, message="Player {} doesn't exist".format(id))
        abort_if_player_doesnt_exist(id)  # Make sure player exists
        parser = reqparse.RequestParser()
        parser.add_argument('season', type=int, help='Valid season argument required (example: season=20182019)')
        parser.add_argument('gametype', type=str, help="Valid gametype argument required - either R or P ")
        parser.add_argument('month', type=str, help='Invalid month argument, must be string')
        parser.add_argument('pos', type=str, help='Invalid position argument, must be string')
        parser.add_argument('depth', type=str, help='Invalid depth argument, must be string')
        parser.add_argument('team', type=int, help='Invalid team argument, must be integer')
        parser.add_argument('returntype', type=str, help='Invalid return type argument, must be string')
        args = parser.parse_args()

        if args['depth'] is not None:
            if args['depth'] == 'allsummaries':
                sql = select_yearly_shooter_summaries
            elif args['depth'] == 'basicranks':
                sql = select_yearly_shooter_summaries_basic_ranks
            else:
                sql = select_yearly_shooter_summaries_basic_ranks
        else:
            sql = select_yearly_shooter_summaries_basic_ranks

        sql += where_sql
        sql += playerid_sql
        sql = sql.format(id)

        # Add season filter
        if args['season'] is not None:
            sql += year_code_sql.format(args['season'])

        # Add game type filter
        if args['gametype'] is not None:
            sql += game_type_sql.format(args['gametype'])

        # Add positional filter
        if args['pos'] is not None:
            sql += pos_sql.format(args['pos'])

        # Add team filter
        if args['team'] is not None:
            sql += team_sql.format(args['team'])

        # Add month filter - default is year
        if args['month'] is not None:
            sql += month_sql.format(args['month'])

        # Add order by sql to the end
        sql += order_by_season_sql

        e = engine()
        playerStats = pd.read_sql_query(sql, con=e)
        print(playerStats.set_index(['year_code', 'month']).index.levels)
        for level in playerStats.set_index(['year_code', 'month']).index.levels[0]:
            print(level)

        print(playerStats.set_index(['year_code', 'month']).index.levels[0])

        if args['returntype'] is not None:
            if args['returntype'] == 'list':
                ps = playerStats.to_dict(orient='records')
            else:
                playerStats = playerStats.set_index(['year_code', 'month'])
                ps = {level: playerStats.xs(level).to_dict('index') for level in playerStats.index.levels[0]}
        else:
            playerStats = playerStats.set_index(['year_code', 'month'])
            ps = {level: playerStats.xs(level).to_dict('index') for level in playerStats.index.levels[0]}

        e.dispose()
        return {'player_stats': ps}