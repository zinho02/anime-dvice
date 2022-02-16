import os
from pyexpat import model
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from datetime import datetime
import os

from datetime import datetime
import os

RESOURCES_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))
DATA_DIR = os.path.join(RESOURCES_DIR, "data")
PLAIN_DIR = os.path.join(DATA_DIR, "plain")
FILTERED_DIR = os.path.join(DATA_DIR, "filtered")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")
AUXILIAR_DIR = os.path.join(DATA_DIR, "aux")

# PLAIN_DIR
ANIMELIST_FILE = os.path.join(PLAIN_DIR, "AnimeList.csv") # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=AnimeList.csv
USERANIMELIST_FILE = os.path.join(PLAIN_DIR, "UserAnimeList.csv") # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserAnimeList.csv
USERLIST_FILE = os.path.join(PLAIN_DIR, "UserList.csv") # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserList.csv

# FILTERED_DIR
FILTERED_ANIMELIST_FILE = os.path.join(FILTERED_DIR, "AnimeListFiltered.csv")
FILTERED_USERANIMELIST_FILE = os.path.join(FILTERED_DIR, "UserAnimeListFiltered.csv")
FILTERED_USERLIST_FILE = os.path.join(FILTERED_DIR, "UserListFiltered.csv")

# AUXILIARY_DIR
ANIMELIST_TYPE_FILE = os.path.join(AUXILIAR_DIR, "animelist_type.csv")
ANIMELIST_STATUS_FILE = os.path.join(AUXILIAR_DIR, "animelist_status.csv")
ANIMELIST_RATING_FILE = os.path.join(AUXILIAR_DIR, "animelist_rating.csv")
ANIMELIST_RELATED_FILE = os.path.join(AUXILIAR_DIR, "animelist_related.csv")
ANIMELIST_GENRE_FILE = os.path.join(AUXILIAR_DIR, "animelist_genre.csv")

NOW = datetime.utcnow()

FEATURES = ["episodes", "status", "score"]   

def list_type():
    type_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_type.csv"), index_col=1, squeeze=True).to_dict()
    for type in type_dict:
        FEATURES.append(type)
        
def list_rating():
    rating_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_rating.csv"), index_col=1, squeeze=True).to_dict()
    for rating in rating_dict:
        FEATURES.append(rating)
        
def list_genre():
    genre_dict = pd.read_csv(os.path.join(AUXILIAR_DIR, "animelist_genre_dict.csv"), index_col=0, squeeze=True).to_dict()
    for genre in genre_dict:
        FEATURES.append(genre)
     
def list_features():
    list_type()
    list_rating()
    list_genre()
    
def find(anime_id):
    teste = model_knn.kneighbors(animelist_df.iloc[[anime_id]][FEATURES], n_neighbors=2)
    print(animelist_df.iloc[[anime_id]]["title"])
    print(animelist_df.iloc[[teste[1][0][1]]]["title"])

if __name__ == '__main__':
    list_features()
    animelist_df = pd.read_csv(FILTERED_ANIMELIST_FILE)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(animelist_df[FEATURES])
    find(700)
    