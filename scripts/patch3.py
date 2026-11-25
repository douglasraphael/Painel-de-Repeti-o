# Cenário de economia mais acima, com explicação e mais percentuais
def apply(s):
    def rep(a,b,all_=False):
        nonlocal s
        assert a in s, 'NF: '+a[:80]
        s=s.replace(a,b) if all_ else s.replace(a,b,1)
    rep(".rx-fase[hidden]{display:none}",".rx-fase[hidden]{display:none}\n.rx-pane>*{order:3}\n.rx-pane>.rx-fase,.rx-pane>.rx-head,.rx-pane>.rx-how-k{order:0}\n.rx-pane>#cenarios,.rx-pane>#u-cenarios{order:1}\n.rx-ex{margin:0;font-size:.8rem;line-height:1.5;color:var(--fg);background:var(--bg2);border:1px solid var(--ln);border-radius:6px;padding:10px 12px}\n.rx-ex b{color:var(--nv)}")
    EX='<p class="rx-ex">O gasto com repetição é o <b>teto</b>: quanto se economizaria se <b>todas</b> as repetições do prazo escolhido deixassem de acontecer (100%). Como parte delas é necessária, escolha um cenário: <b>conservador (10%)</b>, <b>moderado (25%)</b> ou <b>otimista (50%)</b> das repetições deixando de acontecer. Exemplo: se a repetição custa R$ 100 mil por ano e <b>50%</b> dos pedidos repetidos deixarem de existir, a economia é <b>R$ 50 mil por ano</b>.</p>'
    P=[(10,'Conservador · 10%'),(25,'Moderado · 25%'),(50,'Otimista · 50%'),(100,'Teto · 100%')]
    rep("× % de redução escolhido.","× % das repetições que deixam de acontecer.",True)
    rep("<label>Quanto da repetição deixa de acontecer</label>","<label>% das repetições que deixam de acontecer</label>",True)
    old_e='<button type="button" data-v="10">10%</button><button type="button" data-v="20">20%</button><button type="button" data-v="30">30%</button><button type="button" data-v="50">50%</button>'
    rep(old_e,''.join(f'<button type="button" data-v="{p}">{l}</button>' for p,l in P))
    old_u='<button type="button" data-k="reducao_u" data-v="10">10%</button><button type="button" data-k="reducao_u" data-v="20">20%</button><button type="button" data-k="reducao_u" data-v="30">30%</button><button type="button" data-k="reducao_u" data-v="50">50%</button>'
    rep(old_u,''.join(f'<button type="button" data-k="reducao_u" data-v="{p}">{l}</button>' for p,l in P))
    rep('deixam de acontecer.</p></div>\n      <div class="rx-sim">','deixam de acontecer.</p></div>\n      '+EX+'\n      <div class="rx-sim">')
    rep('deixam de acontecer.</p></div>\n        <div class="rx-sim">','deixam de acontecer.</p></div>\n        '+EX+'\n        <div class="rx-sim">')
    rep("['Redução de ' + s.reducao + '% da repetição', '− ' + F.short(s.economia_ano), 'rx-br-a']","[s.reducao + '% das repetições deixam de acontecer', '− ' + F.short(s.economia_ano), 'rx-br-a']",True)
    rep("['Gasto com repetição', F.short(s.repeticao_ano), '']","['Gasto com repetição (teto)', F.short(s.repeticao_ano), '']",True)
    rep("reducao: 20, ordem_med: 'pac', fase: 9, fase_u: 24, reducao_u: 20","reducao: 25, ordem_med: 'pac', fase: 9, fase_u: 24, reducao_u: 25")
    rep("dash.params().reducao ?? 20","dash.params().reducao ?? 25")
    rep("dash.params().reducao_u ?? 20","dash.params().reducao_u ?? 25")
    css=open('/home/claude/cv_style.css').read()
    rep('@media (min-width:1000px){.rx{zoom:1.05}}',css+'@media (min-width:1000px){.rx{zoom:1.05}}')
    return s
