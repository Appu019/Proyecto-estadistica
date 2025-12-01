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

    # Seleccionar solo las columnas necesarias
    df_bolivia = df_bolivia[["PDC", "LIBRE", "CodigoCircunscripcionU", "CodigoCircunscripcionE", "Departamento"]].dropna()

    # Procesar datos para crear "PartidoGanador" y "TipoZona"
    df_procesado = procesar_datos_mesa(df_bolivia.to_dict(orient="records"))

    # Chi-cuadrado
    chi_result = chi_square_test_from_df(df_procesado)

    # T-Student
    t_result = t_test_from_df(df_procesado)

    return {
        "chi_square": chi_result,
        "t_test": t_result
    }