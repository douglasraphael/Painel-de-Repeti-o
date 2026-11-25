import pandas as pd, numpy as np, json, re
df=pd.read_pickle('all.pkl')
u=df[df.TIPO.isin(['URGENCIA','INTERNACAO'])&df['ATEND.'].notna()&df.PACIENTE.notna()&(df.STATUS!='PEDIDO EXCLUIDO')&df['DT PEDIDO'].notna()].copy()
d=pd.to_datetime(u['DT PEDIDO']).dt.normalize()
h=u['HR_PEDIDO'].astype(str).str.extract(r'(\d{1,2}):(\d{2})').astype(float).fillna(0)
u['DTH']=d+pd.to_timedelta(h[0],unit='h')+pd.to_timedelta(h[1],unit='m')
u=u[(d>='2026-01-01')&(d<='2026-10-31')]
print(len(u), u.VALOR.sum(), u.TIPO.value_counts().to_dict())
ev=(u.groupby(['SAME','CD EXAME','PEDIDO'],as_index=False).agg(DTH=('DTH','min'),VALOR=('VALOR','sum'),EXAME=('EXAME','first'),
     TIPO=('TIPO','first'),SETOR=('SETOR SOLICITANTE','first'),MED=('PRESTADOR SOLICITANTE','first'),ATEND=('ATEND.','first')))
ev=ev.sort_values(['SAME','CD EXAME','DTH','PEDIDO'])
g=ev.groupby(['SAME','CD EXAME'])
ev['GAPH']=(ev.DTH-g.DTH.shift()).dt.total_seconds()/3600
norm=lambda s:' '.join(str(s).upper().split())
ev['MEDN']=ev.MED.map(norm); ev['PROPRIO']=ev.GAPH.notna()&(ev.MEDN==g.MEDN.shift())
nome=ev.groupby('CD EXAME').EXAME.agg(lambda s:s.value_counts().index[0]); ev['EXAME']=ev['CD EXAME'].map(nome).str.strip()
ev.to_pickle('ev_urg.pkl')
print(len(ev), ev.VALOR.sum(), ev.SAME.nunique())
for lim in [6,12,24,48,72,168]:
    r=ev[ev.GAPH<=lim]; print(lim,len(r),round(r.VALOR.sum()),r.SAME.nunique(), r.groupby('TIPO').VALOR.sum().round().to_dict())
print(ev[ev.GAPH<=24].groupby('EXAME').VALOR.agg(['size','sum']).sort_values('sum',ascending=False).head(12))
print(ev[ev.GAPH<=24].groupby('SETOR').VALOR.agg(['size','sum']).sort_values('sum',ascending=False).head(10))
