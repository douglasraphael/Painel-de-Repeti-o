import pandas as pd, json, re
ev=pd.read_pickle('ev_urg.pkl')
def area(r):
    s=str(r.SETOR).upper()
    if re.search(r'\bCTI\b|\bUTI\b|\bUCI\b|TERAPIA INTENSIVA|CUIDADOS INTERMEDI',s): return 'CTI / UCI'
    if r.TIPO=='URGENCIA' or re.search(r'\bPS\b|PRONTO',s): return 'Pronto-socorro'
    return 'Internação (demais setores)'
ev['AREA']=ev.apply(area,axis=1)
print(ev.groupby('AREA').VALOR.agg(['size','sum']))
print(ev[ev.AREA=='Internação (demais setores)'].SETOR.value_counts().head(15))
ev.to_pickle('ev_urg.pkl')
K=12/10; F={6:6,24:24,72:72,168:168}
tot=[];exa=[];are=[]
allx=ev.groupby('EXAME').agg(exames=('VALOR','size'),custo_exame=('VALOR','sum'))
for f,lim in F.items():
    r=ev[ev.GAPH<=lim]
    x=r.groupby('EXAME').agg(repeticoes=('VALOR','size'),custo_repeticao=('VALOR','sum')).join(allx).sort_values('custo_repeticao',ascending=False)
    top=x.head(15)
    tot.append(dict(fase=f,meses=10,pacientes=int(ev.SAME.nunique()),pacientes_que_repetem=int(r.SAME.nunique()),exames=len(ev),repeticoes=len(r),
      custo_exame=round(ev.VALOR.sum(),2),custo_repeticao=round(r.VALOR.sum(),2),custo_mesmo_medico=round(r[r.PROPRIO].VALOR.sum(),2),
      custo_rep_urgencia=round(r[r.TIPO=='URGENCIA'].VALOR.sum(),2),custo_rep_internacao=round(r[r.TIPO=='INTERNACAO'].VALOR.sum(),2),
      top15_custo_repeticao=round(top.custo_repeticao.sum(),2)))
    for i,(n,y) in enumerate(top.iterrows()):
        exa.append(dict(fase=f,ordem=i+1,exame=n,exames=int(y.exames),repeticoes=int(y.repeticoes),custo_exame=round(y.custo_exame,2),custo_repeticao=round(y.custo_repeticao,2)))
    rs=x.iloc[15:].sum()
    exa.append(dict(fase=f,ordem=16,exame='Demais exames',exames=int(rs.exames),repeticoes=int(rs.repeticoes),custo_exame=round(rs.custo_exame,2),custo_repeticao=round(rs.custo_repeticao,2)))
    a=r.groupby('AREA').agg(repeticoes=('VALOR','size'),custo_repeticao=('VALOR','sum'))
    ea=ev.groupby('AREA').agg(exames=('VALOR','size'),custo_exame=('VALOR','sum'))
    for n,y in a.join(ea).sort_values('custo_repeticao',ascending=False).iterrows():
        are.append(dict(fase=f,area=n,exames=int(y.exames),repeticoes=int(y.repeticoes),custo_exame=round(y.custo_exame,2),custo_repeticao=round(y.custo_repeticao,2)))
bins=[-1,6,24,72,168]; labs=['Até 6 horas','6 a 24 horas','24 a 72 horas','3 a 7 dias']
r=ev[ev.GAPH<=168].copy(); r['faixa']=pd.cut(r.GAPH,bins,labels=labs)
fx=r.groupby('faixa',observed=False).agg(repeticoes=('VALOR','size'),custo_repeticao=('VALOR','sum'),pacientes=('SAME','nunique')).reset_index()
fx=[dict(ordem=i+1,faixa=str(y.faixa),repeticoes=int(y.repeticoes),pacientes=int(y.pacientes),custo_repeticao=round(y.custo_repeticao,2)) for i,y in fx.iterrows()]
code='\n\n'.join(f'# ===== {f} =====\n'+open(f).read() for f in ['load.py','add_maio.py','urg.py','urg2.py'])
meta=[{"label":"script.py","value":code,"type":"code","lang":"python"},{"label":"Entrada","value":"Planilhas RED 8, pedidos jan–out/2026 (10 meses), Urgência + Internação, sem pedido excluído. Repetição = mesmo exame, mesmo paciente, em pedido diferente; fase = horas desde o pedido anterior (data + hora do pedido)."}]
for nm,rows in [('u_total',tot),('u_exames',exa),('u_areas',are),('u_faixas',fx)]:
    json.dump({"rows":rows,"meta":meta},open(f'out/{nm}.json','w'),ensure_ascii=False); print(nm,len(rows))
for t in tot: print(t['fase'],t['repeticoes'],round(t['custo_repeticao']*K),round(t['custo_exame']*K),round(t['custo_repeticao']/t['custo_exame']*100,1),round(t['custo_mesmo_medico']/t['custo_repeticao']*100))
print(fx); print([a for a in are if a['fase']==24])
