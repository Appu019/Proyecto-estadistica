import pandas as pd
from scipy.stats import ttest_ind
import numpy as np

def chi_square_test_from_df(df: pd.DataFrame) -> dict:
    tabla = pd.crosstab(df['PartidoGanador'], df['TipoZona'])
    if tabla.shape[0] < 2 or tabla.shape[1] < 2:
        # No hay suficiente variabilidad
        return {
            "chi2": None,
            "p_value": None,
            "dof": 0,
            "expected": []
        }

    from scipy.stats import chi2_contingency
    chi2, p_valor, dof, expected = chi2_contingency(tabla)

    def safe_float(val):
        return float(val) if not np.isnan(val) else None

    return {
        "chi2": safe_float(chi2),
        "p_value": safe_float(p_valor),
        "dof": int(dof),
        "expected": [[safe_float(cell) for cell in row] for row in expected.tolist()]
    }

def t_test_from_df(df: pd.DataFrame) -> dict:
    df['TipoZona'] = df.apply(
        lambda row: 'Urbana' if row['CodigoCircunscripcionU'] > 0 else 'Rural', axis=1
    )

    grupo_urbano = df[df['TipoZona'] == 'Urbana']['PDC']
    grupo_rural = df[df['TipoZona'] == 'Rural']['PDC']

    if len(grupo_urbano) < 2 or len(grupo_rural) < 2:
        # No hay suficientes datos en ambas categorías
        return {"statistic": None, "p_value": None}

    t_stat, p_valor = ttest_ind(grupo_urbano, grupo_rural, nan_policy='omit')

    def safe_float(val):
        return float(val) if not np.isnan(val) else None

    return {
        "statistic": safe_float(t_stat),
        "p_value": safe_float(p_valor)
    }