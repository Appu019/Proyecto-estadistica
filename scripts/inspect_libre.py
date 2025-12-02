import pandas as pd

path = 'app/data/EG2025_2v_20251026_235911_6311285959951043675.csv'

# Leer con encabezado real (archivo parece tener header)
df = pd.read_csv(path, header=None, low_memory=False)
# Asignar nombres como en data_service.py
df.columns = [
    "ID", "Cargo", "CodigoPais", "Pais", "CodigoDepartamento", "Departamento",
    "CodigoCircunscripcionU", "CodigoCircunscripcionE", "Provincia", "Municipio", "CodigoLocalidad",
    "Localidad", "CodigoRecinto", "Recinto", "DireccionRecinto", "Mesa", "Votantes",
    "PDC", "LIBRE", "VotosValidos", "VotosNulos", "VotosBlancos", "TotalSufragantes",
    "TotalEmitidos", "VotosPDC", "VotosLIBRE", "TotalVotos", "OtraColumna"
]

# Mostrar primeras columnas para inspección
print('Columns sample:', list(df.columns)[:30])

# Normalizar columnas si existen
cols = list(df.columns)
# Asegurar que existan 'PDC' y 'LIBRE' y 'CodigoCircunscripcionU' en el DF
for c in ['PDC','LIBRE','CodigoCircunscripcionU','Pais']:
    if c not in cols:
        print(f"Warning: column {c} not found in CSV headers")

# Convertir a numérico
df['PDC'] = pd.to_numeric(df['PDC'], errors='coerce')
df['LIBRE'] = pd.to_numeric(df['LIBRE'], errors='coerce')
df['CodigoCircunscripcionU'] = pd.to_numeric(df['CodigoCircunscripcionU'], errors='coerce')

# Filtrar Bolivia
df_bol = df[df['Pais']=='BOLIVIA'].copy()
# TipoZona: >0 => Urbana, else Rural (incluye NaN)
df_bol['TipoZona'] = df_bol['CodigoCircunscripcionU'].apply(lambda u: 'Urbana' if (pd.notna(u) and u>0) else 'Rural')
# Partido ganador
df_bol['PartidoGanador'] = df_bol.apply(lambda r: 'PDC' if r['PDC']>r['LIBRE'] else 'LIBRE', axis=1)

print('\nContingency table (PDC vs TipoZona):')
print(pd.crosstab(df_bol['PartidoGanador'], df_bol['TipoZona']))

rural = df_bol[df_bol['TipoZona']=='Rural']
print('\nTotal rural rows:', len(rural))
print('Rural LIBRE>0 count:', len(rural[rural['LIBRE']>0]))
print('Rural where LIBRE>PDC count:', len(rural[rural['LIBRE']>rural['PDC']]))

print('\nSample rural rows with LIBRE>0 or LIBRE>PDC:')
print(rural[(rural['LIBRE']>0) | (rural['LIBRE']>rural['PDC'])][['PDC','LIBRE','CodigoCircunscripcionU']].head(20).to_string())
