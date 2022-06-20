import os
from datetime import timedelta


class Configuration:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:root@{os.environ["DB_URL"]}/auth'
    JWT_SECRET_KEY = "uuyfu56r67F65FUYFT78"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)