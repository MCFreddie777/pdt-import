# [PDT] Import

This project imports large data dump of twitter tweets


### Data
from https://drive.google.com/drive/folders/1erM4udXKUDRuhzX6n0WeXTb-G87xbIHf 

### Prerequisites

- Python > 3.4
- [Pip](https://packaging.python.org/tutorials/installing-packages/)

```bash
pip install jsonlines sqlalchemy geoalchemy
```

### Usage

All data should be unarchived into the data folder in project root first.

Then, you need to configure your database connection info in `config/connection.py`

```
# config/connection.py

hostname = "localhost"
port = "5432"
username = "root"
password = "secret"
database_name = "db"
```

Then run `run.sh`.

e.g.
```bash
. ./run.sh
```

This shell script runs both migration and and import.
If you only wish to run one of it you might run:

```bash
python src/migrate.py
```

or 

```bash
python src/script.py
```  


