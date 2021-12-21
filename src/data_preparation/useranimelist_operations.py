import pandas as pd


# useranimelist
# drop columns
def drop_useranimelist_my_status(df: pd.DataFrame):
    df.drop('my_status', axis=1, inplace=True)

def drop_useranimelist_my_rewatching(df: pd.DataFrame):
    df.drop('my_rewatching', axis=1, inplace=True)
    
def drop_useranimelist_my_rewatching_ep(df: pd.DataFrame):
    df.drop('my_rewatching_ep', axis=1, inplace=True)
    
def drop_useranimelist_my_tags(df: pd.DataFrame):
    df.drop('my_tags', axis=1, inplace=True)

# drop data
def drop_na_useranimelist(df: pd.DataFrame, usernames_to_drop):
    usernames = df[df['username'].isin(usernames_to_drop)].index
    df.drop(usernames, inplace=True)
