"""
Esquemas de Validación Pydantic - ENAHO Poverty Prediction API
=============================================================
FASE 4: Definición de contratos de datos para validación estricta de entradas
y serialización de respuestas en el microservicio de inferencia en tiempo real.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PovertyPredictionRequest(BaseModel):
    """
    Contrato de datos de entrada para la estimación de pobreza de un hogar.
    Valida estrictamente los rangos de las 6 características estructurales de ENAHO.
    """
    DOMINIO: int = Field(
        ...,
        ge=1,
        le=8,
        description="Dominio geográfico INEI (1: Costa Norte, 2: Costa Centro, 3: Costa Sur, 4: Sierra Norte, 5: Sierra Centro, 6: Sierra Sur, 7: Selva, 8: Lima Metropolitana)"
    )
    ESTRATO: int = Field(
        ...,
        ge=1,
        le=8,
        description="Estrato geográfico según tamaño poblacional y área urbana/rural (1-8)"
    )
    MIEPERHO: int = Field(
        ...,
        ge=1,
        le=30,
        description="Miembros presentes en el hogar (1-30)"
    )
    PERCEPHO: int = Field(
        ...,
        ge=0,
        le=30,
        description="Perceptores de ingresos del hogar (0-30)"
    )
    ESTRSOCIAL: int = Field(
        ...,
        ge=1,
        le=6,
        description="Estrato socioeconómico 1 a 6 (1: Alto, 2: Medio Alto, 3: Medio, 4: Medio Bajo, 5: Bajo, 6: Muy Bajo)"
    )
    SG42: float = Field(
        ...,
        ge=0.0,
        description="Gasto imputado por alquiler en Soles (S/.)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "DOMINIO": 4,
                "ESTRATO": 4,
                "MIEPERHO": 5,
                "PERCEPHO": 1,
                "ESTRSOCIAL": 5,
                "SG42": 80.0
            }
        }
    }


class PovertyPredictionResponse(BaseModel):
    """
    Contrato de datos de salida para la inferencia de vulnerabilidad y pobreza.
    """
    prediction: int = Field(
        ...,
        description="Predicción binaria: 0 (No pobre) o 1 (Vulnerabilidad / Pobreza)"
    )
    status: str = Field(
        ...,
        description="Diagnóstico textual: 'Non-Poor' si prediction == 0, 'Vulnerable/Poverty' si prediction == 1"
    )
    poverty_probability: float = Field(
        ...,
        description="Probabilidad estimada de pobreza redondeada a 4 decimales"
    )
    risk_level: str = Field(
        ...,
        description="Nivel de riesgo clasificado según umbrales: 'Low' (<0.35), 'Medium' (0.35-0.65), 'High' (>0.65)"
    )


class HealthResponse(BaseModel):
    """
    Contrato de datos para el endpoint de verificación de salud del microservicio.
    """
    status: str = Field("healthy", description="Estado operativo del servicio")
    model_loaded: bool = Field(..., description="Indica si el artefacto del modelo está cargado en memoria")
    version: str = Field("1.0.0", description="Versión de la API")


# Alias de retrocompatibilidad
HouseholdFeatures = PovertyPredictionRequest
PredictionResponse = PovertyPredictionResponse
