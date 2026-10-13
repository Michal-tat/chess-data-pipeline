import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema
import pandas as pd

data_path = 'data/raw/games.csv'
data_quality_checks_query = 'sql/checks/data_quality_checks.sql'
create_silver_table_query = 'sql/silver/create_silver_table.sql'
insert_silver_data_query = 'sql/silver/insert_silver_data.sql'
opening_statistics_query = 'sql/gold/opening_statistics.sql'
result_statistics_query = 'sql/gold/result_statistics.sql'
time_control_statistics_query = 'sql/gold/time_control_statistics.sql'

#Load variables from .env file
load_dotenv()
DB_USERNAME =  os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

print("Creating engine... ", end="")
engine = create_engine(f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
print("engine created succesfully\n")

def validate(engine, schema, table):
    t = f"{schema}.{table}"
    with engine.begin() as con:
        rows = con.execute(text(f"SELECT COUNT(*) FROM {t};")).scalar()
        unique_ids = con.execute(text(f"SELECT COUNT(DISTINCT(id)) FROM {t}")).scalar()
        draws_with_winner = con.execute(text(f"SELECT COUNT(*) FROM {t} WHERE winner = 'draw' AND victory_status != 'draw';")).scalar()
        time_anomaly = con.execute(text(f"SELECT COUNT(*) FROM {t} WHERE created_at = last_move_at;")).scalar()
        nulls = con.execute(text(f"SELECT COALESCE(SUM(num_nulls(x.*)), 0) FROM {t} x")).scalar()
    print(f"{schema} table data quality checks:\nrows: {rows}\nunique id's: {unique_ids}\nduplicated id's: {rows-unique_ids}\nrows with draw and winner: {draws_with_winner}\nstart of game same time as last move: {time_anomaly}\nnull values: {nulls}\n")

validate(engine, "bronze", "games")

print("Creating silver schema and silver.games table... ", end="")

with engine.begin() as con:
    with open(create_silver_table_query) as file:
        query = text(file.read())
        con.execute(query)

print("Silver schema and table created succesfully\n")

print("Loading data to silver.games table... ", end="")
with engine.begin() as con:
    with open(insert_silver_data_query) as file:
        query = text(file.read())
        con.execute(query)

print("succesfully loaded data to silver.games table\n")

validate(engine, "silver", "games")

print("Creating gold schema...", end="")
with engine.begin() as con:
    con.execute(CreateSchema("gold", if_not_exists=True))
print("Gold schema created succesfully\n")

print("Creating 3 tables for gold schema\n")

with engine.begin() as con:
    with open(opening_statistics_query) as file:
        query = text(file.read())
        con.execute(query)

with engine.begin() as con:
    with open(result_statistics_query) as file:
        query = text(file.read())
        con.execute(query)

with engine.begin() as con:
    with open(time_control_statistics_query) as file:
        query = text(file.read())
        con.execute(query)

print("Success!!")














