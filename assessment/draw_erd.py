from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

out=Path(__file__).parent/'results'/'entity_relationships.png'
fig,ax=plt.subplots(figsize=(9,6.8),layout='constrained')
ax.set(xlim=(0,10),ylim=(0,8));ax.axis('off')
nodes={'publisher':(1.6,7,'Publisher\npublishingOrgKey'),'dataset':(5,7,'Dataset\ndatasetKey'),'taxon':(8.4,4.8,'Taxon\ntaxonKey / speciesKey'),'record':(5,4.8,'Occurrence record\ngbifID / occurrenceID'),'observer':(1.6,2.6,'Observer / identifier\nrecordedBy / identifiedBy'),'event':(5,2.6,'Observation event\neventDate / individualCount'),'location':(8.4,2.6,'Location\nlatitude / longitude'),'media':(1.6,4.8,'Media reference\nmediaType')}
for key,(x,y,label) in nodes.items():
    ax.add_patch(FancyBboxPatch((x-1.35,y-.46),2.7,.92,boxstyle='round,pad=0.03',facecolor='#eef4f7',edgecolor='#355b70',linewidth=1.3))
    ax.text(x,y,label,ha='center',va='center',fontsize=10)
def arrow(x1,y1,x2,y2,label,tx,ty):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops={'arrowstyle':'->','color':'#355b70','lw':1.5})
    ax.text(tx,ty,label,ha='center',va='center',fontsize=9,bbox={'facecolor':'white','edgecolor':'none','pad':1})
arrow(2.98,7,3.62,7,'publishes',3.3,7.45)
arrow(5,6.5,5,5.3,'contains records',5.9,5.9)
arrow(6.38,4.8,7.02,4.8,'identifies',6.7,5.2)
arrow(3.62,4.8,2.98,4.8,'links to',3.3,5.2)
arrow(5,4.3,5,3.1,'describes',5.65,3.7)
arrow(2.98,2.6,3.62,2.6,'records',3.3,3)
arrow(6.38,2.6,7.02,2.6,'occurs at',6.7,3)
ax.text(5,1.35,'Conceptual associations, not a proven causal graph',ha='center',fontsize=12,fontweight='bold')
ax.text(5,.7,'A dataset contains many records. A record refers to one interpreted taxon and location.\nEvent and person identifiers are not consistently normalised; names alone are not unique keys.',ha='center',fontsize=10)
fig.savefig(out,dpi=180);plt.close(fig)
