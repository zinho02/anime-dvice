import numpy as np
import pandas as pd
import os

# Directories
RESOURCES_DIR = "resources/"
DATA_DIR = RESOURCES_DIR + "data/"
PLAIN_DIR = DATA_DIR + "plain/"
FILTERED_DIR = DATA_DIR + "filtered/"
CLEANED_DIR = DATA_DIR + "cleaned/"

ANIMELIST_FILE = PLAIN_DIR + "AnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=AnimeList.csv
USERANIMELIST_FILE = PLAIN_DIR + "UserAnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserAnimeList.csv
USERLIST_FILE = PLAIN_DIR + "UserList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserList.csv

# Drop columns with no meaning identified
def drop_useranimelist_my_status(df):
    df.drop('my_status', axis=1, inplace=True)

def drop_useranimelist_my_rewatching(df):
    df.drop('my_rewatching', axis=1, inplace=True)
    
def drop_useranimelist_my_rewatching_ep(df):
    df.drop('my_rewatching_ep', axis=1, inplace=True)
    
def drop_useranimelist_my_tags(df):
    df.drop('my_tags', axis=1, inplace=True)

def drop_animelist_source(df):
    df.drop('source', axis=1, inplace=True)

def drop_animelist_popularity(df):
    df.drop('popularity', axis=1, inplace=True)

def drop_animelist_members(df):
    df.drop('members', axis=1, inplace=True)
 
def drop_animelist_broadcast(df):
    df.drop('broadcast', axis=1, inplace=True)

def drop_userlist_access_rank(df):
    df.drop('access_rank', axis=1, inplace=True)

def drop_userlist_stats_rewatched(df):
    df.drop('stats_rewatched', axis=1, inplace=True)

def drop_userlist_stats_episodes(df):
    df.drop('stats_episodes', axis=1, inplace=True)

# Drop demographic data
def drop_userlist_location(df):
    df.drop('location', axis=1, inplace=True)
    
# Drop rows with at least one null value in : birth_date, gender

usernames_to_drop = []

# Drop in UserList
def drop_na_userlist(df):
    usernames = df[df['birth_date'].isnull() & df['gender'].isnull()]['username']
    df.drop(df.index[usernames.index.tolist()], inplace=True)
    usernames_to_drop = usernames.tolist()

# Drop in UserAnimeList
def drop_na_useranimelist(df):
    usernames = df[df['username'].isin(usernames_to_drop)].index
    df.drop(usernames, inplace=True)
    
def process_useranimelist(df):
    # Drop data
    drop_useranimelist_my_rewatching(df)
    drop_useranimelist_my_rewatching_ep(df)
    drop_useranimelist_my_status(df)
    drop_useranimelist_my_tags(df)
    drop_na_useranimelist(df)
    return df
    
    
def process_animelist(df):
    # Drop data
    drop_animelist_broadcast(df)
    drop_animelist_members(df)
    drop_animelist_popularity(df)
    drop_animelist_source(df)
    return df
    
def process_userlist(df):
    # Drop data
    drop_userlist_access_rank(df)
    drop_userlist_location(df)
    drop_userlist_stats_episodes(df)
    drop_userlist_stats_rewatched(df)
    drop_na_userlist(df)
    return df

# Data Frames
animelist_df = pd.read_csv(ANIMELIST_FILE)
process_animelist(animelist_df)
animelist_df.to_csv(FILTERED_DIR + "AnimeListFiltered.csv", index=False, encoding='utf-8')

userlist_df = pd.read_csv(USERLIST_FILE)
process_userlist(userlist_df)
userlist_df.to_csv(FILTERED_DIR + "UserListFiltered.csv", index=False, encoding='utf-8')

# Big CSV
chunksize = 10 ** 6
header = True
with pd.read_csv(USERANIMELIST_FILE, chunksize=chunksize) as useranimelist_reader:
   for useranimelist_chunk in useranimelist_reader:
       process_useranimelist(useranimelist_chunk)
       useranimelist_chunk.to_csv(FILTERED_DIR + "UserAnimeListFiltered.csv", index=False, encoding='utf-8', mode='a', header=header)
       header = False