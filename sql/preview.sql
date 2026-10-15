SELECT gbifID, species, countryCode, eventDate,
       TRY_CAST(decimalLatitude AS DOUBLE) AS latitude,
       TRY_CAST(decimalLongitude AS DOUBLE) AS longitude,
       basisOfRecord
FROM records
LIMIT 20;

