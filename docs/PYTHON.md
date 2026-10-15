# Optional Python and SQL tools

Python is not required for Power BI. These tools are for people who want to write queries.

Install Python 3.10 or newer. In a terminal in this project's folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe analyze.py
.\.venv\Scripts\python.exe analyze.py --sql sql/by_year.sql
.\.venv\Scripts\python.exe analyze.py --sql sql/preview.sql
.\.venv\Scripts\python.exe analyze.py --sql sql/by_year.sql --output outputs/my_yearly_counts.csv
```

On macOS/Linux, use `.venv/bin/python` instead of `.\.venv\Scripts\python.exe`.

The `records` SQL view reads the included Parquet file. Edit the SQL examples or add your own.
Console output is limited to 100 rows. CSV export includes all results and refuses to overwrite files.
To use another dataset, pass `--data "path/to/file.parquet"`.

Source columns are text. `TRY_CAST` turns invalid numeric text into null. The overview reports invalid year values. Queries use up to two threads and a 2 GB DuckDB memory budget.
