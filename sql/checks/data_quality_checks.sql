SELECT DISTINCT winner FROM bronze.games;
SELECT DISTINCT victory_status FROM bronze.games;
SELECT DISTINCT increment_code FROM bronze.games;

SELECT
	MIN(turns) as min_turns,
	MAX(turns) as max_turns,
	MIN(white_rating) as min_white,
	MAX(white_rating) as max_white,
	MIN(black_rating) as min_black,
	MAX(black_rating) as max_black
FROM bronze.games;

/* * */
SELECT COUNT(*) FROM bronze.games WHERE winner = 'draw' AND victory_status != 'draw';

SELECT 
	COUNT(*)
FROM bronze.games
WHERE turns != CARDINALITY(STRING_TO_ARRAY(moves, ' '));

/* * */
SELECT COUNT(*) FROM bronze.games WHERE created_at = last_move_at;

/* * */
SELECT DISTINCT(opening_name) FROM bronze.games ORDER BY opening_name;