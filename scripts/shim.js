// Mini-runtime para o painel funcionar como página estática (sem dependências externas).
window.d3 = {
  sum: (a, f) => a.reduce((s, x) => s + (+f(x) || 0), 0),
  max: (a, f) => a.length ? Math.max(...a.map(f)) : undefined
};
window.dash = (() => {
  const calcs = {}, draws = {}, onData = [];
  const params = {reducao: 25, ordem_med: 'pac', fase: 9, fase_u: 24, reducao_u: 25};
  const data = id => {
    if (calcs[id]) { const c = calcs[id]; return {status: 'ok', data: c.fn(...c.inputs.map(i => data(i).data))}; }
    if (window.DADOS[id]) return {status: 'ok', data: window.DADOS[id]};
    return {status: 'missing', data: []};
  };
  const render = () => {
    onData.forEach(f => f());
    Object.entries(draws).forEach(([n, f]) => document.querySelectorAll('[data-draw="' + n + '"]').forEach(el => f(el)));
  };
  return {
    data, calc: (id, c) => { calcs[id] = c; }, draw: (n, f) => { draws[n] = f; }, onData: f => { onData.push(f); },
    params: () => params, setParams: p => { Object.assign(params, p); render(); },
    setLink: id => { try { history.replaceState(null, '', '#' + id); } catch (e) {} },
    colors: ['#04347a', '#ffc20e'], _render: render
  };
})();
