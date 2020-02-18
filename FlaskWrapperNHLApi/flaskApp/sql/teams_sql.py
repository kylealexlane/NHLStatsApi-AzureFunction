# YEARLY TEAM SUMMARIES #
select_yearly_team_for_summaries = """
        SELECT 
        t.name,
        t.abbreviation,
        t.division,
        t.conference,
        id,
        year_code,
        month,
        game_type,
        num_goals,
        wrist_shot_num,
        backhand_num,
        slap_shot_num,
        snap_shot_num,
        tip_in_num,
        deflected_num,
        wrap_around_num,
        wrist_shot_pred,
        backhand_pred,
        slap_shot_pred,
        snap_shot_pred,
        tip_in_pred,
        deflected_pred,
        wrap_around_pred,
        mean_dist,
        mean_ang,
        sum_xgoals,
        num_shots,
        avg_shoot_perc,
        shot_quality,
        wrist_shot_freq,
        backhand_freq,
        slap_shot_freq,
        snap_shot_freq,
        tip_in_freq,
        deflected_freq,
        wrap_around_freq,
        avg_xgoals,
        avg_xgoals_wrist_shot,
        avg_xgoals_backhand,
        avg_xgoals_slap_shot,
        avg_xgoals_snap_shot,
        avg_xgoals_tip_in,
        avg_xgoals_deflected,
        avg_xgoals_wrap_around,
        goals_aa_per_shot,
        wrist_shot_shooting_perc,
        backhand_shooting_perc,
        slap_shot_shooting_perc,
        snap_shot_shooting_perc,
        tip_in_shooting_perc,
        deflected_shooting_perc,
        wrap_around_shooting_perc,
        avg_shoot_perc_aa,
        wrist_shot_freq_aa,
        backhand_freq_aa,
        slap_shot_freq_aa,
        snap_shot_freq_aa,
        tip_in_freq_aa,
        deflected_freq_aa,
        wrap_around_freq_aa,
        avg_xgoals_aa,
        avg_xgoals_wrist_shot_aa,
        avg_xgoals_backhand_aa,
        avg_xgoals_slap_shot_aa,
        avg_xgoals_snap_shot_aa,
        avg_xgoals_tip_in_aa,
        avg_xgoals_deflected_aa,
        avg_xgoals_wrap_around_aa,
        wrist_shot_shooting_perc_aa,
        backhand_shooting_perc_aa,
        slap_shot_shooting_perc_aa,
        snap_shot_shooting_perc_aa,
        tip_in_shooting_perc_aa,
        deflected_shooting_perc_aa,
        wrap_around_shooting_perc_aa
        FROM nhlstats.yearly_team_shooter_summaries
        LEFT JOIN nhlstats.teams t USING(id)
        """

select_yearly_team_for_summaries_basic_ranks = """
        SELECT 
        t.name,
        t.abbreviation,
        t.division,
        t.conference,
        id,
        month,
        year_code,
        num_goals,
        mean_dist,
        mean_ang,
        sum_xgoals,
        num_shots,
        avg_shoot_perc,
        shot_quality,
        avg_xgoals,
        avg_shoot_perc_aa,
        avg_xgoals_aa,
        goals_aa_per_shot,

        sr.num_goals_rank,
        sr.mean_dist_rank,
        sr.mean_ang_rank,
        sr.sum_xgoals_rank,
        sr.num_shots_rank,
        sr.avg_shoot_perc_rank,
        sr.shot_quality_rank,
        sr.avg_xgoals_rank,
        sr.avg_shoot_perc_aa_rank,
        sr.avg_xgoals_aa_rank,
        sr.goals_aa_per_shot_rank,

        sr.num_goals_pctile,
        sr.mean_dist_pctile,
        sr.mean_ang_pctile,
        sr.sum_xgoals_pctile,
        sr.num_shots_pctile,
        sr.avg_shoot_perc_pctile,
        sr.shot_quality_pctile,
        sr.avg_xgoals_pctile,
        sr.avg_shoot_perc_aa_pctile,
        sr.avg_xgoals_aa_pctile,
        sr.goals_aa_per_shot_pctile
        FROM nhlstats.yearly_team_shooter_summaries
        LEFT JOIN nhlstats.teams t USING(id)
        LEFT JOIN nhlstats.yearly_team_shooter_ranks sr USING(id, year_code, month, game_type)
        """

# YEARLY TEAM AGAINST SUMMARIES - GOALIE STATS #
select_yearly_team_against_summaries = """
        SELECT 
        t.name,
        t.abbreviation,
        t.division,
        t.conference,
        id,
        year_code,
        month,
        game_type,
        num_goals,
        wrist_shot_num,
        backhand_num,
        slap_shot_num,
        snap_shot_num,
        tip_in_num,
        deflected_num,
        wrap_around_num,
        wrist_shot_pred,
        backhand_pred,
        slap_shot_pred,
        snap_shot_pred,
        tip_in_pred,
        deflected_pred,
        wrap_around_pred,
        mean_dist,
        mean_ang,
        sum_xgoals,
        num_shots,
        save_perc,
        shot_quality,
        wrist_shot_freq,
        backhand_freq,
        slap_shot_freq,
        snap_shot_freq,
        tip_in_freq,
        deflected_freq,
        wrap_around_freq,
        xsave_perc,
        xsave_perc_wrist_shot,
        xsave_perc_backhand,
        xsave_perc_slap_shot,
        xsave_perc_snap_shot,
        xsave_perc_tip_in,
        xsave_perc_deflected,
        xsave_perc_wrap_around,
        saves_aa_per_shot,
        wrist_shot_save_perc,
        backhand_save_perc,
        slap_shot_save_perc,
        snap_shot_save_perc,
        tip_in_save_perc,
        deflected_save_perc,
        wrap_around_save_perc,
        save_perc_aa,
        wrist_shot_freq_aa,
        backhand_freq_aa,
        slap_shot_freq_aa,
        snap_shot_freq_aa,
        tip_in_freq_aa,
        deflected_freq_aa,
        wrap_around_freq_aa,
        xsave_perc_aa,
        xsave_perc_wrist_shot_aa,
        xsave_perc_backhand_aa,
        xsave_perc_slap_shot_aa,
        xsave_perc_snap_shot_aa,
        xsave_perc_tip_in_aa,
        xsave_perc_deflected_aa,
        xsave_perc_wrap_around_aa,
        wrist_shot_save_perc_aa,
        backhand_save_perc_aa,
        slap_shot_save_perc_aa,
        snap_shot_save_perc_aa,
        tip_in_save_perc_aa,
        deflected_save_perc_aa,
        wrap_around_save_perc_aa
        FROM nhlstats.yearly_team_against_summaries
        LEFT JOIN nhlstats.teams t USING(id)
        """

select_yearly_team_against_summaries_basic_ranks = """
        SELECT 
        t.name,
        t.abbreviation,
        t.division,
        t.conference,
        id,
        month,
        year_code,
        num_goals,
        mean_dist,
        mean_ang,
        sum_xgoals,
        num_shots,
        save_perc,
        shot_quality,
        xsave_perc,
        save_perc_aa,
        xsave_perc_aa,
        saves_aa_per_shot,

        sr.num_goals_rank,
        sr.mean_dist_rank,
        sr.mean_ang_rank,
        sr.sum_xgoals_rank,
        sr.num_shots_rank,
        sr.save_perc_rank,
        sr.shot_quality_rank,
        sr.xsave_perc_rank,
        sr.save_perc_aa_rank,
        sr.xsave_perc_aa_rank,
        sr.saves_aa_per_shot_rank,

        sr.num_goals_pctile,
        sr.mean_dist_pctile,
        sr.mean_ang_pctile,
        sr.sum_xgoals_pctile,
        sr.num_shots_pctile,
        sr.save_perc_pctile,
        sr.shot_quality_pctile,
        sr.xsave_perc_pctile,
        sr.save_perc_aa_pctile,
        sr.xsave_perc_aa_pctile,
        sr.saves_aa_per_shot_pctile
        FROM nhlstats.yearly_team_against_summaries
        LEFT JOIN nhlstats.teams t USING(id)
        LEFT JOIN nhlstats.yearly_team_against_ranks sr USING(id, year_code, month, game_type)
        """


# GET TEAM BY ID #
get_team_id_sql = """
    SELECT id
    FROM nhlstats.teams
    WHERE id = {}"""