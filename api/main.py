"""
Microservicio REST de Inferencia con FastAPI - ENAHO Poverty Prediction API
===========================================================================
FASE 4: Exposición de endpoints para inferencia en tiempo real, verificación
de salud y documentación OpenAPI interactiva.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, Optional
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    HealthResponse,
    PovertyPredictionRequest,
    PovertyPredictionResponse,
)

MODEL_PATH = Path("models/poverty_model.joblib")
ml_models: Dict[str, Any] = {}


def get_or_load_model() -> Optional[Any]:
    """
    Recupera el modelo de la memoria en caché o lo carga directamente
    desde el artefacto serializado si no ha sido inicializado.
    """
    model = ml_models.get("pipeline")
    if model is None and MODEL_PATH.is_file():
        try:
            model = joblib.load(MODEL_PATH)
            ml_models["pipeline"] = model
            print(f"[INFO] Modelo cargado exitosamente desde: {MODEL_PATH.resolve()}")
        except Exception as exc:
            print(f"[ERROR] Error al cargar el modelo serializado: {exc}")
            model = None
    return model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación cargando el modelo entrenado
    en memoria al inicio y liberando recursos al finalizar.
    """
    get_or_load_model()
    yield
    ml_models.clear()


app = FastAPI(
    title="ENAHO Poverty Prediction API",
    description="Microservicio de producción para la estimación del riesgo y predicción de vulnerabilidad socioeconómica y pobreza en hogares del Perú (INEI ENAHO).",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Metadatos"])
def root():
    """Endpoint raíz con metadatos y enlaces de documentación."""
    return {
        "service": "ENAHO Poverty Prediction API",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/health", response_model=HealthResponse, tags=["Monitoreo"])
def health_check():
    """
    Endpoint de verificación de estado y confirmación del modelo cargado en memoria.
    """
    model = get_or_load_model()
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        version="1.0.0"
    )


@app.post("/predict", response_model=PovertyPredictionResponse, tags=["Inferencia"])
def predict_poverty(request: PovertyPredictionRequest):
    """
    Estima la probabilidad de pobreza y condición de vulnerabilidad para un hogar dado.

    Recibe las 6 características estructurales validadas, ejecuta la inferencia
    con el modelo serializado y clasifica el nivel de riesgo:
      * Low: Probabilidad < 0.35
      * Medium: 0.35 <= Probabilidad <= 0.65
      * High: Probabilidad > 0.65
    """
    model = get_or_load_model()
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El artefacto del modelo no se encuentra disponible. Ejecute el script 'src/train.py'."
        )

    # Conversión a DataFrame preservando el orden exacto de columnas de entrenamiento
    ordered_columns = ["DOMINIO", "ESTRATO", "MIEPERHO", "PERCEPHO", "ESTRSOCIAL", "SG42"]
    data_dict = {col: [getattr(request, col)] for col in ordered_columns}
    input_df = pd.DataFrame(data_dict)

    try:
        prediction = int(model.predict(input_df)[0])

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(input_df)[0][1])
        else:
            probability = float(prediction)

        probability = round(probability, 4)

        # Mapeo de diagnóstico textual
        status_label = "Vulnerable/Poverty" if prediction == 1 else "Non-Poor"

        # Clasificación de nivel de riesgo
        if probability < 0.35:
            risk_level = "Low"
        elif probability <= 0.65:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return PovertyPredictionResponse(
            prediction=prediction,
            status=status_label,
            poverty_probability=probability,
            risk_level=risk_level
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el proceso de inferencia: {str(exc)}"
        )
