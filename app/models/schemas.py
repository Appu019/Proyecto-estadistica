from pydantic import BaseModel
from typing import List, Optional

class MesaData(BaseModel):
    PDC: int
    LIBRE: int
    CodigoCircunscripcionU: Optional[int] = None
    CodigoCircunscripcionE: Optional[int] = None
    Votantes: Optional[int] = None
    NombreDepartamento: Optional[str] = None

class MesaList(BaseModel):
    data: List[MesaData]

class ChiSquareResult(BaseModel):
    chi2: float
    p_value: float
    dof: int
    expected: List[List[float]]
    contingency_table: Optional[dict] = None
    interpretation: Optional[dict] = None

class TTestResult(BaseModel):
    statistic: float
    p_value: float
    means: Optional[dict] = None
    std_devs: Optional[dict] = None
    sample_sizes: Optional[dict] = None
    interpretation: Optional[dict] = None