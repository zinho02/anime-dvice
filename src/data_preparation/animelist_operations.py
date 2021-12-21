import numpy as np
import pandas as pd

from constraints import *


# auxiliary lib
def operate_date(val: str):
    if (len(val) == 4):
        return datetime.strptime(val, '%Y')
    if (len(val) == 9):
        return datetime.strptime(val, '%b, %Y')
    
    return datetime.strptime(val, '%b %d, %Y')

def operate_time(val: str):
    splitted = filter(len, val.split('.'))
    aux = dict({'hr': 0, 'min': 0, 'sec': 0})
    for v in splitted:
        v.replace('.','')
        v = v.strip()
        number, type_time = v.split(' ')
        if (type_time == 'hr'):
            aux['hr'] = number
        if (type_time == 'min'):
            aux['min'] = number
        if (type_time == 'sec'):
            aux['sec'] = number
    time = str(aux['hr']) + ':' + str(aux['min']) + ':' + str(aux['sec'])
    return datetime.strptime(time, '%H:%M:%S').time()

def operate_related(val: str):
    print(val)
    
# animelist
# drop
def drop_animelist_image_url(df: pd.DataFrame):
    df.drop('image_url', axis=1, inplace=True)

def drop_animelist_title(df: pd.DataFrame):
    df.drop('title', axis=1, inplace=True)

def drop_animelist_title_english(df: pd.DataFrame):
    df.drop('title_english', axis=1, inplace=True)

def drop_animelist_title_japanese(df: pd.DataFrame):
    df.drop('title_japanese', axis=1, inplace=True)

def drop_animelist_title_synonyms(df: pd.DataFrame):
    df.drop('title_synonyms', axis=1, inplace=True)

def drop_animelist_licensor(df: pd.DataFrame):
    df.drop('licensor', axis=1, inplace=True)

def drop_animelist_background(df: pd.DataFrame):
    df.drop('background', axis=1, inplace=True)

def drop_animelist_premiered(df: pd.DataFrame):
    df.drop('premiered', axis=1, inplace=True)

def drop_animelist_source(df: pd.DataFrame):
    df.drop('source', axis=1, inplace=True)

def drop_animelist_aired(df: pd.DataFrame):
    df.drop('aired', axis=1, inplace=True)

def drop_animelist_airing(df: pd.DataFrame):
    df.drop('airing', axis=1, inplace=True)

def drop_animelist_popularity(df: pd.DataFrame):
    df.drop('popularity', axis=1, inplace=True)

def drop_animelist_members(df: pd.DataFrame):
    df.drop('members', axis=1, inplace=True)
 
def drop_animelist_broadcast(df: pd.DataFrame):
    df.drop('broadcast', axis=1, inplace=True)

def drop_animelist_opening_theme(df: pd.DataFrame):
    df.drop('opening_theme', axis=1, inplace=True)

def drop_animelist_ending_theme(df: pd.DataFrame):
    df.drop('ending_theme', axis=1, inplace=True)

# transform
def transform_animelist_type(df: pd.DataFrame):
    types = df['type'].unique()
    data = {'id': list(range(0,types.size)), 'type': types.tolist()}
    animelist_type = pd.DataFrame(data)
    animelist_type.to_csv(AUXILIAR_DIR + "animelist_type.csv", index=False, encoding='utf-8')
    replacement = dict()
    for _, row in animelist_type.iterrows():
        replacement[row['type']] = row['id']

    return df.replace({'type': replacement})

def transform_animelist_status(df: pd.DataFrame):
    status = df['status'].unique()
    data = {'id': list(range(0,status.size)), 'status': status.tolist()}
    animelist_status = pd.DataFrame(data)
    animelist_status.to_csv(AUXILIAR_DIR + "animelist_status.csv", index=False, encoding='utf-8')
    replacement = dict()
    for _, row in animelist_status.iterrows():
        replacement[row['status']] = row['id']

    return df.replace({'status': replacement})

def transform_animelist_aired_string(df: pd.DataFrame):
    not_available = df[df['aired_string'].str.contains('Not available')].copy()
    not_available['aired_begin'] = np.NaN
    not_available['aired_end'] = np.NaN
    df.drop(df.loc[df['aired_string'].str.contains('Not available')].index, inplace=True)

    two_dates = df[df['aired_string'].str.contains('to')].copy()
    two_dates['aired_begin'], two_dates['aired_end'] = two_dates['aired_string'].str.split('to', 1).str
    two_dates['aired_begin'] = two_dates['aired_begin'].str.strip()
    two_dates['aired_end'] = two_dates['aired_end'].str.strip()
    two_dates['aired_end'] = two_dates['aired_end'].replace({'\?': np.NaN}, regex=True)
    df.drop(df.loc[df['aired_string'].str.contains('to')].index,inplace=True)

    df['aired_begin'] = df['aired_string']
    df['aired_end'] = np.NaN

    df = df.append(not_available)
    df = df.append(two_dates)

    df.drop('aired_string', axis=1, inplace=True)

    df['aired_begin'] = df['aired_begin'].apply(lambda value: operate_date(value) if not pd.isna(value) else value)
    df['aired_end'] = df['aired_end'].apply(lambda value: operate_date(value) if not pd.isna(value) else value)

    return df

def transform_animelist_duration(df: pd.DataFrame):
    df['duration'] = df['duration'].replace('Unknown',np.NaN)
    df['duration'] = df['duration'].replace({'per ep.': ''}, regex=True)
    df['duration'] = df['duration'].str.strip()
    df['duration'] = df['duration'].apply(lambda value: operate_time(value) if not pd.isna(value) else value)

    return df

def transform_animelist_rating(df: pd.DataFrame):
    rating = df['rating'].unique().copy()
    data = {'id': list(range(0, rating.size)), 'rating': rating.tolist()}
    animelist_rating = pd.DataFrame(data)
    animelist_rating.to_csv(AUXILIAR_DIR + "animelist_rating.csv", index=False, encoding='utf-8')
    replacement = dict()
    for _, row in animelist_rating.iterrows():
        replacement[row['rating']] = row['id']
    return df.replace({'rating': replacement})

def transform_animelist_related(df: pd.DataFrame):
    df['related'] = df['related'].replace('[]',np.NaN)
    df['related'].apply(operate_related)
