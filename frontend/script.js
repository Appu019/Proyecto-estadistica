document.addEventListener("DOMContentLoaded", function () {
  const resultsDiv = document.getElementById('results-content');
  const loadingDiv = document.getElementById('loading');

  // Llamada a la API para obtener los resultados
  fetch('http://127.0.0.1:8000/data/analyze-results')
    .then(response => response.json())
    .then(data => {
      // Chi-square
      document.getElementById('chi2').textContent = data.chi_square.chi2;
      document.getElementById('p_value').textContent = data.chi_square.p_value;
      document.getElementById('dof').textContent = data.chi_square.dof;

      // T-test
      document.getElementById('t_statistic').textContent = data.t_test.statistic;
      document.getElementById('t_p_value').textContent = data.t_test.p_value;

      // Mostrar resultados
      loadingDiv.style.display = 'none';
      resultsDiv.style.display = 'block';
    })
    .catch(error => {
      console.error('Error al obtener los resultados:', error);
      loadingDiv.textContent = 'Error al cargar los resultados.';
    });
});