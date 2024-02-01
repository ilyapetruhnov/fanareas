"""Definitions that provide Dagster code locations."""
from dagster import Definitions, asset, define_asset_job, job, load_assets_from_modules
from fanareas.assets import assets
from fanareas.jobs import seasons_job, teams_job, transfers_job
from fanareas.schedules import teams_schedule, transfers_schedule
from fanareas.resources.db_io_manager import db_io_manager
from fanareas.resources.db_params import POSTGRES_CONFIG
# get_transfers_by_date, db_insert_transfers
# from fanareas.jobs import complex_job, hello_cereal_job
# from fanareas.schedules import every_weekday_9am

all_assets = load_assets_from_modules([assets])
# io_manager_postgres = db_io_manager.configured(
#                 {
#                 "server": {"env": "server"},
#                 "db": {"env": "db"},
#                 "uid": {"env": "uid"},
#                 "pwd": {"env": "pwd"},
#                 "port": {"env": "port"}
#             }
# )
# seasons_job = define_asset_job(name="seasons_job", selection="db_insert_seasons")

defs = Definitions(
    assets=[*all_assets],
    jobs=[seasons_job, teams_job, transfers_job],
    schedules=[teams_schedule, transfers_schedule],
    resources = {"db_io_manager": db_io_manager.configured(POSTGRES_CONFIG)}
    
    )


