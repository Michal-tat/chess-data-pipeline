DROP TABLE IF EXISTS gold.opening_statistics;

CREATE TABLE gold.opening_statistics AS SELECT
	opening_name,
	COUNT(*) AS games_count,
	COUNT(CASE WHEN winner = 'black' THEN 1 END) AS black_wins,
	COUNT(CASE WHEN winner = 'white' THEN 1 END) AS white_wins,
	COUNT(CASE WHEN winner = 'draw' THEN 1 END) AS draws,
	ROUND(AVG(turns), 0) AS avg_turns,
	ROUND(AVG(white_rating), 0) AS avg_white_rating,
	ROUND(AVG(black_rating), 0) AS avg_black_rating
FROM silver.games
GROUP BY opening_name
ORDER BY games_count DESC;