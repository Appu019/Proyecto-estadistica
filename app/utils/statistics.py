import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency

# En chi_square_test_from_df
def chi_square_test_from_df(df: pd.DataFrame) -> dict:
    tabla = pd.crosstab(df['PartidoGanador'], df['TipoZona'])
    if tabla.shape[0] < 2 or tabla.shape[1] < 2:
        return {
            "error": "No hay suficiente variabilidad en los datos para realizar la prueba de Chi-cuadrado.",
            "contingency_table": tabla.to_dict()
        }

    # Para tablas 2x2 la función aplica por defecto la corrección de Yates,
    # lo cual puede producir chi2 == 0 cuando las diferencias observadas son < 0.5.
    # Usamos correction=False para obtener la chi-cuadrado de Pearson sin corrección.
    chi2, p_valor, dof, expected = chi2_contingency(tabla, correction=False)

    # Interpretación
    alpha = 0.05
    decision = "No se rechaza H0" if p_valor > alpha else "Se rechaza H0"
    interpretation = {
        "H0": "No hay asociación entre el partido ganador y el tipo de circunscripción.",
        "H1": "Existe una asociación entre el partido ganador y el tipo de circunscripción.",
        "decision": f"{decision} (p = {p_valor:.3f} > {alpha}). No hay evidencia estadística de asociación." if p_valor > alpha else f"{decision} (p = {p_valor:.3e} < {alpha}). Hay asociación significativa."
    }

    # Devolver claves compatibles con el front y con el schema: incluir 'dof' y 'expected'
    return {
        "chi2": float(chi2),
        "p_value": float(p_valor),
        "dof": int(dof),
        "degrees_of_freedom": int(dof),
        "contingency_table": tabla.to_dict(),
        "expected": expected.tolist(),
        "expected_frequencies": expected.tolist(),
        "interpretation": interpretation
    }
def t_test_from_df(df: pd.DataFrame) -> dict:
    # Clasificar TipoZona usando regla Votantes > mediana, si está disponible
    if 'Votantes' in df.columns and not df['Votantes'].isna().all():
        median_vot = df['Votantes'].median()
        df['TipoZona'] = df['Votantes'].apply(lambda v: 'Urbana' if (pd.notna(v) and v > median_vot) else 'Rural')
    else:
        # Fallback a CodigoCircunscripcionU cuando no haya Votantes
        df['TipoZona'] = df.apply(lambda row: 'Urbana' if (pd.notna(row.get('CodigoCircunscripcionU')) and row.get('CodigoCircunscripcionU') > 0) else 'Rural', axis=1)

    urb = df[df['TipoZona'] == 'Urbana']['PDC']
    rur = df[df['TipoZona'] == 'Rural']['PDC']

    if len(urb) < 2 or len(rur) < 2:
        return {"error": "Datos insuficientes para la prueba T"}

    t_stat, p_val = ttest_ind(urb, rur, nan_policy='omit')

    # Cálculo de medias, desviaciones, tamaños
    means = {"urbana": float(urb.mean()), "rural": float(rur.mean())}
    stds = {"urbana": float(urb.std()), "rural": float(rur.std())}
    ns = {"urbana": len(urb), "rural": len(rur)}

    # Cohen's d (opcional)
    pooled_std = np.sqrt(((ns["urbana"]-1)*stds["urbana"]**2 + (ns["rural"]-1)*stds["rural"]**2) / (ns["urbana"] + ns["rural"] - 2))
    cohens_d = abs(means["urbana"] - means["rural"]) / pooled_std

    interpretation = {
        "H0": "Las medias de votos para PDC en zonas urbanas y rurales son iguales.",
        "H1": "Las medias de votos para PDC en zonas urbanas y rurales son diferentes.",
        "decision": f"Se rechaza H0 (p = {p_val:.3e} < 0.05). Diferencia significativa." if p_val < 0.05 else f"No se rechaza H0 (p = {p_val:.3f} > 0.05).",
        "effect_size": {
            "cohen_d": float(cohens_d),
            "interpretation": "Efecto pequeño" if cohens_d < 0.5 else "Efecto mediano" if cohens_d < 0.8 else "Efecto grande"
        }
    }

    return {
        "statistic": float(t_stat),
        "p_value": float(p_val),
        "means": means,
        "std_devs": stds,
        "sample_sizes": ns,
        "interpretation": interpretation
    }