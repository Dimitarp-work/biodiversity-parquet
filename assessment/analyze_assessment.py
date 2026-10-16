"""Reproduce the full-dataset assessment tables and figures. No source edits."""
from pathlib import Path
import csv, json, hashlib
import duckdb
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assessment'/'results'
OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'data'/'Alcedo_atthis.parquet'
c=duckdb.connect()
c.execute("SET memory_limit='2GB'")
c.execute('SET threads=2')
c.read_parquet(str(SOURCE)).create_view('d')
cols=[x[0] for x in c.execute('describe d').fetchall()]
n=c.execute('select count(*) from d').fetchone()[0]
numeric=['individualCount','decimalLatitude','decimalLongitude','coordinateUncertaintyInMeters','coordinatePrecision','elevation','elevationAccuracy','depth','depthAccuracy','day','month','year']
freq=[]
for col in cols:
    q='"'+col+'"'
    nulls=c.execute(f'select count(*) from d where {q} is null').fetchone()[0]
    groups=c.execute(f'select {q},count(*) n from d where {q} is not null group by 1 order by n,{q}').fetchall()
    if groups:
        low=groups[0][1]; high=groups[-1][1]
        least=min(v for v,k in groups if k==low); most=min(v for v,k in groups if k==high)
        freq.append(dict(variable=col,missing=nulls,unique=len(groups),least_value=least,least_count=low,least_ties=sum(k==low for v,k in groups),most_value=most,most_count=high,most_ties=sum(k==high for v,k in groups)))
    else: freq.append(dict(variable=col,missing=nulls,unique=0,least_value='',least_count=0,least_ties=0,most_value='',most_count=0,most_ties=0))

summaries=[]; arrays={}
for col in numeric:
    a=np.array([r[0] for r in c.execute(f'SELECT TRY_CAST("{col}" AS DOUBLE) FROM d').fetchall()],dtype=float)
    arrays[col]=a
    b=a[np.isfinite(a)]
    missing=next(r['missing'] for r in freq if r['variable']==col)
    row=dict(variable=col,n=int(len(b)),missing=missing,invalid=int(n-missing-len(b)))
    if len(b):
        q=np.quantile(b,[.25,.5,.75,1],method='linear'); iqr=q[2]-q[0]
        row.update(min=float(b.min()),max=float(b.max()),median=float(q[1]),mean=float(b.mean()),q1=float(q[0]),q3=float(q[2]),iqr=float(iqr),std=float(b.std(ddof=1)),skew=float(stats.skew(b,bias=False)),lower_fence=float(q[0]-1.5*iqr),upper_fence=float(q[2]+1.5*iqr),outliers=int(((b<q[0]-1.5*iqr)|(b>q[2]+1.5*iqr)).sum()))
    summaries.append(row)

def export(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
export('frequencies.csv',freq)
fields=list(dict.fromkeys(k for r in summaries for k in r))
export('numeric_summary.csv',[{k:r.get(k) for k in fields} for r in summaries])


result={'rows':n,'columns':len(cols),'cells':n*len(cols),'missing':sum(r['missing'] for r in freq),'duplicates':n-c.execute('select count(*) from (select distinct * from d)').fetchone()[0],'duplicate_gbifID':n-c.execute('select count(distinct gbifID) from d').fetchone()[0],'dataset_count':c.execute('select count(distinct datasetKey) from d').fetchone()[0],'licenses':c.execute('select license,count(*) from d group by 1 order by 2 desc').fetchall(),'datasets':c.execute('select datasetKey,count(*) from d group by 1 order by 2 desc').fetchall(),'frequencies':freq,'numeric_summary':summaries,'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
(OUT/'assessment_results.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
assert n==429646 and result['columns']==50 and result['missing']==7265072
print(json.dumps({k:v for k,v in result.items() if k not in ['frequencies','datasets']},indent=2))
