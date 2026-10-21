"""
Pruebas Unitarias para el Pipeline de Datos y Calidad del Dataset
================================================================
FASE 6: Validación rigurosa de integridad, ausencia de nulos e infinitos,
conformidad de columnas estructurales y rangos lógicos socioeconómicos.
"""

from pathlib import Path
from typing import List, Set
import numpy as np
import pandas as pd
import pytest

from src.preprocess import clean_currency_series

PROCESSED_DATA_PATH = Path("data/processed/enaho_processed.csv")
EXPECTED_COLUMNS: List[str] = [
    "DOMINIO",
    "ESTRATO",
    "MIEPERHO",
    "PERCEPHO",
    "ESTRSOCIAL",
    "SG42",
    "target"
]


def test_processed_data_file_exists() -> None:
    """Valida la existencia física del archivo CSV procesado en disco."""
    assert PROCESSED_DATA_PATH.is_file(), (
        f"El archivo procesado no existe en: {PROCESSED_DATA_PATH.resolve()}. "
        "Ejecute 'python src/preprocess.py' para generarlo."
    )


def test_processed_data_schema_and_column_integrity() -> None:
    """Verifica que el dataset contenga exactamente las 7 columnas requeridas y en el orden esperado."""
    assert PROCESSED_DATA_PATH.is_file(), "El archivo procesado debe existir para validar el esquema."
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Validar que existan exactamente las 7 columnas requeridas
    assert list(df.columns) == EXPECTED_COLUMNS, (
        f"Las columnas no coinciden exactamente. Esperadas: {EXPECTED_COLUMNS}, Obtenidas: {list(df.columns)}"
    )
    assert len(df.columns) == 7, f"Se esperaban exactamente 7 columnas, se encontraron {len(df.columns)}."
    assert len(df) > 0, "El dataset procesado no debe estar vacío."


def test_processed_data_no_nulls_or_infs() -> None:
    """Verifica que no existan valores nulos, NaN ni valores numéricos infinitos en el dataset."""
    assert PROCESSED_DATA_PATH.is_file(), "El archivo procesado debe existir."
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Comprobación estricta de nulos
    total_nulls = int(df.isna().sum().sum())
    assert total_nulls == 0, f"Se encontraron {total_nulls} valores nulos/NaN en el dataset procesado."

    # Comprobación estricta de valores infinitos
    numeric_data = df.select_dtypes(include=[np.number]).values
    total_infs = int(np.isinf(numeric_data).sum())
    assert total_infs == 0, f"Se encontraron {total_infs} valores infinitos en el dataset procesado."


def test_target_binary_integrity() -> None:
    """Verifica que la variable dependiente 'target' sea estrictamente binaria {0, 1}."""
    assert PROCESSED_DATA_PATH.is_file(), "El archivo procesado debe existir."
    df = pd.read_csv(PROCESSED_DATA_PATH)

    unique_target_values: Set[int] = set(df["target"].unique())
    assert unique_target_values.issubset({0, 1}), (
        f"La columna 'target' contiene valores no binarios: {unique_target_values}"
    )
    assert 0 in unique_target_values and 1 in unique_target_values, (
        "El target debe contener ambas clases (0: No Pobre, 1: Pobreza/Vulnerabilidad)."
    )


def test_socioeconomic_feature_logical_ranges() -> None:
    """Verifica que todas las variables cumplan con los rangos lógicos socioeconómicos del INEI."""
    assert PROCESSED_DATA_PATH.is_file(), "El archivo procesado debe existir."
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Rangos lógicos socioeconómicos
    assert (df["MIEPERHO"] >= 1).all(), "MIEPERHO debe tener al menos 1 miembro por hogar."
    assert (df["PERCEPHO"] >= 0).all(), "PERCEPHO debe ser mayor o igual a 0 perceptores."
    assert (df["SG42"] >= 0.0).all(), "SG42 debe ser un gasto positivo o cero."
    assert df["DOMINIO"].isin(range(1, 9)).all(), "DOMINIO debe estar en el rango [1, 8]."
    assert df["ESTRATO"].isin(range(1, 9)).all(), "ESTRATO debe estar en el rango [1, 8]."
    assert df["ESTRSOCIAL"].isin(range(1, 7)).all(), "ESTRSOCIAL debe estar en el rango [1, 6]."


def test_clean_currency_series_behavior() -> None:
    """Valida la función auxiliar de saneamiento de monedas con comas y espacios."""
    raw_series = pd.Series([" 123,45 ", "0,0", "1500,75", " ", None, "nan"])
    cleaned = clean_currency_series(raw_series)

    assert cleaned.iloc[0] == pytest.approx(123.45)
    assert cleaned.iloc[1] == pytest.approx(0.0)
    assert cleaned.iloc[2] == pytest.approx(1500.75)
    assert cleaned.iloc[3] == pytest.approx(0.0)
    assert cleaned.iloc[4] == pytest.approx(0.0)
    assert cleaned.iloc[5] == pytest.approx(0.0)
