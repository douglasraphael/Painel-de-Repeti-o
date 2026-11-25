import re, json, os
s=open('index.html').read()
def rep(a,b,cnt=1):
    global s
    assert a in s, 'NF: '+a[:70]
    s=s.replace(a,b) if cnt==0 else s.replace(a,b,cnt)
def cut(start,end):
    global s
    i=s.index(start); j=s.index(end,i)+len(end); s=s[:i]+s[j:]
# logos -> texto
s=re.sub(r'<div class="rx-brand">.*?</div><span class="rx-tag">','<div class="rx-brand"><b class="rx-bt1">São Cristóvão Saúde</b><span class="rx-logo-sep"></span><span class="rx-bt2">Medicina Diagnóstica</span></div><span class="rx-tag">',s,1,flags=re.S)
rep(".rx tr.rx-in td{background:#eef4fc}",".rx tr.rx-in td{background:#eef4fc}\n.rx-fase[hidden]{display:none}")
rep(".rx-logo-sep{",".rx-bt1{font-size:1.05rem;font-weight:800;color:var(--nv)}.rx-bt2{font-size:.9rem;font-weight:700;color:var(--mu)}\n.rx-logo-sep{")
rep("Repetição de exames · pacientes eletivos","Repetição de exames · RED 8")
rep("De cada R$ 100 gastos com exames de pacientes eletivos,","Nos eletivos, de cada R$ 100 gastos com exames,")
rep('data-tab="geral" aria-selected="true">Visão geral</button>\n    <button type="button" class="rx-tab" role="tab" data-tab="medicos" aria-selected="false">Por médico</button>',
    'data-tab="geral" aria-selected="true">Eletivos</button>\n    <button type="button" class="rx-tab" role="tab" data-tab="urg" aria-selected="false">Urgência e Internação</button>\n    <button type="button" class="rx-tab" role="tab" data-tab="medicos" aria-selected="false">Médicos (eletivos)</button>')
rep('data-v="9">9 meses</button>','data-v="9">10 meses</button>')
rep("vale para todo o painel","vale para Eletivos e Médicos")
rep("Em amarelo, os que já têm protocolo em construção.","Em amarelo, os que já têm proposta de protocolo.")
rep("p ? 'protocolo' : ''","p ? 'proposta' : ''")
rep("Ferritina e vitamina B12 em andamento; estender a TSH/T4 livre, vitamina D e hemoglobina glicada.","Implantar as propostas de ferritina e vitamina B12 e, depois, estender a TSH/T4 livre, vitamina D e hemoglobina glicada.")
rep("o alvo realista sai dos protocolos por exame.","o alvo realista sai dos protocolos por exame, quando forem implantados.")
rep("competências jan–abr e jun–out/2026 (9 meses; maio não recebido).","pedidos de jan a out/2026 (10 meses).")
s=re.sub(r"6 meses \(até 180\) e 9 meses \(todo o período\)\. Repetições de exames feitos antes de janeiro ou em maio não aparecem\. Valores por ano = período × 12/9\.",
 "6 meses (até 180) e 10 meses (todo o período). Repetições de exames feitos antes de janeiro não aparecem. Valores por ano = período × 12/10.",s)
s=s.replace("(× 12/9)","(× 12/10)")
cut('\n      <section class="rx-card" id="unidades">','</section>')
cut("dash.calc('setores_tab'","})); }});\n")
cut("  dash.draw('setores', el => {","  });\n")
rep("const def = {reducao: 20, ordem_med: 'pac', fase: 9};","const def = {reducao: 20, ordem_med: 'pac', fase: 9, fase_u: 24, reducao_u: 20};")
rep("    document.querySelectorAll('.rx-pane').forEach(p => { p.hidden = p.id !== id; });\n","    document.querySelectorAll('.rx-pane').forEach(p => { p.hidden = p.id !== id; });\n    document.querySelectorAll('#fase').forEach(b => { b.hidden = id === 'urg'; });\n")
rep("['geral', 'medicos'].includes(h)","['geral', 'urg', 'medicos'].includes(h)")
rep("el.textContent = f === 1 ? '1 mês' : f + ' meses'; });","el.textContent = f === 1 ? '1 mês' : f === 9 ? '10 meses' : f + ' meses'; });")
urg=open('urg_pane.html').read(); calcs=open('urg_calcs.js').read(); draws=open('urg_draws.js').read()
rep("    </section>\n  </div>\n</div>\n\n<script>","    </section>\n\n"+urg+"  </div>\n</div>\n\n<script>")
i=s.index("</script>"); s=s[:i]+calcs+s[i:]
rep("  dash.draw('medbars', el => {",draws+"  dash.draw('medbars', el => {")
import patch2
s=patch2.apply(s)
s=s.replace('<meta name="dash-one-writer">\n<meta name="dash-form" content="dashboard">\n','')
# dados embutidos
M={'total':'f_total','exames':'f_exames','med_rank':'f_med_rank','med_total':'f_med_total','faixas':'f_faixas','u_total':'u_total','u_exames':'u_exames','u_areas':'u_areas','u_faixas':'u_faixas'}
D={k:json.load(open(f'out/{v}.json'))['rows'] for k,v in M.items()}
shim=open('shim.js').read()
head='''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Análise executiva de repetição de exames · RED 8</title>
<style>body{margin:0;background:#eef3fa}</style>
</head>
<body>
<div id="dash-root">
'''
dados='<script>window.DADOS = '+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';</script>\n<script>\n'+shim+'\n</script>\n'
# insere dados+shim antes do primeiro <script> da página
i=s.index('<script>'); s=s[:i]+dados+s[i:]
s=head+s+'\n<script>dash._render();</script>\n</div>\n</body>\n</html>\n'
os.makedirs('painel-de-repeti-o',exist_ok=True)
open('painel-de-repeti-o/index.html','w').write(s)
print(len(s))
