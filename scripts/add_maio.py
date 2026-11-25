import pandas as pd
df=pd.read_pickle('all.pkl')
m=pd.read_excel('data_mai/maio.xlsx',sheet_name=0)
m.columns=[str(c).strip() for c in m.columns]
m['VALOR']=pd.to_numeric(m['VL REPASSE'],errors='coerce')
m['ARQ']='Maio_2026_Valores_Revisados.xlsx'
print(len(m), m.VALOR.sum(), m['DT PEDIDO'].min(), m['DT PEDIDO'].max(), m.TIPO.value_counts().to_dict())
print(m[m['ATEND.'].isna()|m.PACIENTE.isna()].VALOR.sum())
k=['PEDIDO','CD EXAME','CD PROCED','SAME']
mk=set(map(tuple,m[k].dropna().values)); 
ov=df[df[k].apply(tuple,axis=1).isin(mk)]
print('linhas de outros arquivos com mesma chave:',len(ov), ov.ARQ.value_counts().to_dict())
al=pd.concat([df,m],ignore_index=True)
al.to_pickle('all.pkl')
