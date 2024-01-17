"""Collection of Cereal schedules"""

from dagster import ScheduleDefinition
from fanareas.jobs import transfers_job, teams_job

transfers_schedule = ScheduleDefinition(job=transfers_job, cron_schedule="* * * * *")

teams_schedule = ScheduleDefinition(job=teams_job, cron_schedule="0 * * * *")
