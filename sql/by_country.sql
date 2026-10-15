SELECT countryCode, COUNT(*) AS occurrence_records
FROM records
GROUP BY countryCode
ORDER BY occurrence_records DESC;

