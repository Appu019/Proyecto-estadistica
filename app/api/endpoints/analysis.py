from fastapi import APIRouter
from app.models.schemas import MesaList, ChiSquareResult, TTestResult
from app.services.analysis_service import analizar_chi_square, analizar_t_test

router = APIRouter()

@router.post("/chi-square", response_model=ChiSquareResult)
def chi_square_endpoint(data: MesaList):
    return analizar_chi_square(data)

@router.post("/t-test", response_model=TTestResult)
def t_test_endpoint(data: MesaList):
    return analizar_t_test(data)