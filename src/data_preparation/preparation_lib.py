import os
from datetime import datetime

import numpy as np
import pandas as pd

from animelist_operations import *
from useranimelist_operations import *
from userlist_operations import *


def process_animelist(df: pd.DataFrame):
    # Drop data
    drop_animelist_title(df)
    drop_animelist_title_english(df)
    drop_animelist_title_japanese(df)
    drop_animelist_title_synonyms(df)
    drop_animelist_image_url(df)
    drop_animelist_source(df)
    drop_animelist_aired(df)
    drop_animelist_airing(df)
    drop_animelist_popularity(df)
    drop_animelist_members(df)
    drop_animelist_background(df)
    drop_animelist_premiered(df)
    drop_animelist_broadcast(df)
    drop_animelist_licensor(df)
    drop_animelist_opening_theme(df)
    drop_animelist_ending_theme(df)

    # Transform
    df = transform_animelist_type(df)
    df = transform_animelist_status(df)
    df = transform_animelist_aired_string(df)
    df = transform_animelist_duration(df)
    df = transform_animelist_rating(df)

    return df

def process_useranimelist(df: pd.DataFrame, usernames_to_drop):
    # Drop data
    drop_useranimelist_my_rewatching(df)
    drop_useranimelist_my_rewatching_ep(df)
    drop_useranimelist_my_status(df)
    drop_useranimelist_my_tags(df)
    drop_na_useranimelist(df, usernames_to_drop)
    return df

def process_userlist(df: pd.DataFrame):
    # Drop data
    drop_userlist_access_rank(df)
    drop_userlist_location(df)
    drop_userlist_stats_episodes(df)
    drop_userlist_stats_rewatched(df)
    # Drop rows with at least one null value in : birth_date, gender
    usernames_to_drop = drop_na_userlist(df)
    return df, usernames_to_drop


if __name__ == '__main__':
    # Data Frames
    animelist_df = pd.read_csv(ANIMELIST_FILE)
    process_animelist(animelist_df)
    animelist_df.to_csv(FILTERED_DIR + "AnimeListFiltered.csv", index=False, encoding='utf-8')

    userlist_df = pd.read_csv(USERLIST_FILE)
    _, usernames_to_drop = process_userlist(userlist_df)
    userlist_df.to_csv(FILTERED_DIR + "UserListFiltered.csv", index=False, encoding='utf-8')

    notaired_animelist_df = animelist_df[animelist_df['status'] == 'Not yet aired']
    notaired_ids = notaired_animelist_df['anime_id']

    # Big CSV
    chunksize = 10 ** 6
    header = True
    useranimelist_reader = pd.read_csv(USERANIMELIST_FILE, chunksize=chunksize)
    for useranimelist_chunk in useranimelist_reader:
        process_useranimelist(useranimelist_chunk, usernames_to_drop)
        useranimelist_chunk = useranimelist_chunk[~useranimelist_chunk['anime_id'].isin(notaired_ids)]
        useranimelist_chunk.to_csv(FILTERED_DIR + "UserAnimeListFiltered.csv", index=False, encoding='utf-8', mode='a', header=header)
        header = False
