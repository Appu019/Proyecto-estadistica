# Análisis Estadístico Electoral Bolivia 2025

Este proyecto analiza si existe una asociación entre el partido ganador en las mesas electorales (PDC o LIBRE) y el tipo de circunscripción (urbana vs. rural) en las **Elecciones Presidenciales de Bolivia 2025**. Se utilizan pruebas estadísticas como **Chi-cuadrado** y **T-Student**, implementadas en una API REST con **FastAPI**, y se visualizan los resultados mediante un frontend interactivo.

---

## 📁 Estructura del Proyecto
#
mi_proyecto_fastapi/
├── app/                     # Backend (FastAPI)
│   ├── main.py              # Punto de entrada de la API
│   ├── api/                 # Endpoints
│   ├── core/                # Configuración (CORS, variables, etc.)
│   ├── models/              # Modelos Pydantic
│   ├── services/            # Lógica del análisis estadístico
│   ├── utils/               # Funciones auxiliares
│   └── data/                # CSV con datos electorales
│
├── frontend/                # Interfaz (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── requirements.txt         # Dependencias
├── .env                     # Variables de entorno (opcional)
├── .gitignore
└── README.md

---

## ⚙️ Requisitos

- Python 3.8+
- `pip` (gestor de paquetes de Python)

---

## 🧪 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Proyecto-estadistica.git
cd Proyecto-estadistica
```

### 2. Crear un entorno virtual
Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```


Windows (CMD)

cmd
```bash
python -m venv .venv
.venv\Scripts\activate
```

Windows (PowerShell)

powershell
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

    💡 Si PowerShell bloquea la ejecución, ejecuta:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

    El archivo requirements.txt debe contener:

    1 fastapi
    2 uvicorn[standard]
    3 pandas
    4 scipy
    5 numpy
    6 pydantic

🚀 Ejecutar la Aplicación
Levantar el servidor de desarrollo


```bash
uvicorn app.main:app --reload
```
Acceder al frontend

    Interfaz de usuario con resultados del análisis:
    🔗 http://127.0.0.1:8000/static/index.html

📊 Análisis Implementado

    Prueba Chi-cuadrado de independencia:
    Evalúa si el partido ganador (PDC/LIBRE) es independiente del tipo de zona (urbana/rural).
    Prueba T-Student:
    Compara las medias de votos del PDC entre zonas urbanas y rurales.
    Clasificación automática:  
        Partido ganador por mesa: el que tiene más votos (PDC o LIBRE).
        Tipo de zona: urbana si CodigoCircunscripcionU > 0, de lo contrario rural.

📎 Datos

    Los datos se encuentran en: app/data/EG2025_2v_20251026_235911_6311285959951043675.csv
    El análisis se realiza solo con los registros de Bolivia.

📝 Autor

    Arcangel (GitHub: @Appu019)