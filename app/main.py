from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import analysis, data

app = FastAPI(title="API de Análisis Estadístico Electoral")

# Montar la carpeta de frontend como archivos estáticos
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(analysis.router, prefix="/analyze", tags=["análisis"])
app.include_router(data.router, prefix="/data", tags=["datos"])

@app.get("/")
def read_root():
    # Redirigir al index.html del frontend
    return {"message": "Ir a /static/index.html para ver el frontend"}