from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema
import psycopg2
import pandas as pd

data_path = 'data/raw/games.csv'

USERNAME = "postgres"
PASSWORD = "admin"
HOST = "localhost"
PORT = "5432"
DB_NAME = "lichess_analisys_db"

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

with engine.connect() as con:
    res = con.execute(text("SELECT version();"))
    print(res.fetchone())

df = pd.read_csv(data_path)

with engine.begin() as con:
    con.execute(CreateSchema("bronze", if_not_exists=True))


df.to_sql("raw_games", engine, schema="bronze", if_exists="replace", index=False)

with engine.connect() as con:
    count = con.execute(text("SELECT COUNT(*) FROM bronze.raw_games;")).scalar()
    print("number of rows: ", count)

with engine.connect() as con:
    sample = con.execute(text("SELECT * FROM bronze.raw_games LIMIT 2;")).fetchall()
    print("\nsample data: ", sample)