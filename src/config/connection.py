class Connection:
    hostname = "localhost"
    port = "5432"
    username = "root"
    password = "root"
    database_name = "pdt"


db_string = f'postgresql://{Connection.username}:{Connection.password}@{Connection.hostname}:{Connection.port}/{Connection.database_name}'
