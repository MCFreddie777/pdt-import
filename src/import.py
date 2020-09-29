from pathlib import Path
import jsonlines
from base import Session
from helpers.parser import parse_object
from models.country import Country
from models.account import Account
from models.hashtag import Hashtag
from models.tweet import Tweet

session = Session()

# load all .jsonl files from data folder
file_ext = '.jsonl'
data_dir = Path('data')
files = (entry for entry in data_dir.iterdir() if entry.is_file() and entry.name.endswith(file_ext))

for file in files:
    # parse each json line of the file
    with jsonlines.open(file) as reader:
        for obj in reader:
            parse_object(obj)
            # save all data

session.commit()
session.close()
