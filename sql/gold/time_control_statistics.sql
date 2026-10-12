DROP TABLE IF EXISTS gold.time_control_statistics;

CREATE TABLE gold.time_control_statistics AS SELECT 
	increment_code, 
	COUNT(*) AS game_count, 
	ROUND(AVG(turns), 0) AS average_turns, 
	COUNT(CASE WHEN victory_status = 'mate' THEN 1 END) as mates_count,
	COUNT(CASE WHEN victory_status = 'draw' THEN 1 END) as draw_count,
	COUNT(CASE WHEN victory_status = 'resign' THEN 1 END) as resignations_count,
	COUNT(CASE WHEN victory_status = 'outoftime' THEN 1 END) as timeouts_count
FROM silver.games
GROUP BY increment_code
ORDER BY game_count DESC;