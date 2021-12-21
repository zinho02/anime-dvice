import pandas as pd

from constraints import *


# auxiliary lib
def test_active(last_online):
    '''Derive user active status based on last online'''
    datetime_obj = datetime.strptime(last_online, '%Y-%m-%d %H:%M:%S')
    delta = NOW - datetime_obj
    return delta.days > 365 * 10 + 2


def add_active_attribute(df: pd.DataFrame):
    active = [False for x in range (len(df.index))]
    df['active'] = active
    df['active'] = df['last_online'].apply(test_active)


# userlist
# drop
def drop_userlist_access_rank(df: pd.DataFrame):
    df.drop('access_rank', axis=1, inplace=True)

def drop_userlist_stats_rewatched(df: pd.DataFrame):
    df.drop('stats_rewatched', axis=1, inplace=True)

def drop_userlist_stats_episodes(df: pd.DataFrame):
    df.drop('stats_episodes', axis=1, inplace=True)

def drop_userlist_location(df: pd.DataFrame):
    df.drop('location', axis=1, inplace=True)

# Drop in UserList
def drop_na_userlist(df: pd.DataFrame):
    usernames = df[df['birth_date'].isnull() & df['gender'].isnull()]['username']
    df.drop(df.index[usernames.index.tolist()], inplace=True)
    return usernames.tolist()
