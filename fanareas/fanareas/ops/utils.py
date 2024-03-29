import requests
import pandas as pd
import os
from itertools import chain
from sqlalchemy import MetaData, Table, select
from dagster import op
import time


api_key = os.getenv("api_key")
base_url = os.getenv("base_url")
core_url = os.getenv("core_url")

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

def fetch_data(context, url):
    data = []
    result = api_call(url)
    while 'data' in result.json().keys():
        data.append(result.json()['data'])
        url = result.json()['pagination']['next_page']
        limit = result.json()['rate_limit']['remaining']
        if limit == 1:
            seconds_until_reset = result.json()['rate_limit']['resets_in_seconds']
            context.log.info(seconds_until_reset)
            time.sleep(seconds_until_reset)
            continue
        else:
            has_more = result.json()['pagination']['has_more']
            if has_more == False:
                break
            result = api_call(url)
    result_df = pd.DataFrame(list(chain(*data)))  
    return result_df

@op
def upsert(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    # Perform upsert (merge) based on the 'id' column
    merged_df = pd.concat([existing_df, new_df], ignore_index=True)
    merged_df = merged_df.drop_duplicates(subset='id', keep='last')
    return merged_df

@op
def flatten_list(nested_list):
    flattened_list = []
    for item in nested_list:
        if isinstance(item, list):
            flattened_list.extend(flatten_list(item))
        else:
            flattened_list.append(item)
    return flattened_list
