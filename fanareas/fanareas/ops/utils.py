import requests
import pandas as pd
import os
import sqlalchemy
import psycopg2
from sqlalchemy import MetaData, Table, select
from dagster import op


api_key = os.getenv("api_key")
base_url = os.getenv("base_url")

@op
def create_db_connection():
    uid = os.getenv("uid")
    pwd = os.getenv("pwd")
    server = os.getenv("server")
    port = os.getenv("port")
    db = os.getenv("db")
    url = f"postgresql://{uid}:{pwd}@{server}:{port}/{db}"
    engine = sqlalchemy.create_engine(url)
    return engine

@op
def get_records(response):
    records=[]
    data = response.json()['data']
    if type(data) == list:
        for i in range(len(data)):
            records.append(tuple(data[i].values()))
    else:
        records.append(tuple(data.values()))
    return records

@op
def get_fields(response):
    data = response.json()['data']
    if type(data) == list:
        keys = tuple(data[0].keys())
    else:
        keys = tuple(data.keys())
    return keys

@op
def api_call(url):
    headers = { 'Authorization': api_key }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        print(f"Error: {response.status_code}")
        return None

@op
def fetch_data(api_url):
    data = []
    while True:
        result = api_call(api_url)
        data.append(result.json()['data'])
        api_url = result.json()['pagination']['next_page']
        has_more = result.json()['pagination']['has_more']
        if has_more == False:
            break
    result = pd.DataFrame(data[0])
    return result

@op
def db_insert(df: pd.DataFrame, table_name: str) -> bool:
    conn = create_db_connection()
    df.to_sql(table_name, con=conn, index=False, if_exists="replace")
    return True

@op
def db_upsert(df: pd.DataFrame, table_name: str) -> bool:
    conn = create_db_connection()
    engine = conn.connect()
    ids = tuple(df['id'].unique())
    engine.execute(f"""delete from {table_name} where id in {ids}""")
    df.to_sql(table_name, con=conn, index=False, if_exists="append")
    return True

@op
def get_ids_from_db_col(table_name: str):
    engine = create_db_connection()

    metadata = MetaData()

    table = Table(table_name, metadata, autoload_with=engine)
    column_name = 'id'
    # Establish a connection
    connection = engine.connect()

    # Create a SELECT statement
    distinct_values_query = select(table.c[column_name].distinct())

    # Execute the query
    result = connection.execute(distinct_values_query)

    # Fetch the results
    rows = result.fetchall()

    # Process the results
    results = [i[0] for i in rows]

    # Close the connection
    connection.close()
    return results
