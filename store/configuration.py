import os


class Configuration:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:root@{os.environ["DB_URL"]}/store'
    JWT_SECRET_KEY = "uuyfu56r67F65FUYFT78"
    REDIS_HOST = 'store-redis'
    REDIS_LIST = 'NEW_PRODUCT'
