# Verified assessment work

Run `pip install -r assessment/requirements.txt`, then `python assessment/analyze_assessment.py` from the repository root.

The script reads all 429,646 rows without modifying the source. Results include per-column null counts, distinct values, frequency representatives and tie counts; numeric summaries; exploratory coordinate correlations; and figures. Source SHA-256 is recorded in the results JSON.

NULLs are excluded from distinct values, frequencies and numeric calculations. Frequency ties use the lexicographically first value. Numeric parsing uses TRY_CAST and invalid counts are reported. Quantiles use linear interpolation, standard deviation/covariance use n−1, and box plot flags use strict 1.5×IQR fences. Pairwise-valid Pearson/Spearman correlations use decimalLatitude as an exploratory reference, not a selected model target. No deduplication, imputation, filtering or model fitting was performed.

The original GBIF download is https://doi.org/10.15468/dl.5kx93n, created 18 March 2026. Its API metadata confirms 104,965,065 original rows and filters for NL, HUMAN_OBSERVATION, PRESENT and 2010–2025. The species extract filters speciesKey 2475532.

The Google assessment is an in-progress working document: https://docs.google.com/document/d/1qa4yUP-Jt3bYsOItCxeLUsv9dTvqXczX0e2MH0tH-_g/edit

Outstanding group work: agree the project question and roles, target and final predictor set, validation and success criteria, and review the complete submission. No accuracy or population-level claims have been invented.
