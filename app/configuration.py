import os


class Configuration:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:root@{os.environ["DB_URL"]}/app'
    JWT_SECRET_KEY = "uuyfu56r67F65FUYFT78"
    REDIS_HOST = 'redis'
