"""Definitions that provide Dagster code locations."""
from dagster import Definitions, asset, define_asset_job, job

from fanareas.assets.assets import seasons_df,db_insert_seasons,season_ids,teams_df,db_insert_teams,team_ids, db_insert_teams,squads_df,db_insert_squads, transfers_today_df, db_insert_transfers
from fanareas.jobs import seasons_job, teams_job, transfers_job
from fanareas.schedules import teams_schedule, transfers_schedule
# get_transfers_by_date, db_insert_transfers
# from fanareas.jobs import complex_job, hello_cereal_job
# from fanareas.schedules import every_weekday_9am

# all_assets = load_assets_from_modules([assets_productcategory, assets_dataanalysis])
# seasons_job = define_asset_job(name="seasons_job", selection="db_insert_seasons")

defs = Definitions(
    assets=[
        seasons_df,
            db_insert_seasons,
            season_ids,
            teams_df,
            team_ids,
            db_insert_teams,
            squads_df,
            db_insert_squads,
            transfers_today_df,
            db_insert_transfers
            ],
    jobs=[seasons_job, teams_job, transfers_job],
    schedules=[teams_schedule, transfers_schedule],
)


