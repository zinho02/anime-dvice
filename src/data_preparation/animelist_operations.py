import json

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

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

def json_convert(string) -> json:
    if(type(string) == dict):
        return json.loads(json.dumps(string))
    new_string = str(string).replace('"', '*special_char*')
    new_string = str(new_string).replace('\'', '"')
    new_string = str(new_string).replace('*special_char*', '\'')
    return json.loads(new_string)

def operate_related(anime_id: int, related: str, df: DataFrame):
    related_json = json_convert(related)

    data = pd.DataFrame()
    data.loc[0, 'anime_id'] = anime_id
    # data.set_index('anime_id', inplace=True)

    for relation_type in related_json.keys():
        for relation in related_json[relation_type]:
            relation_json = json_convert(relation)
            if (df[(df['anime_id'] == relation_json['mal_id']) & (df['title'] == relation_json['title'])]['anime_id'].shape[0] > 0):
                relation_type_formatted = (relation_type.lower()).replace(' ', '_')
                data.loc[0, relation_type_formatted] = relation_json['mal_id']
    
    return data

def convert_genre(string: str):
    string = string.replace(', ', ',')
    string = string.replace(' ', '_')
    string = string.lower()
    return string.split(',')

# animelist
# drop
def drop_animelist_image_url(df: pd.DataFrame):
    df.drop('image_url', axis=1, inplace=True)

# def drop_animelist_title(df: pd.DataFrame):
#     df.drop('title', axis=1, inplace=True)

# def drop_animelist_title_english(df: pd.DataFrame):
#     df.drop('title_english', axis=1, inplace=True)

# def drop_animelist_title_japanese(df: pd.DataFrame):
#     df.drop('title_japanese', axis=1, inplace=True)

# def drop_animelist_title_synonyms(df: pd.DataFrame):
#     df.drop('title_synonyms', axis=1, inplace=True)

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

def drop_animelist_producer(df: pd.DataFrame):
    df.drop('producer', axis=1, inplace=True)

def drop_animelist_studio(df: pd.DataFrame):
    df.drop('studio', axis=1, inplace=True)

# transform
def transform_animelist_type(df: pd.DataFrame):
    types = df['type'].unique()
    animelist_type = pd.DataFrame({'id': list(range(0,types.size)), 'type': types.tolist()})
    animelist_type.to_csv(ANIMELIST_TYPE_FILE, index=False, encoding='utf-8')
    replacement = dict()
    for _, row in animelist_type.iterrows():
        replacement[row['type']] = row['id']

    return df.replace({'type': replacement})

def transform_animelist_status(df: pd.DataFrame):
    status = df['status'].unique()
    animelist_status = pd.DataFrame({'id': list(range(0,status.size)), 'status': status.tolist()})
    animelist_status.to_csv(ANIMELIST_STATUS_FILE, index=False, encoding='utf-8')
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
    animelist_rating.to_csv(ANIMELIST_RATING_FILE, index=False, encoding='utf-8')
    replacement = dict()
    for _, row in animelist_rating.iterrows():
        replacement[row['rating']] = row['id']
    return df.replace({'rating': replacement})

def transform_animelist_related(df: pd.DataFrame):
    new_df = pd.DataFrame()
    for _, row in df.iterrows():
        if (not row['related'] == '[]'):
            new_row = operate_related(row['anime_id'], row['related'], df)
            new_df = new_df.append(new_row, ignore_index = True)
    new_df.to_csv(ANIMELIST_RELATED_FILE, index=False, encoding='utf-8')

    df.drop('related', axis=1, inplace=True)

def transform_animelist_genre(df: pd.DataFrame):
    # drop null values
    df = df.dropna(subset=['genre'])
    df['genre'] = df['genre'].apply(convert_genre)
    genres = set()
    for _, row in df.iterrows():
        for gen in row['genre']:
            genres.add(gen)

    genres_list = list(genres)

    for i in df.index:
        new_list = list()
        for gen in df.at[i, 'genre']:
            new_list.append(genres_list.index(gen))
        df.at[i, 'genre'] = new_list

    animelist_genres = pd.DataFrame({'id': range(0,len(genres_list)), 'genre': genres_list})
    animelist_genres.to_csv(ANIMELIST_GENRE_FILE, index=False, encoding='utf-8')
    return df

def columns_types(df: pd.DataFrame): 
    type_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_type.csv"), index_col=1, squeeze=True).to_dict()
    for key in type_dict:
        df[key] = df.apply(lambda x: encode_types(key, x["type"]), axis=1)
    return df

def encode_types(curr_type: str, type: str):
    if (curr_type == type):
        return 1
    return 0

def columns_genres(df: pd.DataFrame):
    genre_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_genre_dict.csv"), index_col=0, squeeze=True).to_dict()
    for key in genre_dict:
        df[key] = 0
    for key in genre_dict:
        df[key] = df.apply(lambda x: encode_genres(key, x["genre"]), axis=1)
    return df
    

def encode_genres(curr_genre: str, genres: str):
    if (not isinstance(genres, str)):
        return 0
    genres = genres.split(", ")
    if curr_genre in genres:
        return 1
    return 0
    
def columns_rating(df: pd.DataFrame): 
    rating_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_rating.csv"), index_col=1, squeeze=True).to_dict()
    for key in rating_dict:
        df[key] = df.apply(lambda x: encode_ratings(key, x["rating"]), axis=1)
    return df

def encode_ratings(curr_rating: str, rating: str):
    if (curr_rating == rating):
        return 1
    return 0

def encode_animelist_status(df: pd.DataFrame):
    status_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_status.csv"), index_col=1, squeeze=True).to_dict()
    df.replace({"status": status_dict}, inplace=True)
    return df
