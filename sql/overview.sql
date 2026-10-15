-- Counts are occurrence records, not individual organisms or deduplicated sightings.
SELECT speciesKey, species, COUNT(*) AS occurrence_records,
       COUNT(DISTINCT countryCode) AS country_codes,
       MIN(TRY_CAST(year AS INTEGER)) AS earliest_year,
       MAX(TRY_CAST(year AS INTEGER)) AS latest_year,
       COUNT(*) FILTER (WHERE year IS NOT NULL AND TRY_CAST(year AS INTEGER) IS NULL)
           AS invalid_year_values
FROM records
GROUP BY speciesKey, species
ORDER BY occurrence_records DESC;

