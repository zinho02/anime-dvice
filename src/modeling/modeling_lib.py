import os
from pyexpat import model
from turtle import goto
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
    
def title_anime_recommend_by_title(model, title: str, df: pd.DataFrame, n=2):
    anime = find_anime_by_all_titles(title, df)
    kneighbors = model.kneighbors(anime[FEATURES], n_neighbors=n+1)
    animes_recommended = list()
    for i in range(1, n+1):
        animes_recommended.append(str(df.iloc[[kneighbors[1][0][i]]]["title"]))
    return animes_recommended
    
def recommend_by_title(model, title: str, df: pd.DataFrame, n=2):
    anime = find_anime_by_all_titles(title, df)
    kneighbors = model.kneighbors(anime[FEATURES], n_neighbors=n+1)
    animes_recommended = list()
    for i in range(1, n+1):
        animes_recommended.append(int(df.iloc[[kneighbors[1][0][i]]]["anime_id"]))
    return animes_recommended
    
def recommend_by_id(model, anime_id: int, df: pd.DataFrame, n=2):
    anime = find_anime_by_id(anime_id, df)
    kneighbors = model.kneighbors(anime[FEATURES], n_neighbors=n+1)
    animes_recommended = list()
    for i in range(1, n+1):
        animes_recommended.append(int(df.iloc[[kneighbors[1][0][i]]]["anime_id"]))
    return animes_recommended
        
    
def find_anime_by_id(anime_id: int, df: pd.DataFrame):
    return df.loc[df["anime_id"] == anime_id]
    
def find_anime_by_all_titles(title: str, df: pd.DataFrame):
    functions = [find_anime_by_title, find_anime_by_title_english, find_anime_by_title_synonyms, find_anime_by_title_japanese]
    anime = None
    for i in range(len(functions)):
        anime = functions[i](title, df)
        if (not anime.empty):
            return anime
    raise Exception("Anime não encontrado")
    
def find_anime_by_title(title: str, df: pd.DataFrame):
    return df.loc[df["title"] == title]

def find_anime_by_title_english(title_english: str, df: pd.DataFrame):
    return df.loc[df["title_english"] == title_english]

def find_anime_by_title_japanese(title_japanese: str, df: pd.DataFrame):
    return df.loc[df["title_japanese"] == title_japanese]

def find_anime_by_title_synonyms(title_synonyms: str, df: pd.DataFrame):
    return df.loc[df["title_synonyms"] == title_synonyms]

def build_model_knn(metric: str, algorithm: str, df: pd.DataFrame, radius = 1.0, leaf_size = 30):
    p = 2
    if (metric == 'minkowski'):
        p = 4
    model_knn = NearestNeighbors(metric = metric, algorithm = algorithm, radius = radius, leaf_size = leaf_size, p = p)
    model_knn.fit(df[FEATURES])
    return model_knn

def build_model_knn_radius(metric: str, algorithm: str, df: pd.DataFrame, radius: float):
    return build_model_knn(metric = metric, algorithm = algorithm, df = df, radius = radius)

METRICS = ['euclidean', 'manhattan', 'minkowski']
ALGORITHMS = ['kd_tree']

def build_models_knn(radius: float, leaf_size: int, animelist_df: pd.DataFrame):
    models = list()
    for algorithm in ALGORITHMS:
        for metric in METRICS:
            models.append(build_model_knn(metric, algorithm, animelist_df, radius, leaf_size))
    return models
            
def test_model_knn(model, usernames: list, useranimelist_df: pd.DataFrame, animelist_df: pd.DataFrame):
    favorites = build_favorites_dict(usernames, useranimelist_df)
    score = 0
    for username in favorites:
        recommendeds = recommend_by_id(model, favorites[username][0], animelist_df, 20)
        score_username = 0
        for recommended in recommendeds:
            if (recommended in favorites[username]):
                score_username = score_username + 1
        score_username = score_username / len(recommendeds)      
        score = score + score_username
    score = score / len(favorites)
    print("O modelo com a métrica = " + str(model.effective_metric_) + " teve score = " + str(score))
    
            
def build_favorites_dict(usernames: list, useranimelist_df: pd.DataFrame, min_score = 8):
    favorites = {}
    for username in usernames:
        favorites_list = useranimelist_df[useranimelist_df["username"] == username]
        favorites_list = useranimelist_df[useranimelist_df["my_score"] > min_score]
        favorites_list = favorites_list["anime_id"].to_list()
        if len(favorites_list) > 0:
            favorites[username] = favorites_list
        
    return favorites
        

def test_models_knn(models: list, animelist_df: pd.DataFrame):
    nrows = 1000
    useranimelist_df = pd.read_csv(FILTERED_USERANIMELIST_FILE, nrows=nrows * 100)
    userlist_df = pd.read_csv(FILTERED_USERLIST_FILE, nrows=nrows)
    usernames = userlist_df["username"].to_list()
    for model in models:
        test_model_knn(model, usernames, useranimelist_df, animelist_df)
        
def test():
    list_features()
    animelist_df = pd.read_csv(FILTERED_ANIMELIST_FILE)
    
    for i in range(len(RADIUS)):
        for j in range(len(LEAF_SIZE)):
            print("Testando com os parâmetros:\nRaio = " + str(RADIUS[i]) + "\nQuantidade do nós folha = " + str(LEAF_SIZE[j]))
            models = build_models_knn(RADIUS[i], LEAF_SIZE[j], animelist_df)
            test_models_knn(models, animelist_df)
            
def cli():
    list_features()
    animelist_df = pd.read_csv(FILTERED_ANIMELIST_FILE)
    model = build_model_knn('euclidean', 'kd_tree', animelist_df, radius = 1.0, leaf_size=30)
    
    while True:
        next_anime = True
        anime_title = input("Qual o título do anime que você gosta?\n")
        n = int(input("Quantos animes você gostaria de ser recomendado?\n"))
        recommendations = get_recommendations(anime_title, model, animelist_df, n)
        for recommendation in recommendations:
            print(recommendation.split("\n")[0].split("    ")[1])
        while True:
            next = input("Gostaria de outra recomendação? (S/N)\n")
            if (next == "N".casefold()):
                next_anime = False
                break
            elif (next == "S".casefold()):
                next_anime = True
                break
        if (not next_anime):
            break
        
            
RADIUS=[1, 1.5, 2, 2.5, 3]  

LEAF_SIZE=[30, 40, 50, 60, 70]

def get_recommendations(anime_title: str, model, df: pd.DataFrame, n: int):
    return title_anime_recommend_by_title(model, anime_title, df, n=n)

if __name__ == '__main__':
    # test()
    cli()
    