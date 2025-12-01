import pandas as pd

def procesar_datos_mesa(data_list: list) -> pd.DataFrame:
    df = pd.DataFrame(data_list)

    # Convertir columnas numéricas relevantes a tipo numérico
    df['PDC'] = pd.to_numeric(df['PDC'], errors='coerce')
    df['LIBRE'] = pd.to_numeric(df['LIBRE'], errors='coerce')
    df['CodigoCircunscripcionU'] = pd.to_numeric(df['CodigoCircunscripcionU'], errors='coerce')

    # Clasificar partido ganador
    df['PartidoGanador'] = df.apply(
        lambda row: 'PDC' if row['PDC'] > row['LIBRE'] else 'LIBRE', axis=1
    )

    # Clasificar tipo de zona: U > 0 como urbano, E > 0 como rural
    df['TipoZona'] = df.apply(
        lambda row: 'Urbana' if row['CodigoCircunscripcionU'] > 0 else 'Rural', axis=1
    )

    return df