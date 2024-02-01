CREATE TABLE seasons (
    id INT,
    sport_id INT,
    league_id INT,
    tie_breaker_rule_id INT,
    name TEXT,
    finished BOOLEAN,
    pending BOOLEAN,
    is_current BOOLEAN,
    starting_at DATE,
    ending_at DATE,
    standings_recalculated_at DATE,
    games_in_current_week BOOLEAN,
    PRIMARY KEY (id)
);

CREATE TABLE types (
        id INT,
        name INT,
        code INT,
        developer_name TEXT,
        model_type TEXT,
        stat_group TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE coaches (
    id INT,
    player_id INT,
    sport_id INT,
    country_id INT,
    nationality_id INT,
    city_id INT,
    common_name TEXT,
    firstname TEXT,
    lastname TEXT,
    name TEXT,
    display_name TEXT,
    height INT,
    weight INT,
    date_of_birth DATE,
    gender TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE standings (
    id INT,
    participant_id INT,
    sport_id INT,
    league_id INT,
    season_id INT,
    stage_id INT,
    group_id INT,
    round_id INT,
    standing_rule_id INT,
    position INT,
    result TEXT,
    points INT,
    PRIMARY KEY (id)
);

CREATE TABLE teams(
    id INT,
    sport_id INT,
    country_id INT,
    venue_id INT,
    gender TEXT,
    name TEXT,
    short_code TEXT,
    image_path TEXT,
    founded INT,
    type TEXT,
    placeholder BOOLEAN,
    last_played_at DATE,
    PRIMARY KEY (id)
);

CREATE TABLE fixtures(
    id INT,
    sport_id INT,
    league_id INT,
    season_id INT,
    stage_id INT,
    group_id INT,
    aggregate_id INT,
    round_id INT,
    state_id INT,
    venue_id INT,
    name TEXT,
    starting_at DATE,
    result_info TEXT,
    leg TEXT,
    details TEXT,
    length INT,
    placeholder BOOLEAN,
    has_odds BOOLEAN,
    starting_at_timestamp BIGINT,
    PRIMARY KEY (id)
);

CREATE TABLE players (
    id INT,
  sport_id INT,
  country_id INT,
  nationality_id  INT,
  city_id  INT,
  position_id  INT,
  detailed_position_id  INT,
  type_id  INT,
  common_name TEXT,
  firstname TEXT,
  lastname TEXT,
  name TEXT,
  display_name TEXT,
  image_path TEXT,
  height INT,
  weight INT,
  date_of_birth DATE,
  gender TEXT,
  PRIMARY KEY (id)
);

CREATE TABLE squads (
        id INT,
        player_id INT,
         team_id INT,
         season_id INT,
         has_values BOOLEAN,
         position_id INT,
         jersey_number INT,
    PRIMARY KEY (id)
);

CREATE TABLE topscorers (
        id INT,
        season_id INT,
        player_id INT,
         type_id INT,
         position INT,
         total INT,
         participant_id INT,
    PRIMARY KEY (id)
);

CREATE TABLE transfers (
        id INT,
        sport_id INT,
         player_id INT,
         type_id INT,
         from_team_id INT,
         to_team_id INT,
         position_id INT,
         detailed_position_id INT,
         date DATE,
         career_ended BOOLEAN,
         completed BOOLEAN,
         amount TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE team_stats_detailed (
        id INT,
        team_statistic_id INT,
        type_id INT,
        value_count INT,
        value_average INT,
        value_player_id INT,
        value_player_name TEXT,
        value_coach INT,
        value_coach_average INT,
        value_all_count INT,
        value_all_average INT,
        value_all_first INT,
        value_home_count INT,
        value_home_percentage INT,
        value_home_average INT,
        value_home_first INT,
        value_away_count INT,
        value_away_percentage INT,
        value_away_average INT,
        value_away_first INT,
        value_over_0_5_matches_count INT,
        value_over_0_5_matches_percentage INT,
        value_over_0_5_team_count INT,
        value_over_0_5_team_percentage INT,
        value_over_1_5_matches_count INT,
        value_over_1_5_matches_percentage INT,
        value_over_1_5_team_count INT,
        value_over_1_5_team_percentage INT,
        value_over_2_5_matches_count INT,
        value_over_2_5_matches_percentage INT,
        value_over_2_5_team_count INT,
        value_over_2_5_team_percentage INT,
        value_over_3_5_matches_count INT,
        value_over_3_5_matches_percentage INT,
        value_over_3_5_team_count INT,
        value_over_3_5_team_percentage INT,
        value_over_4_5_matches_count INT,
        value_over_4_5_matches_percentage INT,
        value_over_4_5_team_count INT,
        value_over_4_5_team_percentage INT,
        value_over_5_5_matches_count INT,
        value_over_5_5_matches_percentage INT,
        value_over_5_5_team_count INT,
        value_over_5_5_team_percentage INT,
        value_0_15_count INT,
        value_0_15_percentage INT,
        value_15_30_count INT,
        value_15_30_percentage INT,
        value_30_45_count INT,
        value_30_45_percentage INT,
        value_45_60_count INT,
        value_45_60_percentage INT,
        value_60_75_count INT,
        value_60_75_percentage INT,
        value_75_90_count INT,
        value_75_90_percentage INT,
        value_home_overall_percentage INT,
        value_away_overall_percentage INT,
    PRIMARY KEY (id)
);

CREATE TABLE team_stats (
        id INT,
        team_id INT,
        season_id INT,
        has_values BOOLEAN,
    PRIMARY KEY (id)
);

CREATE TABLE player_stats_detailed (
        id INT,
        player_statistic_id INT,
        type_id INT,
        total INT,
        goals INT,
        penalties INT,
        home INT,
        away INT,
    PRIMARY KEY (id)
);


CREATE TABLE player_stats (
        id INT,
        player_id INT,
        team_id INT,
        season_id INT,
        has_values BOOLEAN,
        position_id INT,
        jersey_number INT,
    PRIMARY KEY (id)
);