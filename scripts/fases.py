import pandas as pd, numpy as np, json, re
ev=pd.read_pickle('eventos.pkl'); ev=ev[ev.MES<='2026-10'].copy()
ev['REP']=ev.GAP.notna()
norm=lambda s: re.sub(r'^(DRA?\.?\s+)','',' '.join(str(s).upper().split()))
ev['MEDN']=ev.MED.map(norm)
ev=ev.sort_values(['SAME','CD EXAME','DATA','PEDIDO'])
ev['MEDN_ANT']=ev.groupby(['SAME','CD EXAME']).MEDN.shift()
ev['PROPRIO']=ev.REP&(ev.MEDN==ev.MEDN_ANT)
K=12/10; FASES={1:30,3:90,6:180,9:10**6}; MIN=100
tot=[];exa=[];sete=[];medr=[];medt=[]
allx=ev.groupby('EXAME').agg(exames=('VALOR','size'),custo_exame=('VALOR','sum'))
gm=ev.groupby('MEDN'); medbase=pd.DataFrame(dict(pacientes=gm.SAME.nunique(),exames=gm.size()))
medbase=medbase[(medbase.pacientes>=MIN)&(~medbase.index.str.contains('HOSPITAL'))]
for f,lim in FASES.items():
    r=ev[ev.REP&(ev.GAP<=lim)]
    cm=r[r.PROPRIO].VALOR.sum()
    x=r.groupby('EXAME').agg(repeticoes=('VALOR','size'),custo_repeticao=('VALOR','sum')).join(allx).sort_values('custo_repeticao',ascending=False)
    top=x.head(15)
    tot.append(dict(fase=f,meses=10,pacientes=int(ev.SAME.nunique()),pacientes_que_repetem=int(r.SAME.nunique()),exames=len(ev),repeticoes=len(r),
        custo_exame=round(ev.VALOR.sum(),2),custo_repeticao=round(r.VALOR.sum(),2),custo_mesmo_medico=round(cm,2),custo_outro_medico=round(r.VALOR.sum()-cm,2),
        top15_custo_repeticao=round(top.custo_repeticao.sum(),2)))
    for i,(n,y) in enumerate(top.iterrows()):
        exa.append(dict(fase=f,ordem=i+1,exame=n.strip(),exames=int(y.exames),repeticoes=int(y.repeticoes),custo_exame=round(y.custo_exame,2),custo_repeticao=round(y.custo_repeticao,2)))
    rs=x.iloc[15:].sum()
    exa.append(dict(fase=f,ordem=16,exame='Demais exames',exames=int(rs.exames),repeticoes=int(rs.repeticoes),custo_exame=round(rs.custo_exame,2),custo_repeticao=round(rs.custo_repeticao,2)))
    s=r.groupby('SETOR').agg(repeticoes=('VALOR','size'),custo_repeticao=('VALOR','sum')).sort_values('custo_repeticao',ascending=False)
    for n,y in s.iterrows(): sete.append(dict(fase=f,setor=str(n).strip(),repeticoes=int(y.repeticoes),custo_repeticao=round(y.custo_repeticao,2)))
    gr=r.groupby('MEDN'); d=medbase.copy()
    d['repeticoes']=gr.size(); d['custo_repeticao']=gr.VALOR.sum(); d['rep_proprio']=r[r.PROPRIO].groupby('MEDN').size()
    d=d.fillna(0); media=d.repeticoes.sum()/d.pacientes.sum()
    for n,y in d.iterrows():
        rp=y.repeticoes/y.pacientes
        medr.append(dict(fase=f,medico=n,pacientes=int(y.pacientes),repeticoes=int(y.repeticoes),rep_por_paciente=round(rp,3),rep_proprio=int(y.rep_proprio),
           custo_repeticao=round(y.custo_repeticao,2),vs_media=round(rp/media,3) if media else 0))
    acima=d[(d.repeticoes/d.pacientes)>=2*media]
    medt.append(dict(fase=f,meses=10,medicos=len(d),media_rep_por_paciente=round(media,4),medicos_acima_2x=len(acima),custo_acima_2x=round(acima.custo_repeticao.sum(),2)))
# fases não cumulativas
bins=[-1,30,90,180,10**6]; labs=['Até 1 mês','1 a 3 meses','3 a 6 meses','Mais de 6 meses']
r=ev[ev.REP].copy(); r['faixa']=pd.cut(r.GAP,bins,labels=labs)
fx=r.groupby('faixa',observed=False).agg(repeticoes=('VALOR','size'),custo_repeticao=('VALOR','sum'),pacientes=('SAME','nunique')).reset_index()
fx=[dict(ordem=i+1,faixa=str(y.faixa),repeticoes=int(y.repeticoes),pacientes=int(y.pacientes),custo_repeticao=round(y.custo_repeticao,2)) for i,y in fx.iterrows()]
code='\n\n'.join(f'# ===== {f} =====\n'+open(f).read() for f in ['load.py','analise.py','fases.py'])
meta=[{"label":"script.py","value":code,"type":"code","lang":"python"},{"label":"Entrada","value":"Planilhas RED 8, pedidos jan–out/2026 (10 meses), Externo + Ambulatório, sem pedido excluído. Fase = tempo desde o exame anterior do mesmo paciente (1 mês = 30 dias, 3 = 90, 6 = 180, 9 = todo o período, até 10 meses)."}]
for nm,rows in [('f_total',tot),('f_exames',exa),('f_setores',sete),('f_med_rank',medr),('f_med_total',medt),('f_faixas',fx)]:
    json.dump({"rows":rows,"meta":meta},open(f'out/{nm}.json','w'),ensure_ascii=False); print(nm,len(rows))
for t in tot: print(t['fase'],t['repeticoes'],t['custo_repeticao'],round(t['custo_repeticao']*K),t['pacientes_que_repetem'],round(t['custo_mesmo_medico']/t['custo_repeticao'],3))
print(fx); print(medt)
