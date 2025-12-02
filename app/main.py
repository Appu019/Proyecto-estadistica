from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import analysis, data
from app.services.data_service import cargar_y_analizar_datos
from app.services.data_service import get_zone_distribution
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Análisis Estadístico Electoral")

# Configure CORS to allow any origin/method/header (development convenience)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# Montar la carpeta de frontend como archivos estáticos
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(analysis.router, prefix="/analyze", tags=["análisis"])
app.include_router(data.router, prefix="/data", tags=["datos"])

@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def read_root():
    """Redirige al frontend (no aparece en la documentación de la API)."""
    return "/static/index.html"

@app.get("/api/results")
def get_analysis_results_for_postman():
    """
    Endpoint dedicado para Postman o clientes HTTP.
    Devuelve los resultados del análisis estadístico en formato JSON.
    """
    return cargar_y_analizar_datos()



@router.get("/zone-distribution")
def zone_distribution():
    return get_zone_distribution()

# Api publica para consumo desde JS
# http://127.0.0.1:8000/data/analyze-results