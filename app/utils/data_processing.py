import pandas as pd


def procesar_datos_mesa(data_list: list) -> pd.DataFrame:
    df = pd.DataFrame(data_list)

    # Convertir a numérico (manejar errores como NaN)
    df['PDC'] = pd.to_numeric(df['PDC'], errors='coerce')
    df['LIBRE'] = pd.to_numeric(df['LIBRE'], errors='coerce')
    # Asegurar columna de votantes y convertir a numérico
    if 'Votantes' in df.columns:
        df['Votantes'] = pd.to_numeric(df['Votantes'], errors='coerce')
    # Mantener conversión de códigos por si existen
    if 'CodigoCircunscripcionU' in df.columns:
        df['CodigoCircunscripcionU'] = pd.to_numeric(df['CodigoCircunscripcionU'], errors='coerce')
    if 'CodigoCircunscripcionE' in df.columns:
        df['CodigoCircunscripcionE'] = pd.to_numeric(df['CodigoCircunscripcionE'], errors='coerce')
    if 'CodigoLocalidad' in df.columns:
        df['CodigoLocalidad'] = pd.to_numeric(df['CodigoLocalidad'], errors='coerce')

    # Eliminar filas con valores faltantes en columnas clave
    df = df.dropna(subset=['PDC', 'LIBRE'])

    # Clasificar partido ganador en la mesa
    df['PartidoGanador'] = df.apply(
        lambda row: 'PDC' if row['PDC'] > row['LIBRE'] else 'LIBRE',
        axis=1
    )

    # Clasificar tipo de zona usando regla: Votantes > mediana -> Urbana
    # Si no hay columna Votantes, caer en fallback: CodigoCircunscripcionU >0 -> Urbana
    if 'Votantes' in df.columns and not df['Votantes'].isna().all():
        median_vot = df['Votantes'].median()
        df['TipoZona'] = df['Votantes'].apply(lambda v: 'Urbana' if (pd.notna(v) and v > median_vot) else 'Rural')
    else:
        df['TipoZona'] = df.apply(lambda row: 'Urbana' if (pd.notna(row.get('CodigoCircunscripcionU')) and row.get('CodigoCircunscripcionU') > 0) else 'Rural', axis=1)

    return df