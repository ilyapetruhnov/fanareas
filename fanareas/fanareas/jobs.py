from dagster import define_asset_job, DailyPartitionsDefinition


seasons_job = define_asset_job(name="seasons_job", selection="seasons")
teams_job = define_asset_job(name="teams_job", selection="teams")

#partitions_def = DailyPartitionsDefinition(start_date="2024-01-01")

transfers_job = define_asset_job(name="transfers_job", selection="transfers")
