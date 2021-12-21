from datetime import datetime

RESOURCES_DIR = "/home/ggiacomoni/ufsc/datamining/data-mining/resources/"
DATA_DIR = RESOURCES_DIR + "data/"
PLAIN_DIR = DATA_DIR + "plain/"
FILTERED_DIR = DATA_DIR + "filtered/"
CLEANED_DIR = DATA_DIR + "cleaned/"
AUXILIAR_DIR = DATA_DIR + "aux/"

# PLAIN_DIR
ANIMELIST_FILE = PLAIN_DIR + "AnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=AnimeList.csv
USERANIMELIST_FILE = PLAIN_DIR + "UserAnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserAnimeList.csv
USERLIST_FILE = PLAIN_DIR + "UserList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserList.csv

# AUXILIARY_DIR
ANIMELIST_TYPE_FILE = AUXILIAR_DIR + "animelist_type.csv"
ANIMELIST_STATUS_FILE = AUXILIAR_DIR + "animelist_status.csv"
ANIMELIST_RATING_FILE = AUXILIAR_DIR + "animelist_rating.csv"
ANIMELIST_RELATED_FILE = AUXILIAR_DIR + "animelist_related.csv"
ANIMELIST_GENRE_FILE = AUXILIAR_DIR + "animelist_genre.csv"

NOW = datetime.utcnow()
