import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema
import pandas as pd

data_path = 'data/raw/games.csv'

#Load variables from .env file
load_dotenv()
DB_USERNAME =  os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

with engine.connect() as con:
    res = con.execute(text("SELECT version();"))
    print(res.fetchone())

df = pd.read_csv(data_path)

print("creating bronze schema")
with engine.begin() as con:
    con.execute(CreateSchema("bronze", if_not_exists=True))

print("importing data to database")
df.to_sql("games", engine, schema="bronze", if_exists="replace", index=False)

with engine.connect() as con:
    count = con.execute(text("SELECT COUNT(*) FROM bronze.games;")).scalar()
    print("number of rows: ", count)

with engine.connect() as con:
    sample = con.execute(text("SELECT * FROM bronze.games LIMIT 2;")).fetchall()
    print("\nsample data: ", sample)