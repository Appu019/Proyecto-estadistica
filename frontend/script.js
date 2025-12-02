document.addEventListener("DOMContentLoaded", function () {
  const resultsDiv = document.getElementById('results-content');
  const loadingDiv = document.getElementById('loading');
  const refreshBtn = document.getElementById('refresh');

  function fmt(n, digits=3){ if(n===null||n===undefined) return '—'; return (typeof n === 'number') ? n.toFixed(digits) : String(n) }

  function buildContingencyTable(obj){
    if(!obj) return '<div class="small">No hay datos</div>';
    // obj: { Zona: {Partido: count, ...}, ... }
    // find all parties and zones
    const zones = Object.keys(obj);
    const partiesSet = new Set();
    zones.forEach(z=> Object.keys(obj[z]).forEach(p=>partiesSet.add(p)));
    const parties = Array.from(partiesSet);
    let html = '<table class="contingency"><thead><tr><th>Partido \ Zona</th>' + zones.map(z=>`<th>${z}</th>`).join('') + '</tr></thead><tbody>';
    parties.forEach(p=>{
      html += '<tr><td>'+p+'</td>' + zones.map(z=>`<td>${(obj[z][p]!==undefined)?obj[z][p]:0}</td>`).join('') + '</tr>';
    });
    html += '</tbody></table>';
    return html;
  }

  function render(data){
    console.log('Datos recibidos:', data);
    // Chi-square
    const chi = data.chi_square || {};
    if(chi.error){
      document.getElementById('chi2').textContent = '—';
      document.getElementById('p_value').textContent = '—';
      document.getElementById('dof').textContent = '—';
      document.getElementById('chi-interpret').textContent = chi.error;
      document.getElementById('contingency-table').innerHTML = buildContingencyTable(chi.contingency_table);
    } else {
      document.getElementById('chi2').textContent = fmt(chi.chi2,4);
      document.getElementById('p_value').textContent = fmt(chi.p_value,6);
      document.getElementById('dof').textContent = (chi.dof!==undefined)?chi.dof: (chi.degrees_of_freedom || '—');
      document.getElementById('chi-interpret').textContent = (chi.interpretation && chi.interpretation.decision) ? chi.interpretation.decision : '—';
      document.getElementById('contingency-table').innerHTML = buildContingencyTable(chi.contingency_table || chi.contingency_table);
    }

    // T-test
    const tt = data.t_test || {};
    if(tt.error){
      document.getElementById('t_statistic').textContent = '—';
      document.getElementById('t_p_value').textContent = '—';
      document.getElementById('means').textContent = tt.error;
      document.getElementById('t-interpret').textContent = tt.error;
    } else {
      document.getElementById('t_statistic').textContent = fmt(tt.statistic,4);
      document.getElementById('t_p_value').textContent = fmt(tt.p_value,6);
      // Means
      if(tt.means){
        const m = tt.means;
        document.getElementById('means').innerHTML = Object.keys(m).map(k=>`<div class="small">${k}: <strong>${fmt(m[k],3)}</strong></div>`).join('');
      }
      // stds and ns
      const stds = tt.std_devs || tt.std_devs || tt.std_devs;
      if(tt.std_devs){
        document.getElementById('stds').innerHTML = Object.keys(tt.std_devs).map(k=>`<div class="small">${k}: ${fmt(tt.std_devs[k],3)}</div>`).join('');
      }
      if(tt.sample_sizes){
        document.getElementById('ns').innerHTML = Object.keys(tt.sample_sizes).map(k=>`<div class="small">${k}: ${tt.sample_sizes[k]}</div>`).join('');
      }
      document.getElementById('t-interpret').textContent = (tt.interpretation && tt.interpretation.decision) ? tt.interpretation.decision : '—';
    }

    loadingDiv.style.display = 'none';
    resultsDiv.style.display = 'grid';
    try{ updateCharts(data); }catch(e){ console.warn('Charts update failed', e); }
  }

  // Chart instances
  let contingencyChartInstance = null;
  let meansChartInstance = null;

  function updateCharts(data){
    // Contingency chart
    const chi = data.chi_square || {};
    const contObj = chi.contingency_table || chi.contingency_table || null;
    const zones = contObj ? Object.keys(contObj) : [];
    const parties = contObj ? Array.from(new Set(zones.flatMap(z => Object.keys(contObj[z])))) : [];

    const colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd'];

    const datasets = parties.map((p,i) => ({
      label: p,
      data: zones.map(z => (contObj && contObj[z] && contObj[z][p]) ? contObj[z][p] : 0),
      backgroundColor: colors[i % colors.length]
    }));

    const ctx = document.getElementById('contingencyChart').getContext('2d');
    if(contingencyChartInstance){ contingencyChartInstance.destroy(); }
    contingencyChartInstance = new Chart(ctx, {
      type: 'bar',
      data: { labels: zones, datasets },
      options: { responsive:true, plugins: { legend:{ position:'bottom' } }, scales: { y: { beginAtZero:true } } }
    });

    // Means chart
    const tt = data.t_test || {};
    const means = tt.means || null;
    const meanLabels = means ? Object.keys(means) : [];
    const meanData = means ? meanLabels.map(k => means[k]) : [];
    const ctx2 = document.getElementById('meansChart').getContext('2d');
    if(meansChartInstance){ meansChartInstance.destroy(); }
    meansChartInstance = new Chart(ctx2, {
      type: 'bar',
      data: { labels: meanLabels, datasets: [{ label: 'Media PDC', data: meanData, backgroundColor: '#007bff' }] },
      options: { responsive:true, plugins:{ legend:{ display:false } }, scales:{ y:{ beginAtZero:false } } }
    });
  }

  function fetchAndRender(){
    loadingDiv.style.display = 'block';
    resultsDiv.style.display = 'none';
    fetch('http://127.0.0.1:8000/data/analyze-results')
      .then(resp => resp.json())
      .then(render)
      .catch(err => { console.error('Error:',err); loadingDiv.textContent = 'Error al cargar los resultados.' });
  }

  refreshBtn.addEventListener('click', fetchAndRender);
  // primero fetch
  fetchAndRender();
});