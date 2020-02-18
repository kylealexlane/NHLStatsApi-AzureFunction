where_sql = " WHERE 1=1"  # just adding the where so the rest of the filters can have AND to start..
#TODO: figure out better way to do this.. maybe just replace first AND with WHERE after adding filters..

year_code_sql = """ AND year_code = {}"""

playerid_sql = """ AND id = {}"""

game_type_sql = """ AND game_type = '{}'"""

min_num_shots_sql = """ AND num_shots >= {}"""

pos_sql = """ AND p.pos_code = '{}'"""

team_sql = """ AND p.team_id = {}"""

month_sql = """ AND month = '{}'"""

first_name_not_null_sql = """ AND p.first_name IS NOT NULL"""

last_name_not_null_sql = """ AND p.last_name IS NOT NULL"""

order_by_goals_sql = """ ORDER BY num_goals DESC"""

order_by_season_sql = """ ORDER BY year_code DESC"""

