-- Retain unknown/invalid years as a NULL group.
SELECT TRY_CAST(year AS INTEGER) AS year, COUNT(*) AS occurrence_records
FROM records
GROUP BY 1
ORDER BY 1 NULLS LAST;

