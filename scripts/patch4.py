# Layout de computador: hero com número em destaque, colunas alinhadas e blocos lado a lado
def apply(s):
    def rep(a,b):
        nonlocal s
        assert a in s, 'NF: '+a[:80]
        s=s.replace(a,b,1)
    rep('@media (min-width:1000px){.rx{zoom:1.05}}',open('/home/claude/desk.css').read()+'@media (min-width:1000px){.rx{zoom:1.05}}')
    rep('    <div class="rx-hero-in">\n      <span class="rx-eye">','    <div class="rx-hero-in"><div>\n      <span class="rx-eye">')
    rep(' por ano.</p>\n    </div>\n  </section>',' por ano.</p>\n    </div>\n    <div class="rx-big"><span>Repetição nos eletivos · por ano</span><strong data-draw="v" data-source="kpi" data-field="custo_repeticao_ano" data-fmt="short">—</strong><em>repetição em até <b data-draw="fase-txt">—</b> · pedidos de jan a out/26</em></div></div>\n  </section>')
    rep("document.querySelectorAll('#fase').forEach(b => { b.hidden = id === 'urg'; });","document.querySelectorAll('#fase,.rx-big').forEach(b => { b.hidden = id === 'urg'; });")
    return s

_apply4 = apply
def apply(s):
    s = _apply4(s)
    def rep(a,b):
        nonlocal s
        assert a in s, 'NF: '+a[:80]
        s=s.replace(a,b,1)
    rep('<p class="rx-lead">Nos eletivos, de cada R$ 100 gastos com exames,',
        '<p class="rx-lead rx-h-u" hidden>Em urgência e internação, de cada R$ 100 gastos com exames, <b data-draw="v" data-source="u_kpi" data-field="pct_custo" data-fmt="brl">—</b> vão para exames pedidos de novo para o mesmo paciente em até <b data-draw="faseu-txt">—</b> — cerca de <b data-draw="v" data-source="u_kpi" data-field="custo_repeticao_ano" data-fmt="short">—</b> por ano.</p>\n      <p class="rx-lead rx-h-el">Nos eletivos, de cada R$ 100 gastos com exames,')
    rep('<div class="rx-big"><span>Repetição nos eletivos · por ano</span>','<div class="rx-big rx-h-el"><span>Repetição nos eletivos · por ano</span>')
    rep('pedidos de jan a out/26</em></div></div>','pedidos de jan a out/26</em></div>\n    <div class="rx-big rx-h-u" hidden><span>Repetição em urgência e internação · por ano</span><strong data-draw="v" data-source="u_kpi" data-field="custo_repeticao_ano" data-fmt="short">—</strong><em>repetição em até <b data-draw="faseu-txt">—</b> · pedidos de jan a out/26</em></div></div>')
    rep("document.querySelectorAll('#fase,.rx-big').forEach(b => { b.hidden = id === 'urg'; });","document.querySelectorAll('#fase,.rx-h-el').forEach(b => { b.hidden = id === 'urg'; });\n    document.querySelectorAll('.rx-h-u').forEach(b => { b.hidden = id !== 'urg'; });")
    rep("  dash.draw('fasetab', el => {","  dash.draw('faseu-txt', el => { const f = +(dash.params().fase_u ?? 24); el.textContent = f === 168 ? '7 dias' : f + ' horas'; });\n  dash.draw('fasetab', el => {")
    rep('.rx-big[hidden]{display:none}','.rx-big[hidden],.rx-lead[hidden]{display:none}')
    return s
