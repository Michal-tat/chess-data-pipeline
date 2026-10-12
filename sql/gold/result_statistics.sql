DROP TABLE IF EXISTS gold.result_statistics;

CREATE TABLE gold.result_statistics AS SELECT
	winner,
	COUNT(*) AS games_count,
	ROUND(AVG(turns), 0) as avg_turns,
	ROUND(AVG(white_rating), 0) AS avg_white_rating,
	ROUND(AVG(black_rating), 0) AS avg_black_rating
FROM silver.games
GROUP BY winner;
