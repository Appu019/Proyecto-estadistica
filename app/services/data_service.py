import pandas as pd
from app.utils.statistics import chi_square_test_from_df, t_test_from_df
from app.utils.data_processing import procesar_datos_mesa

def cargar_y_analizar_datos():
    # Cargar el archivo CSV
    df = pd.read_csv("app/data/EG2025_2v_20251026_235911_6311285959951043675.csv", header=None, low_memory=False)
    

    # Asignar 28 nombres de columnas según el orden real del archivo
    df.columns = [
        "ID", "Cargo", "CodigoPais", "Pais", "CodigoDepartamento", "Departamento",
        "CodigoCircunscripcionU", "CodigoCircunscripcionE", "Provincia", "Municipio", "CodigoLocalidad",
        "Localidad", "CodigoRecinto", "Recinto", "DireccionRecinto", "Mesa", "Votantes",
        "PDC", "LIBRE", "VotosValidos", "VotosNulos", "VotosBlancos", "TotalSufragantes",
        "TotalEmitidos", "VotosPDC", "VotosLIBRE", "TotalVotos", "OtraColumna"
    ]

    # Filtrar solo votos de Bolivia
    df_bolivia = df[df['Pais'] == 'BOLIVIA'].copy()

    # Seleccionar solo las columnas necesarias e incluir 'Votantes' para la regla
    cols_needed = ["PDC", "LIBRE", "Votantes", "CodigoCircunscripcionU", "CodigoCircunscripcionE", "CodigoLocalidad", "Departamento"]
    df_bolivia = df_bolivia[cols_needed].copy()
    # Asegurar numérico (NaN si no convertible) y conservar filas
    df_bolivia['PDC'] = pd.to_numeric(df_bolivia['PDC'], errors='coerce')
    df_bolivia['LIBRE'] = pd.to_numeric(df_bolivia['LIBRE'], errors='coerce')
    df_bolivia['Votantes'] = pd.to_numeric(df_bolivia['Votantes'], errors='coerce')
    df_bolivia['CodigoCircunscripcionU'] = pd.to_numeric(df_bolivia['CodigoCircunscripcionU'], errors='coerce')
    df_bolivia['CodigoCircunscripcionE'] = pd.to_numeric(df_bolivia['CodigoCircunscripcionE'], errors='coerce')
    df_bolivia['CodigoLocalidad'] = pd.to_numeric(df_bolivia['CodigoLocalidad'], errors='coerce')
    df_bolivia = df_bolivia.dropna(subset=['PDC', 'LIBRE'])

    # Procesar datos para crear "PartidoGanador" y "TipoZona" (TipoZona se basará en Votantes > mediana)
    df_procesado = procesar_datos_mesa(df_bolivia.to_dict(orient="records"))

    # Chi-cuadrado
    chi_result = chi_square_test_from_df(df_procesado)

    # T-Student
    t_result = t_test_from_df(df_procesado)

    return {
        "chi_square": chi_result,
        "t_test": t_result
    }
    
def get_zone_distribution():
    df = pd.read_csv("app/data/EG2025_2v_20251026_235911_6311285959951043675.csv", header=None, low_memory=False)
        
    df.columns = [
        "ID", "Cargo", "CodigoPais", "Pais", "CodigoDepartamento", "Departamento",
        "CodigoCircunscripcionU", "CodigoCircunscripcionE", "Provincia", "Municipio", "CodigoLocalidad",
        "Localidad", "CodigoRecinto", "Recinto", "DireccionRecinto", "Mesa", "Votantes",
        "PDC", "LIBRE", "VotosValidos", "VotosNulos", "VotosBlancos", "TotalSufragantes",
        "TotalEmitidos", "VotosPDC", "VotosLIBRE", "TotalVotos", "Extra"
    ]
    df_bolivia = df[df['Pais'] == 'BOLIVIA'].copy()
    # Seleccionar y convertir columnas necesarias
    cols_needed = ["PDC", "LIBRE", "Votantes", "CodigoCircunscripcionU", "CodigoCircunscripcionE", "CodigoLocalidad", "Departamento"]
    df_bolivia = df_bolivia[cols_needed].copy()
    for c in ['PDC','LIBRE','Votantes','CodigoCircunscripcionU','CodigoCircunscripcionE','CodigoLocalidad']:
        df_bolivia[c] = pd.to_numeric(df_bolivia[c], errors='coerce')
    df_bolivia = df_bolivia.dropna(subset=['PDC','LIBRE'])
    # Usar el mismo procesamiento para obtener TipoZona basada en Votantes
    df_proc = procesar_datos_mesa(df_bolivia.to_dict(orient='records'))
    counts = df_proc['TipoZona'].value_counts().to_dict()
    return {"zone_distribution": counts}