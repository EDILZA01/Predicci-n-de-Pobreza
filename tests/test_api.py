"""
Pruebas Unitarias y de Integración para la API REST de Inferencia (FastAPI)
===========================================================================
FASE 6: Validación de contratos OpenAPI, healthcheck, estructura de inferencia
y captura de errores de validación con Pydantic (HTTP 422).
"""

from typing import Any, Dict
from fastapi.testclient import TestClient
import pytest

from api.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Verifica que el endpoint raíz responda con código 200 y metadatos correctos."""
    response = client.get("/")
    assert response.status_code == 200
    data: Dict[str, Any] = response.json()
    assert data["service"] == "ENAHO Poverty Prediction API"
    assert data["status"] == "online"
    assert "version" in data


def test_healthcheck() -> None:
    """
    Verifica el endpoint GET /health:
      - Código HTTP 200.
      - JSON con status == 'healthy'.
      - model_loaded is True.
    """
    response = client.get("/health")
    assert response.status_code == 200

    data: Dict[str, Any] = response.json()
    assert data.get("status") == "healthy", f"Se esperaba status 'healthy', recibido: {data.get('status')}"
    assert data.get("model_loaded") is True, "El artefacto del modelo debe estar cargado en memoria (model_loaded=True)."
    assert data.get("version") == "1.0.0"


def test_prediction_endpoint_structure() -> None:
    """
    Verifica el endpoint POST /predict con un payload representativo válido:
      - Código HTTP 200.
      - Presencia de claves 'prediction', 'status', 'poverty_probability', 'risk_level'.
      - prediction en {0, 1}.
      - 0.0 <= poverty_probability <= 1.0.
      - risk_level en ['Low', 'Medium', 'High'].
    """
    valid_payload: Dict[str, Any] = {
        "DOMINIO": 4,
        "ESTRATO": 4,
        "MIEPERHO": 5,
        "PERCEPHO": 1,
        "ESTRSOCIAL": 5,
        "SG42": 80.0
    }

    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200, f"Fallo al invocar /predict. Detalle: {response.text}"

    data: Dict[str, Any] = response.json()

    # Comprobación de claves obligatorias en el contrato
    for expected_key in ["prediction", "status", "poverty_probability", "risk_level"]:
        assert expected_key in data, f"Clave esperada '{expected_key}' no encontrada en la respuesta."

    # Validación de tipos y rangos de las respuestas
    prediction = data["prediction"]
    status_label = data["status"]
    poverty_prob = data["poverty_probability"]
    risk_level = data["risk_level"]

    assert prediction in [0, 1], f"La predicción debe ser 0 o 1, recibida: {prediction}"
    assert status_label in ["Non-Poor", "Vulnerable/Poverty"], f"Diagnóstico inesperado: {status_label}"
    assert isinstance(poverty_prob, float), "poverty_probability debe ser un flotante."
    assert 0.0 <= poverty_prob <= 1.0, f"poverty_probability fuera de rango [0, 1]: {poverty_prob}"
    assert risk_level in ["Low", "Medium", "High"], f"Nivel de riesgo inválido: {risk_level}"


def test_prediction_validation_error() -> None:
    """
    Verifica que datos fuera de los rangos lógicos permitidos por Pydantic
    (ej. MIEPERHO < 1, ESTRSOCIAL > 6, DOMINIO > 8) sean interceptados
    retornando código HTTP 422 (Unprocessable Entity).
    """
    # Caso 1: MIEPERHO negativo
    invalid_payload_1: Dict[str, Any] = {
        "DOMINIO": 4,
        "ESTRATO": 4,
        "MIEPERHO": -2,
        "PERCEPHO": 1,
        "ESTRSOCIAL": 5,
        "SG42": 80.0
    }
    response_1 = client.post("/predict", json=invalid_payload_1)
    assert response_1.status_code == 422, f"Se esperaba 422 para MIEPERHO=-2, obtenido: {response_1.status_code}"

    # Caso 2: ESTRSOCIAL fuera de rango (10 > 6)
    invalid_payload_2: Dict[str, Any] = {
        "DOMINIO": 4,
        "ESTRATO": 4,
        "MIEPERHO": 4,
        "PERCEPHO": 1,
        "ESTRSOCIAL": 10,
        "SG42": 80.0
    }
    response_2 = client.post("/predict", json=invalid_payload_2)
    assert response_2.status_code == 422, f"Se esperaba 422 para ESTRSOCIAL=10, obtenido: {response_2.status_code}"

    # Caso 3: Tipo de dato no numérico en SG42
    invalid_payload_3: Dict[str, Any] = {
        "DOMINIO": 4,
        "ESTRATO": 4,
        "MIEPERHO": 4,
        "PERCEPHO": 1,
        "ESTRSOCIAL": 5,
        "SG42": "invalido"
    }
    response_3 = client.post("/predict", json=invalid_payload_3)
    assert response_3.status_code == 422, f"Se esperaba 422 para SG42='invalido', obtenido: {response_3.status_code}"
