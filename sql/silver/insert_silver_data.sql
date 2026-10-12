TRUNCATE silver.games;

INSERT INTO silver.games
SELECT
    DISTINCT ON (id)
    id,
    rated,
    TO_TIMESTAMP(created_at / 1000) AS created_at,
    TO_TIMESTAMP(last_move_at / 1000) AS last_move_at,
    turns,
    victory_status,
    winner,
    increment_code,
    white_id,
    white_rating,
    black_id,
    black_rating,
    moves,
    opening_eco,
    opening_name,
    opening_ply
FROM bronze.games
WHERE 
    NOT (winner = 'draw' AND victory_status != 'draw')
    AND created_at != last_move_at
ORDER BY id, last_move_at DESC;