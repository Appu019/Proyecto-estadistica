from pydantic import BaseModel
from typing import List, Optional

class MesaData(BaseModel):
    PDC: int
    LIBRE: int
    CodigoCircunscripcionU: int
    CodigoCircunscripcionE: int
    NombreDepartamento: str

class MesaList(BaseModel):
    data: List[MesaData]

class ChiSquareResult(BaseModel):
    chi2: float
    p_value: float
    dof: int
    expected: List[List[float]]

class TTestResult(BaseModel):
    statistic: float
    p_value: float