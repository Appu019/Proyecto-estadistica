import pandas as pd
from scipy.stats import chi2_contingency

path = 'app/data/EG2025_2v_20251026_235911_6311285959951043675.csv'

# Leer como hace el servicio
df = pd.read_csv(path, header=None, low_memory=False)
df.columns = [
    "ID", "Cargo", "CodigoPais", "Pais", "CodigoDepartamento", "Departamento",
    "CodigoCircunscripcionU", "CodigoCircunscripcionE", "Provincia", "Municipio", "CodigoLocalidad",
    "Localidad", "CodigoRecinto", "Recinto", "DireccionRecinto", "Mesa", "Votantes",
    "PDC", "LIBRE", "VotosValidos", "VotosNulos", "VotosBlancos", "TotalSufragantes",
    "TotalEmitidos", "VotosPDC", "VotosLIBRE", "TotalVotos", "OtraColumna"
]

# Convertir a numérico donde haga falta
for c in ['PDC','LIBRE','CodigoCircunscripcionU','CodigoCircunscripcionE','CodigoLocalidad','Votantes']:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Filtrar Bolivia
df_bol = df[df['Pais']=='BOLIVIA'].copy()
# Asegurar que existan valores de PDC y LIBRE
df_bol = df_bol.dropna(subset=['PDC','LIBRE'])

# Calcular ganador
df_bol['PartidoGanador'] = df_bol.apply(lambda r: 'PDC' if r['PDC']>r['LIBRE'] else 'LIBRE', axis=1)

rules = {}
# Regla U (actual): CodigoCircunscripcionU >0 => Urbana
rules['U'] = df_bol['CodigoCircunscripcionU'].apply(lambda u: 'Urbana' if (pd.notna(u) and u>0) else 'Rural')
# Regla E: CodigoCircunscripcionE >0 => Urbana
rules['E'] = df_bol['CodigoCircunscripcionE'].apply(lambda u: 'Urbana' if (pd.notna(u) and u>0) else 'Rural')
# Regla Localidad: CodigoLocalidad >0 => Urbana
rules['Localidad'] = df_bol['CodigoLocalidad'].apply(lambda u: 'Urbana' if (pd.notna(u) and u>0) else 'Rural')
# Regla Votantes: arriba de mediana de Votantes => Urbana
median_vot = df_bol['Votantes'].median()
rules['Votantes_median'] = df_bol['Votantes'].apply(lambda v: 'Urbana' if (pd.notna(v) and v>median_vot) else 'Rural')

print('Median Votantes:', median_vot)

results = {}
for name, series in rules.items():
    tabla = pd.crosstab(df_bol['PartidoGanador'], series)
    results[name] = tabla
    print(f'\n--- Rule: {name} ---')
    print(tabla)
    # try chi2 without Yates
    try:
        chi2,p,dof,exp = chi2_contingency(tabla, correction=False)
        print('chi2:',chi2,'p:',p,'dof:',dof)
    except Exception as e:
        print('chi2 error:', e)

# Show a small sample where rules disagree between U and E
print('\nSample rows where U != E:')
mask = rules['U'] != rules['E']
print(df_bol[mask][['CodigoCircunscripcionU','CodigoCircunscripcionE','CodigoLocalidad','Votantes','PDC','LIBRE']].head(20).to_string())
