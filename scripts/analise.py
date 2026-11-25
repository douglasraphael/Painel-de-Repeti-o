import pandas as pd, numpy as np, json
df=pd.read_pickle('all.pkl')
df=df[df['ATEND.'].notna()&df.PACIENTE.notna()]
e=df[df.TIPO.isin(['EXTERNO','AMBULATORIO'])&(df.STATUS!='PEDIDO EXCLUIDO')&df['DT PEDIDO'].notna()].copy()
e['DATA']=pd.to_datetime(e['DT PEDIDO']).dt.normalize()
e=e[e.DATA>='2026-01-01']
ev=(e.groupby(['SAME','CD EXAME','PEDIDO'],as_index=False)
     .agg(DATA=('DATA','min'),VALOR=('VALOR','sum'),EXAME=('EXAME','first'),SETOR=('SETOR SOLICITANTE','first'),
          MED=('PRESTADOR SOLICITANTE','first'),TIPO=('TIPO','first')))
ev=ev.sort_values(['SAME','CD EXAME','DATA','PEDIDO'])
g=ev.groupby(['SAME','CD EXAME'])
ev['GAP']=(ev.DATA-g.DATA.shift()).dt.days
ev['MED_ANT']=g.MED.shift()
ev['MESMO_MED']=np.where(ev.GAP.notna(), np.where(ev.MED==ev.MED_ANT,'Mesmo médico','Outro médico'),None)
ev['MES']=ev.DATA.dt.strftime('%Y-%m')
# nome exame canônico por código (mais frequente)
nome=ev.groupby('CD EXAME').EXAME.agg(lambda s:s.value_counts().index[0])
ev['EXAME']=ev['CD EXAME'].map(nome)
ev.to_pickle('eventos.pkl')
print(len(e),e.VALOR.sum(),len(ev),ev.VALOR.sum(),ev.SAME.nunique())
for w in [0,7,15,30,60,90]:
    r=ev[ev.GAP<=w]
    print(w,len(r),round(r.VALOR.sum(),2),r.SAME.nunique(), r.groupby('MESMO_MED').VALOR.sum().round(0).to_dict())
print(ev[ev.GAP<=30].groupby('EXAME').agg(n=('VALOR','size'),v=('VALOR','sum')).sort_values('v',ascending=False).head(25))
print(ev.groupby('MES').VALOR.agg(['size','sum']))
