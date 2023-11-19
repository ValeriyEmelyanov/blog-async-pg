import databases

DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "blog_async"
DB_HOST = "localhost"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

database = databases.Database(SQLALCHEMY_DATABASE_URL)
