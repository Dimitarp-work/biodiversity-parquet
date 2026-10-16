from pathlib import Path
import duckdb,numpy as np,json,csv,calendar
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]; O=R/'assessment/results';c=duckdb.connect()
c.read_parquet(str(R/'data/Alcedo_atthis.parquet')).create_view('d')
rows=c.execute("select try_cast(year as integer) y,try_cast(month as integer) m,count(*) n from d group by 1,2 order by 1,2").fetchall()
valid={(y,m):n for y,m,n in rows if y is not None and 2010<=y<=2025 and m is not None and 1<=m<=12}
excluded=sum(n for y,m,n in rows if (y,m) not in valid)
monthly=[dict(year=y,month=m,year_month=f'{y}-{m:02}',time_index=(y-2010)*12+m-1,sighting_count=valid.get((y,m),0),month_sin=float(np.sin(2*np.pi*m/12)),month_cos=float(np.cos(2*np.pi*m/12))) for y in range(2010,2026) for m in range(1,13)]
a=np.array([r['sighting_count'] for r in monthly]);q=np.quantile(a,[.25,.5,.75]);iqr=q[2]-q[0];lo=q[0]-1.5*iqr;hi=q[2]+1.5*iqr
corr=[]
for col in ['time_index','year','month_sin','month_cos']:
 x=np.array([r[col] for r in monthly]);corr.append(dict(variable=col,reference='sighting_count',n=192,pearson=float(np.corrcoef(x,a)[0,1]),spearman=float(stats.spearmanr(x,a).statistic)))
annual=[dict(year=y,sighting_count=sum(n for yy,m,n in rows if yy==y),unknown_month_count=sum(n for yy,m,n in rows if yy==y and (m is None or not 1<=m<=12))) for y in range(2010,2026)]
def write(name,data):
 with (O/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
write('monthly_sightings.csv',monthly);write('annual_sightings.csv',annual);write('sighting_correlations.csv',corr)
s=dict(source_rows=sum(n for y,m,n in rows),included=int(a.sum()),excluded_unknown_month=excluded,months=len(a),zero_months=int((a==0).sum()),min=int(a.min()),max=int(a.max()),mean=float(a.mean()),median=float(q[1]),q1=float(q[0]),q3=float(q[2]),iqr=float(iqr),std=float(a.std(ddof=1)),skew=float(stats.skew(a,bias=False)),lower_fence=float(lo),upper_fence=float(hi),outliers=[r for r in monthly if r['sighting_count']<lo or r['sighting_count']>hi],min_months=[r['year_month'] for r in monthly if r['sighting_count']==a.min()],max_months=[r['year_month'] for r in monthly if r['sighting_count']==a.max()],covariance_time_count=float(np.cov(np.arange(192),a,ddof=1)[0,1]),correlations=corr,annual=annual)
(O/'sightings_summary.json').write_text(json.dumps(s,indent=2))
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,4.2),layout='constrained');ax.hist(a,bins=16,color='#19789a',edgecolor='white');ax.set(xlabel='Recorded sightings per calendar month',ylabel='Number of months',title='Distribution of kingfisher sighting counts | 192 months');fig.savefig(O/'sightings_distribution.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,3),layout='constrained');ax.boxplot(a,orientation='horizontal',whis=1.5);ax.set(xlabel='Recorded sightings per calendar month',yticks=[],title='Monthly kingfisher sightings | 1.5 × IQR box plot');fig.savefig(O/'sightings_boxplot.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,4.2),layout='constrained');ax.plot(np.arange(192),a,color='#19789a',lw=1.4);ax.set(xticks=np.arange(0,192,24),xticklabels=[str(y) for y in range(2010,2026,2)],xlabel='Observation year (monthly points)',ylabel='Recorded sightings per month',title='Kingfisher sightings over time | 2010–2025');fig.savefig(O/'sightings_over_time.png',dpi=180);plt.close(fig)
assert s['included']+excluded==429646 and len(a)==192
print(json.dumps(s,indent=2))

