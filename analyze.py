"""Query Parquet directly without loading the whole dataset into Python."""
import argparse
import csv
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT.parent / 'Alcedo_atthis.parquet')
    parser.add_argument('--sql', type=Path, default=ROOT / 'sql' / 'overview.sql')
    parser.add_argument('--output', type=Path, help='Optional CSV result file; refuses to overwrite')
    args = parser.parse_args()
    if not args.data.is_file():
        parser.error(f'Data file not found: {args.data}')
    if args.output and args.output.exists():
        parser.error(f'Output already exists: {args.output}')
    with duckdb.connect() as con:
        con.execute("SET memory_limit = '2GB'")
        con.execute('SET threads = 2')
        con.read_parquet(str(args.data)).create_view('records')
        result = con.execute(args.sql.read_text(encoding='utf-8-sig'))
        headers = [column[0] for column in result.description]
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x', newline='', encoding='utf-8-sig') as handle:
                writer = csv.writer(handle)
                writer.writerow(headers)
                while batch := result.fetchmany(10000):
                    writer.writerows(batch)
            print(f'Saved {args.output.resolve()}')
        else:
            rows = result.fetchmany(101)
            print('\t'.join(headers))
            for row in rows[:100]:
                print('\t'.join('NULL' if item is None else str(item) for item in row))
            if len(rows) > 100:
                print('Showing first 100 rows. Use --output to export all results.')

if __name__ == '__main__':
    main()

