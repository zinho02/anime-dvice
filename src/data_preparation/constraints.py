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

# CLEANED_DIR
CLEANED_ANIMELIST_FILE = os.path.join(CLEANED_DIR, "AnimeListCleaned.csv")
CLEANED_USERANIMELIST_FILE = os.path.join(CLEANED_DIR, "UserAnimeListCleaned.csv")
CLEANED_USERLIST_FILE = os.path.join(CLEANED_DIR, "UserListCleaned.csv")


# AUXILIARY_DIR
ANIMELIST_TYPE_FILE = os.path.join(AUXILIAR_DIR, "animelist_type.csv")
ANIMELIST_STATUS_FILE = os.path.join(AUXILIAR_DIR, "animelist_status.csv")
ANIMELIST_RATING_FILE = os.path.join(AUXILIAR_DIR, "animelist_rating.csv")
ANIMELIST_RELATED_FILE = os.path.join(AUXILIAR_DIR, "animelist_related.csv")
ANIMELIST_GENRE_FILE = os.path.join(AUXILIAR_DIR, "animelist_genre.csv")

NOW = datetime.utcnow()
