from dagster import asset
import pandas as pd
from fanareas.ops.utils import api_call, fetch_data, base_url, get_fields, get_records, get_ids_from_db_col, db_insert
from itertools import product
import datetime

@asset
def seasons_df() -> pd.DataFrame:
    df = fetch_data(f"{base_url}/seasons")
    return df

@asset()
def db_insert_seasons(context, seasons_df: pd.DataFrame) -> pd.DataFrame:
    try:
        context.log.info(seasons_df.head())
        table = 'seasons'
        db_insert(df = seasons_df, table_name = table)
        return seasons_df
    except Exception as e:
        context.log.info(str(e))

@asset
def season_ids(db_insert_seasons) -> list:
    season_ids = get_ids_from_db_col(table_name='seasons')
    return season_ids

@asset
def teams_df(season_ids) -> pd.DataFrame:
    teams_records_set = set()
    for season_id in season_ids:
        teams_url = f"{base_url}/teams/seasons/{season_id}"
        response_teams = api_call(teams_url)
        team_records = get_records(response_teams)
        for team in team_records:
            teams_records_set.add(team)
    teams_fields = get_fields(response_teams)
    df = pd.DataFrame.from_records(list(teams_records_set), columns=teams_fields)
    return df

@asset()
def db_insert_teams(context, teams_df: pd.DataFrame) -> pd.DataFrame:
    try:
        context.log.info(teams_df.head())
        table = 'teams'
        db_insert(df = teams_df, table_name = table)
        return teams_df
    except Exception as e:
        context.log.info(str(e))

@asset
def team_ids(db_insert_teams) -> list:
    team_ids = get_ids_from_db_col(table_name='teams')
    return team_ids

@asset
def squads_df(season_ids, team_ids) -> pd.DataFrame:
    combinations = list(product(season_ids, team_ids))
    squads = []
    for season_id, team_id in combinations:
        players_url = f"{base_url}/squads/seasons/{season_id}/teams/{team_id}"
        response_players = api_call(players_url)
        try:
            squads.append(response_players.json()['data'])
        except Exception as e:
            pass
    squads_records = set()
    data_size = len(squads)
    for i in range(data_size):
        data_sz = len(squads[i])
        for item in range(data_sz):
            squads_records.add(tuple(squads[i][item].values()))
    squads_fields = tuple(squads[0][0].keys())
    df = pd.DataFrame.from_records(list(squads_records), columns=squads_fields)
    return df


@asset()
def db_insert_squads(context, squads_df: pd.DataFrame) -> bool:
    try:
        context.log.info(squads_df.head())
        table = 'squads'
        db_insert(df = squads_df, table_name = table)
        return True
    except Exception as e:
        context.log.info(str(e))

@asset
def transfers_today_df(context):
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    url = f"{base_url}/transfers/between/{date}/{date}"
    transfers_today_df = fetch_data(url)
    print(context.get_tag("date"))
    context.log.info(transfers_today_df.head())
    return transfers_today_df

@asset()
def db_insert_transfers(context, transfers_today_df: pd.DataFrame) -> bool:
    try:
        context.log.info(transfers_today_df.head())
        table = 'transfers'
        db_insert(df = transfers_today_df, table_name = table)
        return True
    except Exception as e:
        context.log.info(str(e))






