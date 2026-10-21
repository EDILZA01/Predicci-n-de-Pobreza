"""
Módulo de Evaluación Rigurosa y Generación de Reportes - ENAHO Poverty Prediction
================================================================================
FASE 3: Evaluación de Desempeño sobre Datos de Prueba No Vistos (Hold-out 30%).
Calcula todas las métricas formales de las diapositivas de clase:
- Matriz de Confusión: VP, VN, FP, FN
- Precisión: VP / (VP + FP)
- Recall (Sensibilidad): VP / (VP + FN)
- Especificidad: VN / (VN + FP) = 1 - TFP
- Tasa de error positiva (err+): FN / (VP + FN)
- Tasa de error negativa (err-): FP / (VN + FP)
- F1-Score: 2 * (prec * recall) / (prec + recall)
- Accuracy y Área Bajo la Curva ROC (ROC-AUC)
Genera artefactos visuales en `reports/figures/`:
- confusion_matrix.png
- roc_curve.png
"""

from pathlib import Path
from typing import Any, Dict, Tuple
import joblib
import matplotlib
matplotlib.use("Agg")  # Backend no interactivo para entornos headless / producción
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)


def load_evaluation_artifacts(
    model_path: Path | str = "models/poverty_model.joblib",
    x_test_path: Path | str = "data/processed/X_test.csv",
    y_test_path: Path | str = "data/processed/y_test.csv"
) -> Tuple[Any, pd.DataFrame, pd.Series]:
    """
    Carga el pipeline entrenado y los datos de prueba independientes.

    Parameters
    ----------
    model_path : Path | str
        Ruta al archivo joblib del modelo.
    x_test_path : Path | str
        Ruta al archivo CSV con las características de prueba.
    y_test_path : Path | str
        Ruta al archivo CSV con el target de prueba.

    Returns
    -------
    Tuple[Any, pd.DataFrame, pd.Series]
        Pipeline entrenado, matriz X_test y vector y_test.
    """
    m_file = Path(model_path)
    x_file = Path(x_test_path)
    y_file = Path(y_test_path)

    if not m_file.is_file():
        raise FileNotFoundError(f"Modelo serializado no encontrado en: {m_file.resolve()}. Ejecutar 'src/train.py'.")
    if not x_file.is_file() or not y_file.is_file():
        raise FileNotFoundError(f"Datos de prueba no encontrados en: {x_file.resolve()} o {y_file.resolve()}.")

    model = joblib.load(m_file)
    X_test = pd.read_csv(x_file)
    y_test = pd.read_csv(y_file)["target"]

    return model, X_test, y_test


def compute_slide_metrics(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray | None = None
) -> Dict[str, float]:
    """
    Calcula exhaustivamente todas las métricas de clase formalizadas en las diapositivas:
      * Matriz de Confusión: VN, FP, FN, VP
      * Precisión: prec = VP / (VP + FP)
      * Recall: recall = VP / (VP + FN)
      * Especificidad: espec = VN / (VN + FP)
      * Tasa de error positiva: err+ = FN / (VP + FN)
      * Tasa de error negativa: err- = FP / (VN + FP)
      * F1-Score: 2 * (prec * recall) / (prec + recall)
      * Accuracy: (VP + VN) / Total
      * ROC-AUC

    Parameters
    ----------
    y_true : pd.Series | np.ndarray
        Etiquetas reales de prueba (0: No pobre, 1: Vulnerable/Pobre).
    y_pred : np.ndarray
        Etiquetas predichas binarias.
    y_proba : np.ndarray | None, optional
        Probabilidades estimadas para la clase positiva.

    Returns
    -------
    Dict[str, float]
        Métricas consolidadas.
    """
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = [float(val) for val in cm.ravel()]

    total = tn + fp + fn + tp

    # Fórmulas de diapositivas
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    espec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    err_plus = fn / (tp + fn) if (tp + fn) > 0 else 0.0
    err_minus = fp / (tn + fp) if (tn + fp) > 0 else 0.0
    f1 = 2 * (prec * recall) / (prec + recall) if (prec + recall) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0

    roc_auc = float(roc_auc_score(y_true, y_proba)) if y_proba is not None else 0.0

    metrics: Dict[str, float] = {
        "VN": tn,
        "FP": fp,
        "FN": fn,
        "VP": tp,
        "total": total,
        "precision": prec,
        "recall": recall,
        "especificidad": espec,
        "err_plus": err_plus,
        "err_minus": err_minus,
        "f1_score": f1,
        "accuracy": accuracy,
        "roc_auc": roc_auc
    }

    return metrics


def generate_visual_artifacts(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
    roc_auc: float,
    figures_dir: Path | str = "reports/figures"
) -> Tuple[Path, Path]:
    """
    Genera y guarda en disco los artefactos visuales: matriz de confusión y curva ROC.

    Parameters
    ----------
    y_true : pd.Series | np.ndarray
        Etiquetas reales.
    y_pred : np.ndarray
        Etiquetas predichas.
    y_proba : np.ndarray
        Probabilidades continuas para la clase 1.
    roc_auc : float
        Puntaje ROC-AUC calculado.
    figures_dir : Path | str
        Directorio donde se exportarán las imágenes.

    Returns
    -------
    Tuple[Path, Path]
        Rutas a confusion_matrix.png y roc_curve.png.
    """
    fig_dir = Path(figures_dir)
    fig_dir.mkdir(parents=True, exist_ok=True)

    cm_path = fig_dir / "confusion_matrix.png"
    roc_path = fig_dir / "roc_curve.png"

    # 1. Matriz de Confusión
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=["No Pobre (0)", "Vulnerable (1)"],
        cmap=plt.cm.Blues,
        values_format="d",
        ax=ax
    )
    ax.set_title("Matriz de Confusión - Conjunto de Prueba (30%)", fontsize=12, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(cm_path, dpi=300)
    plt.close(fig)

    # 2. Curva ROC
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.plot(fpr, tpr, color="#1f77b4", lw=2.5, label=f"Modelo Seleccionado (AUC = {roc_auc:.4f})")
    ax.plot([0, 1], [0, 1], color="#7f7f7f", lw=1.5, linestyle="--", label="Clasificador Aleatorio (AUC = 0.5000)")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("Tasa de Falsos Positivos (1 - Especificidad)", fontsize=11)
    ax.set_ylabel("Tasa de Verdaderos Positivos (Recall)", fontsize=11)
    ax.set_title("Curva ROC (Receiver Operating Characteristic)", fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="lower right", frameon=True)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(roc_path, dpi=300)
    plt.close(fig)

    return cm_path, roc_path


def evaluate_model_pipeline(
    model_path: Path | str = "models/poverty_model.joblib",
    x_test_path: Path | str = "data/processed/X_test.csv",
    y_test_path: Path | str = "data/processed/y_test.csv"
) -> Dict[str, float]:
    """
    Ejecuta el pipeline completo de evaluación sobre el split de prueba (30%).

    Parameters
    ----------
    model_path : Path | str
        Ruta al artefacto .joblib.
    x_test_path : Path | str
        Ruta a X_test.csv.
    y_test_path : Path | str
        Ruta a y_test.csv.

    Returns
    -------
    Dict[str, float]
        Diccionario con todas las métricas de clase calculadas.
    """
    print("=" * 105)
    print("FASE 3: EVALUACIÓN RIGUROSA DE RENDIMIENTO SOBRE DATOS NO VISTOS (30% TEST HOLD-OUT)")
    print("=" * 105)

    model, X_test, y_test = load_evaluation_artifacts(model_path, x_test_path, y_test_path)
    print(f"[CARGA] Modelo cargado desde: {Path(model_path).resolve()}")
    print(f"[CARGA] Datos de prueba cargados: {len(X_test):,} observaciones no vistas.\n")

    # Inferencia
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    # Métricas formales
    m = compute_slide_metrics(y_test, y_pred, y_proba)

    # Matriz de Confusión Tabular en Consola
    print("=" * 105)
    print("MATRIZ DE CONFUSIÓN (CONJUNTO DE PRUEBA INDEPENDIENTE)")
    print("=" * 105)
    print(f"{'':<25} | {'Predicho: No Pobre (0)':^26} | {'Predicho: Vulnerable (1)':^26} | {'Total Real':^14}")
    print("-" * 105)
    print(f"{'Real: No Pobre (0)':<25} | {int(m['VN']):^26,} | {int(m['FP']):^26,} | {int(m['VN'] + m['FP']):^14,}")
    print(f"{'Real: Vulnerable (1)':<25} | {int(m['FN']):^26,} | {int(m['VP']):^26,} | {int(m['FN'] + m['VP']):^14,}")
    print("-" * 105)
    print(f"{'Total Predicho':<25} | {int(m['VN'] + m['FN']):^26,} | {int(m['FP'] + m['VP']):^26,} | {int(m['total']):^14,}\n")

    # Reporte Formal con Fórmulas de Diapositivas
    print("=" * 105)
    print("REPORTE FORMAL DE MÉTRICAS DE CLASE (FÓRMULAS DIRECTAS DE DIAPOSITIVAS)")
    print("=" * 105)
    print(f"  * Verdaderos Positivos (VP):             {int(m['VP']):>8,}  [Hogares vulnerables clasificados correctamente]")
    print(f"  * Verdaderos Negativos (VN):             {int(m['VN']):>8,}  [Hogares no pobres clasificados correctamente]")
    print(f"  * Falsos Positivos (FP):                 {int(m['FP']):>8,}  [Hogares no pobres clasificados erróneamente]")
    print(f"  * Falsos Negativos (FN):                 {int(m['FN']):>8,}  [Hogares vulnerables clasificados erróneamente]")
    print("-" * 105)
    print(f"  * Precisión (Precision):                 {m['precision']:>8.4f}  (VP / [VP + FP])")
    print(f"  * Recall / Sensibilidad:                 {m['recall']:>8.4f}  (VP / [VP + FN])")
    print(f"  * Especificidad (Specificity):           {m['especificidad']:>8.4f}  (VN / [VN + FP] = 1 - TFP)")
    print(f"  * Tasa de Error Positiva (err+):         {m['err_plus']:>8.4f}  (FN / [VP + FN] = 1 - Recall)")
    print(f"  * Tasa de Error Negativa (err-):         {m['err_minus']:>8.4f}  (FP / [VN + FP] = 1 - Espec)")
    print(f"  * F1-Score (Media Armónica):             {m['f1_score']:>8.4f}  (2 * [Prec * Rec] / [Prec + Rec])")
    print(f"  * Exactitud Global (Accuracy):           {m['accuracy']:>8.4f}  ([VP + VN] / Total)")
    print(f"  * Área Bajo Curva ROC (ROC-AUC):         {m['roc_auc']:>8.4f}")
    print("=" * 105)

    # Generación y confirmación de figuras
    cm_path, roc_path = generate_visual_artifacts(y_test, y_pred, y_proba, m["roc_auc"])
    print("\n[ARTEFACTOS VISUALES EXPORTADOS]")
    print(f"  - Matriz de Confusión:  {cm_path.resolve()}")
    print(f"  - Curva ROC:            {roc_path.resolve()}")
    print("=" * 105 + "\n")

    return m


def main() -> None:
    """Función principal de ejecución del módulo de evaluación."""
    evaluate_model_pipeline()


if __name__ == "__main__":
    main()
