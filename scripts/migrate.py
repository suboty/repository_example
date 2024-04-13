import ast
from pathlib import Path

from tqdm import tqdm
import requests
import pandas as pd

REPOSITORY_URL = 'http://localhost:8786/v0'

if __name__ == '__main__':
    source_data = pd.read_csv(Path('data', 'source.csv')).fillna('')

    data = pd.read_csv(Path('data', 'merged_output_tsv.csv'), on_bad_lines='skip', sep='\t').fillna('')

    try:
        print('Migrate rss messages...')
        for data_iloc in tqdm(data.iloc):
            json_for_repository = {
                "link": data_iloc['link'],
                "title": data_iloc['title'],
                "description": data_iloc['description'],
                "tags_array": ast.literal_eval(data_iloc['tags_array']),
                "categories_array": ast.literal_eval(data_iloc['categories_array']),
                "enclosures_tuples": [str(x) for x in ast.literal_eval(data_iloc['enclosures_tuples'])],
                "author": data_iloc['author'],
                "guid": data_iloc['guid'],
                "source_hash": data_iloc['source_hash'],
                "public_time": data_iloc['public_time'],
                "source_time": data_iloc['source_time']
            }

            res = requests.post(url=f'{REPOSITORY_URL}/rss_messages/', json=json_for_repository).json()

        print('Migrate rss sources...')
        for source_data_iloc in tqdm(source_data.iloc):
            json_for_repository = {
                "source_name": source_data_iloc['source_name'],
                "source_description": source_data_iloc['source_description'],
                "site_url": source_data_iloc['site_url'],
                "rss_url": source_data_iloc['rss_url'],
                "source_hash": source_data_iloc['source_hash'],
                "source_time": source_data_iloc['source_time']
            }

            res = requests.post(url=f'{REPOSITORY_URL}/sources/', json=json_for_repository).json()

    except requests.exceptions.ConnectionError:
        print('Error while connection! Canceled')
        exit(111)
    except Exception as e:
        print(f'Error while loading data! Exception: {e}')
