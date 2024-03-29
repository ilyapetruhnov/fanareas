# import pandas as pd
# from sqlalchemy import create_engine
# from dagster import get_dagster_logger
# from dagster import AssetKey, EnvVar

# # from dagster_embedded_elt.sling import (SlingResource, SlingSourceConnection, SlingTargetConnection)
from fanareas.ops.utils import fetch_data, base_url, upsert
import pandas as pd
from dagster import IOManager, io_manager
from dagster import (
    Field,
    IOManager,
    EnvVar,
    StringSource,
    IntSource,
    resource,
    io_manager,
)




class DbIOManager(IOManager):
    """Sample IOManager to handle loading the contents of tables as pandas DataFrames.

    Does not handle cases where data is written to different schemas for different outputs, and
    uses the name of the asset key as the table name.
    """

    def __init__(self, con_string: str):
        self._con = con_string

    def handle_output(self, context, obj):
        if isinstance(obj, pd.DataFrame):
            # write df to table
            obj.set_index('id').to_sql(name=context.asset_key.path[-1], con=self._con, if_exists="replace")
        elif obj is None:
            # dbt has already written the data to this table
            pass
        else:
            raise ValueError(f"Unsupported object type {type(obj)} for DbIOManager.")

    def load_input(self, context) -> pd.DataFrame:
        """Load the contents of a table as a pandas DataFrame."""
        model_name = context.asset_key.path[-1]
        #context.add_output_metadata({"table_name": model_name})
        return pd.read_sql(f"SELECT * FROM {model_name}", con=self._con)
    
    def upsert_input(self, context) -> pd.DataFrame:
        dataset_name = context.asset_key.path[-1]
        try:
            existing_df = self.load_input(context)
            last_id = max(existing_df['id'])
            url = f"{base_url}/{dataset_name}?filters=idAfter:{last_id}"
        except Exception as e:
            existing_df = pd.DataFrame([])
            url = f"{base_url}/{dataset_name}"
        new_df = fetch_data(url)
        merged_df = upsert(existing_df, new_df)
        context.log.info(merged_df.head())
        return merged_df


@io_manager(config_schema={"con_string": str})
def db_io_manager(context):
    return DbIOManager(context.resource_config["con_string"])

