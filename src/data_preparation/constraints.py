from datetime import datetime

RESOURCES_DIR = "/home/ggiacomoni/ufsc/datamining/data-mining/resources/"
DATA_DIR = RESOURCES_DIR + "data/"
PLAIN_DIR = DATA_DIR + "plain/"
FILTERED_DIR = DATA_DIR + "filtered/"
CLEANED_DIR = DATA_DIR + "cleaned/"
AUXILIAR_DIR = DATA_DIR + "aux/"

ANIMELIST_FILE = PLAIN_DIR + "AnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=AnimeList.csv
USERANIMELIST_FILE = PLAIN_DIR + "UserAnimeList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserAnimeList.csv
USERLIST_FILE = PLAIN_DIR + "UserList.csv" # https://www.kaggle.com/azathoth42/myanimelist/version/9?select=UserList.csv

NOW = datetime.utcnow()
