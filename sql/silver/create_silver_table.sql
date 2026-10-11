CREATE SCHEMA IF NOT EXISTS silver;

CREATE TABLE IF NOT EXISTS silver.games (
    id VARCHAR PRIMARY KEY,
    rated BOOLEAN,
    created_at DOUBLE PRECISION,
    last_move_at DOUBLE PRECISION,
    turns INTEGER,
    victory_status TEXT,
    winner TEXT,
    increment_code TEXT,
    white_id TEXT,
    white_rating INTEGER,
    black_id TEXT,
    black_rating INTEGER,
    moves TEXT,
    opening_eco TEXT,
    opening_name TEXT,
    opening_ply INTEGER
);