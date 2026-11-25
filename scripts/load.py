import pandas as pd,glob,re
frames=[]
for f in sorted(glob.glob('data/*.xlsx')):
    d=pd.read_excel(f,sheet_name=0)
    d.columns=[str(c).strip() for c in d.columns]
    corr=[c for c in d.columns if c in('VALOR ATT','VL CORRIGIDO','VALOR CORRIGIDO','VALOR REAL')]
    d['VALOR']=d[corr[0]] if corr else d['VL REPASSE']
    d['VALOR']=pd.to_numeric(d['VALOR'],errors='coerce').fillna(pd.to_numeric(d['VL REPASSE'],errors='coerce'))
    d['ARQ']=f.split('/')[-1]
    frames.append(d)
df=pd.concat(frames,ignore_index=True)
df.to_pickle('all.pkl')
