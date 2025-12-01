from fastapi import APIRouter
from app.services.data_service import cargar_y_analizar_datos   

router = APIRouter()

@router.get("/analyze-results")
def get_analysis_results():
    resultados = cargar_y_analizar_datos()
    return resultados