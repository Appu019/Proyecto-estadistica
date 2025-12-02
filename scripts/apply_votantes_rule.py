import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind
import json

path = 'app/data/EG2025_2v_20251026_235911_6311285959951043675.csv'

# Leer CSV con mismos nombres que el servicio
df = pd.read_csv(path, header=None, low_memory=False)
df.columns = [
    "ID", "Cargo", "CodigoPais", "Pais", "CodigoDepartamento", "Departamento",
    "CodigoCircunscripcionU", "CodigoCircunscripcionE", "Provincia", "Municipio", "CodigoLocalidad",
    "Localidad", "CodigoRecinto", "Recinto", "DireccionRecinto", "Mesa", "Votantes",
    "PDC", "LIBRE", "VotosValidos", "VotosNulos", "VotosBlancos", "TotalSufragantes",
    "TotalEmitidos", "VotosPDC", "VotosLIBRE", "TotalVotos", "OtraColumna"
]

# Convertir columnas numéricas
for c in ['PDC', 'LIBRE', 'Votantes']:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Filtrar Bolivia
df_bol = df[df['Pais'] == 'BOLIVIA'].copy()
# Eliminar filas con PDC/LIBRE faltantes
df_bol = df_bol.dropna(subset=['PDC', 'LIBRE'])

# Calcular ganador
df_bol['PartidoGanador'] = df_bol.apply(lambda r: 'PDC' if r['PDC'] > r['LIBRE'] else 'LIBRE', axis=1)

# Regla por Votantes: encima de la mediana => Urbana
median_vot = df_bol['Votantes'].median()
df_bol['TipoZona'] = df_bol['Votantes'].apply(lambda v: 'Urbana' if (pd.notna(v) and v > median_vot) else 'Rural')

# Contingency
tabla = pd.crosstab(df_bol['PartidoGanador'], df_bol['TipoZona'])
# Chi2 (pearson)
chi2_res = None
try:
    chi2, p, dof, expected = chi2_contingency(tabla, correction=False)
    chi2_res = {'chi2': float(chi2), 'p_value': float(p), 'dof': int(dof), 'expected': expected.tolist()}
except Exception as e:
    chi2_res = {'error': str(e)}

# T-test PDC between zones
urb = df_bol[df_bol['TipoZona'] == 'Urbana']['PDC']
rur = df_bol[df_bol['TipoZona'] == 'Rural']['PDC']
if len(urb) < 2 or len(rur) < 2:
    t_res = {'error': 'Datos insuficientes para la prueba T'}
else:
    t_stat, pval = ttest_ind(urb, rur, nan_policy='omit')
    means = {'urbana': float(urb.mean()), 'rural': float(rur.mean())}
    stds = {'urbana': float(urb.std()), 'rural': float(rur.std())}
    ns = {'urbana': int(len(urb)), 'rural': int(len(rur))}
    pooled_std = np.sqrt(((ns['urbana']-1)*stds['urbana']**2 + (ns['rural']-1)*stds['rural']**2) / (ns['urbana'] + ns['rural'] - 2))
    cohens_d = abs(means['urbana'] - means['rural']) / pooled_std if pooled_std > 0 else None
    t_res = {'statistic': float(t_stat), 'p_value': float(pval), 'means': means, 'std_devs': stds, 'sample_sizes': ns, 'cohen_d': cohens_d}

output = {
    'median_votantes': median_vot,
    'contingency_table': tabla.to_dict(),
    'chi2': chi2_res,
    't_test': t_res
}

print(json.dumps(output, indent=2, ensure_ascii=False))
