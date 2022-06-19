import os


class Configuration:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:root@{os.environ["DB_URL"]}/users'
