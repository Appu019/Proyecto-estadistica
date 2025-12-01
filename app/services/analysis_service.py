from app.models.schemas import MesaList, ChiSquareResult, TTestResult
from app.utils.data_processing import procesar_datos_mesa
from app.utils.statistics import chi_square_test_from_df, t_test_from_df

def analizar_chi_square(data: MesaList) -> ChiSquareResult:
    df = procesar_datos_mesa([m.dict() for m in data.data])
    result = chi_square_test_from_df(df)
    return ChiSquareResult(**result)

def analizar_t_test(data: MesaList) -> TTestResult:
    df = procesar_datos_mesa([m.dict() for m in data.data])
    result = t_test_from_df(df)
    return TTestResult(**result)