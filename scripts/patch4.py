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
