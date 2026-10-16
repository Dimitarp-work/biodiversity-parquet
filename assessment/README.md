# Kingfisher sighting-count assessment

The primary question is: how do recorded kingfisher sightings vary over months and years from 2010–2025?

Run from the repository root:
1. pip install -r assessment/requirements.txt
2. python assessment/analyze_assessment.py
3. python assessment/analyze_sightings.py

The first script audits the original 429,646 records and 50 columns. The second builds monthly_sightings.csv and annual_sightings.csv, produces the sighting-count distribution, box plot and time-series chart, and calculates correlations against sighting_count. No external dataset is used.

Each monthly count is COUNT(*) for a year/month; it is not SUM(individualCount) or a unique-bird count. There are 429,619 records with valid months and 27 unknown-month records. All 192 calendar months are represented and have positive counts. Annual totals include all 429,646 records.

Monthly count summary: minimum 209, maximum 6,296, mean 2,237.60, median 1,979.50, Q1 998.25, Q3 3,146.50, IQR 2,148.25, sample SD 1,465.09. No month falls outside the strict 1.5×IQR fences. Quantiles use linear interpolation; SD/covariance use n−1.

Correlations use 192 monthly rows: time_index, year and cyclic month sine/cosine against sighting_count. Record-level coordinates are retained in the source dictionary and basic summaries but are not the response for this analysis. Correlation is descriptive; no causal effect, population growth or predictive accuracy is asserted.

The source Parquet remains unchanged. Full source missingness, frequencies and numeric summaries remain available. NULLs are excluded from source summary calculations; frequency ties use the lexicographically first tied value.

[Working Google assessment](https://docs.google.com/document/d/1qa4yUP-Jt3bYsOItCxeLUsv9dTvqXczX0e2MH0tH-_g/edit)
[Original GBIF download](https://doi.org/10.15468/dl.5kx93n)

The unrelated loan examples have been removed from the working document. The original blank Word template is preserved as a historical source template. Group roles and final review remain open.
