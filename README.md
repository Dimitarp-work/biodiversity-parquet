# Biodiversity Parquet starter

Analyze the Alcedo atthis (common kingfisher) occurrence dataset with Python, SQL, or Power BI.

## Data

The existing file is `V:\Alcedo_atthis.parquet`: 429,646 records, 50 columns, species key `2475532`.
It was extracted from `E:\DS AI\0046453-260226173443078.csv` on 2026-10-15.
The source is tab-separated despite its extension. All Parquet columns are strings, with empty fields represented as null.
Counts describe source occurrence records, not individual organisms or independently verified sightings. No deduplication or quality filtering has been applied.
Keep the per-record `license`, `rightsHolder`, and source identifiers when sharing derived data.

Data stays outside this Git repository. Parquet files, environments, generated outputs, and Power BI binaries are ignored.

## Run now on this computer

A local Python environment has been prepared. In PowerShell:

```powershell
cd V:\biodiversity-parquet
.\.venv\Scripts\python.exe analyze.py
.\.venv\Scripts\python.exe analyze.py --sql sql/by_year.sql
.\.venv\Scripts\python.exe analyze.py --sql sql/by_country.sql
.\.venv\Scripts\python.exe analyze.py --sql sql/preview.sql
.\.venv\Scripts\python.exe analyze.py --sql sql/by_year.sql --output outputs/by_year.csv
```

No environment activation is required. Output commands refuse to overwrite existing files.
Edit or add SQL files: the `records` view refers to the Parquet file. Console results are capped at 100 rows; CSV export streams all result rows.
`TRY_CAST` in the examples turns invalid numbers into null. The overview reports invalid year values.

To use another file:

```powershell
.\.venv\Scripts\python.exe analyze.py --data "V:\another_species.parquet"
```

## Set up on another computer

Install Python 3.10 or newer, clone/copy the repository, and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy the Parquet file separately and pass its location with `--data`, or place it in the repository's parent folder.

## Open in Power BI Desktop

1. Select **Home > Get data > More**, search for **Parquet**, and select **Connect**.
2. Enter `V:\Alcedo_atthis.parquet`, then choose **Transform Data**.
3. Set `decimalLatitude` and `decimalLongitude` to **Decimal number**, using **English (United States)** locale because source decimals use a dot. Set `year`, `month`, and `day` to **Whole number**. Leave identifiers such as `gbifID` and `speciesKey` as text.
4. Choose **Close & Apply**. Set the coordinate columns' data categories to **Latitude** and **Longitude** and their summarization to **Don't summarize**.

Alternatively, use **Get data > Blank query > Advanced Editor** and paste `powerbi/Alcedo_atthis.pq`. Rename the query to `Alcedo_atthis`, then Close & Apply. This includes the numeric conversions. Review any conversion errors rather than removing those rows blindly.

Keep `eventDate` as text initially: biodiversity dates may contain partial dates or date ranges.

Create a measure after naming the table `Alcedo_atthis`:

```dax
Sightings = COUNTROWS('Alcedo_atthis')
```

Start with a card showing `Sightings`, a column chart with `year` on the axis and `Sightings` as its value, and a bar chart by `countryCode`. These are record counts, not population estimates.

Power BI Service refresh of a local file requires an appropriate gateway and access to the same file location. A drive mapping visible only in your desktop session may not be visible to the gateway.

Microsoft connector documentation: https://learn.microsoft.com/en-us/power-query/connectors/parquet

## Git

This is a local repository on branch `main`. No GitHub remote is configured.
Use `git status`, `git diff`, and `git add` / `git commit` to track code changes.
Do not commit the source CSV or datasets. The original source and exported Parquet remain unchanged.
