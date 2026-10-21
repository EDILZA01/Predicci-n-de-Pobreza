"""
Módulo de Ingesta, Preprocesamiento y Auditoría Estadística - ENAHO Poverty Prediction
=======================================================================================
FASE 2: Pipeline de Ingeniería de Datos y Auditoría Estadística Vectorizada.
Realiza la ingesta de microdatos crudos (ENAHO Sumaria 2025 - INEI), limpieza y tipado
de variables estructurales, construcción del target binario de pobreza y cálculo de momentos
estadísticos analíticos mediante álgebra matricial y vectorial con NumPy.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def clean_currency_series(series: pd.Series) -> pd.Series:
    """
    Limpia y estandariza una serie con formato numérico o monetario a float64.

    Reemplaza comas decimales por puntos, elimina espacios en blanco y rellena
    valores nulos o cadenas vacías con 0.0.

    Parameters
    ----------
    series : pd.Series
        Serie con datos numéricos o representaciones en texto.

    Returns
    -------
    pd.Series
        Serie depurada convertida a tipo float64 con nulos imputados a 0.0.
    """
    cleaned = series.astype(str).str.strip().str.replace(",", ".", regex=False)
    cleaned = cleaned.replace({"nan": None, "None": None, "": None})
    numeric_series = pd.to_numeric(cleaned, errors="coerce")
    return numeric_series.fillna(0.0).astype(float)


def load_raw_data(filepath: Path | str) -> Tuple[pd.DataFrame, str]:
    """
    Carga el dataset crudo identificando automáticamente el delimitador (';' o ',').

    Parameters
    ----------
    filepath : Path | str
        Ruta del archivo CSV de entrada.

    Returns
    -------
    Tuple[pd.DataFrame, str]
        Tupla con el DataFrame cargado y el delimitador detectado.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Archivo de entrada no encontrado en: {path.resolve()}")

    with open(path, "r", encoding="latin1") as file_handler:
        header_sample = file_handler.readline()

    delimiter = ";" if header_sample.count(";") >= header_sample.count(",") else ","
    df = pd.read_csv(path, sep=delimiter, encoding="latin1", low_memory=False)
    return df, delimiter


def compute_univariate_stats(x: np.ndarray) -> Dict[str, float]:
    """
    Calcula analíticamente los momentos univariados mediante formulación vectorial:
      * Media: mean = np.sum(x) / len(x)
      * Centrado respecto a la media: dx = x - np.mean(x)
      * Varianza: variance = np.mean(dx * dx)
      * Desviación estándar: stdev = np.sqrt(variance)
      * Extremos: Mínimo y Máximo

    Parameters
    ----------
    x : np.ndarray
        Vector unidimensional numérico.

    Returns
    -------
    Dict[str, float]
        Diccionario con las estadísticas univariadas.
    """
    n = len(x)
    mean = float(np.sum(x) / n)
    dx = x - np.mean(x)
    variance = float(np.mean(dx * dx))
    stdev = float(np.sqrt(variance))
    min_val = float(np.min(x))
    max_val = float(np.max(x))

    return {
        "mean": mean,
        "variance": variance,
        "stdev": stdev,
        "min": min_val,
        "max": max_val,
    }


def compute_bivariate_stats(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
    """
    Calcula analíticamente los momentos bivariados mediante formulación vectorial:
      * Centrado en x: dx = x - np.mean(x)
      * Centrado en y: dy = y - np.mean(y)
      * Desviación estándar x: stdev_x = np.sqrt(np.mean(dx * dx))
      * Desviación estándar y: stdev_y = np.sqrt(np.mean(dy * dy))
      * Covarianza muestral: covariance = np.mean(dx * dy)
      * Correlación de Pearson: r = covariance / (stdev_x * stdev_y)

    Parameters
    ----------
    x : np.ndarray
        Vector unidimensional de la variable predictora.
    y : np.ndarray
        Vector unidimensional del target binario.

    Returns
    -------
    Dict[str, float]
        Diccionario con covarianza y coeficiente de Pearson.
    """
    dx = x - np.mean(x)
    dy = y - np.mean(y)
    stdev_x = np.sqrt(np.mean(dx * dx))
    stdev_y = np.sqrt(np.mean(dy * dy))
    covariance = float(np.mean(dx * dy))

    if stdev_x * stdev_y != 0.0:
        pearson_r = float(covariance / (stdev_x * stdev_y))
    else:
        pearson_r = 0.0

    return {
        "covariance": covariance,
        "pearson_r": pearson_r,
    }


def run_preprocessing(
    input_path: Path | str = "data/raw/Sumaria-2025.csv",
    output_path: Path | str = "data/processed/enaho_processed.csv"
) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de la Fase 2: lectura, limpieza, tipado,
    auditoría estadística univariada/bivariada y exportación del dataset final.

    Parameters
    ----------
    input_path : Path | str, optional
        Ruta del archivo CSV crudo de entrada.
    output_path : Path | str, optional
        Ruta destino del dataset procesado.

    Returns
    -------
    pd.DataFrame
        DataFrame preprocesado final.
    """
    input_file = Path(input_path)
    output_file = Path(output_path)

    # =========================================================================
    # PASO 1: Confirmación de carga de datos brutos y dimensiones iniciales
    # =========================================================================
    print("=" * 100)
    print("PASO 1: CONFIRMACIÓN DE CARGA DE DATOS BRUTOS Y DIMENSIONES INICIALES")
    print("=" * 100)
    print(f"Ruta de entrada especificada: {input_file.resolve()}")

    df_raw, delimiter_used = load_raw_data(input_file)
    initial_rows, initial_cols = df_raw.shape
    print(f"Delimitador detectado: '{delimiter_used}' | Codificación: 'latin1' | low_memory: False")
    print(f"Dimensiones de entrada leídas: {initial_rows:,} filas y {initial_cols:,} columnas.")

    # Validación de existencia de columnas requeridas
    structural_features: List[str] = ["DOMINIO", "ESTRATO", "MIEPERHO", "PERCEPHO", "ESTRSOCIAL", "SG42"]
    target_source_col: str = "POBREZA"
    all_required_cols = structural_features + [target_source_col]

    missing_cols = [c for c in all_required_cols if c not in df_raw.columns]
    if missing_cols:
        raise KeyError(f"Columnas indispensables no encontradas en el dataset crudo: {missing_cols}")

    print("Columnas estructurales y variable de pobreza identificadas exitosamente.")

    # 1. Target binario: [1, 2] -> 1 (Pobreza extrema / no extrema), 3 -> 0 (No pobre)
    # Descartar registros con valores nulos o fuera del rango [1, 3] en POBREZA
    valid_poverty_mask = df_raw[target_source_col].notna() & df_raw[target_source_col].isin([1, 2, 3])
    discarded_poverty = initial_rows - int(valid_poverty_mask.sum())
    df_clean = df_raw.loc[valid_poverty_mask].copy()

    if discarded_poverty > 0:
        print(f"Registros descartados por valor inválido o ausente en '{target_source_col}': {discarded_poverty:,}")
    else:
        print(f"Registros validados en '{target_source_col}': {len(df_clean):,} (100% conformes en rango [1, 3]).")

    poverty_map = {1: 1, 2: 1, 3: 0}
    target_series = df_clean[target_source_col].map(poverty_map).astype(int)

    # 2. Extracción y casteo de las 6 características estructurales
    processed_df = pd.DataFrame()
    for int_col in ["DOMINIO", "ESTRATO", "MIEPERHO", "PERCEPHO", "ESTRSOCIAL"]:
        processed_df[int_col] = pd.to_numeric(df_clean[int_col], errors="coerce")

    # Limpieza de SG42 (alquiler imputado)
    processed_df["SG42"] = clean_currency_series(df_clean["SG42"])

    # Eliminación de cualquier fila residual con valores NaN en estas 6 columnas
    rows_before_drop = len(processed_df)
    processed_df.dropna(subset=structural_features, inplace=True)
    residual_dropped = rows_before_drop - len(processed_df)

    if residual_dropped > 0:
        print(f"Filas residuales descartadas por valores NaN en características estructurales: {residual_dropped:,}")
    else:
        print(f"Integridad de características estructurales: 0 filas residuales con NaN.")

    # Casteo estricto a tipos enteros
    for int_col in ["DOMINIO", "ESTRATO", "MIEPERHO", "PERCEPHO", "ESTRSOCIAL"]:
        processed_df[int_col] = processed_df[int_col].astype(int)

    # Incorporación del target binario alineado
    processed_df["target"] = target_series.loc[processed_df.index]

    print(f"Observaciones estructuradas consolidadas: {len(processed_df):,} registros.\n")

    # =========================================================================
    # PASO 2: Tabla de Auditoría Estadística Univariada
    # =========================================================================
    print("=" * 100)
    print("PASO 2: TABLA DE AUDITORÍA ESTADÍSTICA UNIVARIADA (MOMENTOS VECTORIZADOS EN NUMPY)")
    print("=" * 100)
    header_univ = f"{'Variable':<14} {'Media':>14} {'Varianza':>16} {'Desv. Estándar':>16} {'Mínimo':>14} {'Máximo':>14}"
    print(header_univ)
    print("-" * 100)

    for col in structural_features:
        x_col = processed_df[col].to_numpy(dtype=float)
        stats = compute_univariate_stats(x_col)
        print(
            f"{col:<14} "
            f"{stats['mean']:>14.4f} "
            f"{stats['variance']:>16.4f} "
            f"{stats['stdev']:>16.4f} "
            f"{stats['min']:>14.4f} "
            f"{stats['max']:>14.4f}"
        )
    print("-" * 100 + "\n")

    # =========================================================================
    # PASO 3: Tabla de Auditoría Estadística Bivariada y Balance de Clases
    # =========================================================================
    print("=" * 100)
    print("PASO 3: TABLA DE AUDITORÍA ESTADÍSTICA BIVARIADA Y BALANCE DE CLASES")
    print("=" * 100)
    header_biv = f"{'Variable':<14} {'Covarianza (c/ target)':>26} {'Correlación Pearson (r)':>26}   {'Interpretación':<20}"
    print(header_biv)
    print("-" * 100)

    y_target = processed_df["target"].to_numpy(dtype=float)
    for col in structural_features:
        x_feat = processed_df[col].to_numpy(dtype=float)
        biv_metrics = compute_bivariate_stats(x_feat, y_target)
        r_corr = biv_metrics["pearson_r"]

        if abs(r_corr) < 0.10:
            interpretacion = "Asociación muy leve"
        elif r_corr > 0:
            interpretacion = "Asociación positiva"
        else:
            interpretacion = "Asociación inversa (protectora)"

        print(
            f"{col:<14} "
            f"{biv_metrics['covariance']:>26.6f} "
            f"{biv_metrics['pearson_r']:>26.6f}   "
            f"{interpretacion:<20}"
        )
    print("-" * 100)

    # Balance de Clases
    count_0 = int(np.sum(y_target == 0))
    count_1 = int(np.sum(y_target == 1))
    total_samples = len(y_target)
    pct_0 = (count_0 / total_samples) * 100.0
    pct_1 = (count_1 / total_samples) * 100.0
    ratio = count_0 / count_1 if count_1 > 0 else 0.0

    print("\nBalance de Clases (Variable 'target'):")
    print(f"  - Clase 0 [No pobre]:                  {count_0:>8,} hogares ({pct_0:>6.2f}%)")
    print(f"  - Clase 1 [Pobreza / Vulnerabilidad]:   {count_1:>8,} hogares ({pct_1:>6.2f}%)")
    print(f"  - Total Muestral Evaluado:             {total_samples:>8,} hogares (100.00%)")
    print(f"  - Relación de Desbalance (Clase 0/1):    {ratio:>7.2f} : 1\n")

    # =========================================================================
    # PASO 4: Resumen y Reporte Final de Integridad
    # =========================================================================
    print("=" * 100)
    print("PASO 4: RESUMEN Y REPORTE FINAL DE INTEGRIDAD")
    print("=" * 100)

    nan_total = int(processed_df.isna().sum().sum())
    inf_total = int(np.isinf(processed_df.to_numpy(dtype=float)).sum())

    print(f"[AUDITORÍA INTEGRIDAD] Total de valores nulos (NaN) detectados:      {nan_total}")
    print(f"[AUDITORÍA INTEGRIDAD] Total de valores infinitos (Inf) detectados:  {inf_total}")

    if nan_total != 0 or inf_total != 0:
        raise ValueError("Error de integridad: Se detectaron valores nulos o infinitos no permitidos.")

    # Exportación
    output_file.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(output_file, sep=",", index=False, encoding="utf-8")

    final_rows, final_cols = processed_df.shape
    print(f"[EXPORTACIÓN EXITOSA] Archivo generado en: {output_file.resolve()}")
    print(f"[DIMENSIONES FINALES] Filas: {final_rows:,} | Columnas: {final_cols}")
    print(f"[COLUMNAS PROCESADAS] {list(processed_df.columns)}")
    print("=" * 100 + "\n")

    return processed_df


if __name__ == "__main__":
    run_preprocessing()
