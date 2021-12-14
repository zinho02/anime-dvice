import numpy as np
import pandas as pd
import os

# Directories
RESOURCES_DIR = "../../resources/"
DATA_DIR = RESOURCES_DIR + "data/"

ANIMELIST_FILE = DATA_DIR + "AnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=AnimeList.csv
USERANIMELIST_FILE = DATA_DIR + "UserAnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserAnimeList.csv
USERLIST_FILE = DATA_DIR + "UserList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserList.csv

# Data Frames
animelist_df = pd.read_csv(ANIMELIST_FILE)
print(animelist_df.head())

# Big CSV
chunksize = 10 ** 6
with pd.read_csv(USERANIMELIST_FILE, chunksize=chunksize) as useranimelist_reader:
    for useranimelist_chunk in useranimelist_reader:
        print(useranimelist_chunk.head())

userlist_df = pd.read_csv(USERLIST_FILE)
print(userlist_df.head())
