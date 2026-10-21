"""
Módulo de Entrenamiento Supervisado y Optimización - ENAHO Poverty Prediction
=============================================================================
FASE 3: Selección de Modelos, Optimización de Hiperparámetros y Serialización.
Compara tres familias de clasificadores (Regresión Logística L2, k-NN y SVM RBF)
mediante validación cruzada estratificada (5-folds) optimizando el F1-score
sobre la clase vulnerable positiva para mitigar el desbalance de clases.
"""

from pathlib import Path
from typing import Any, Dict, List, Tuple
import time
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def load_and_split_data(
    data_path: Path | str = "data/processed/enaho_processed.csv",
    test_size: float = 0.30,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Carga el dataset procesado y realiza la partición estratificada Hold-out.

    Parameters
    ----------
    data_path : Path | str
        Ruta al archivo CSV con las características procesadas y el target.
    test_size : float
        Proporción asignada al conjunto de prueba no visto (por defecto 30%).
    random_state : int
        Semilla para garantizar reproducibilidad estricta.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]
        Conjuntos X_train, X_test, y_train, y_test.
    """
    file_path = Path(data_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Dataset procesado no encontrado en: {file_path.resolve()}")

    df = pd.read_csv(file_path)
    feature_cols = ["DOMINIO", "ESTRATO", "MIEPERHO", "PERCEPHO", "ESTRSOCIAL", "SG42"]
    target_col = "target"

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Exportar el split de prueba no visto para evaluación independiente
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    x_test_path = output_dir / "X_test.csv"
    y_test_path = output_dir / "y_test.csv"

    X_test.to_csv(x_test_path, index=False)
    y_test.to_frame(name="target").to_csv(y_test_path, index=False)

    print(f"[DATOS] Split Hold-out estratificado (70% train / 30% test):")
    print(f"        - Entrenamiento: {len(X_train):,} muestras")
    print(f"        - Prueba no vista: {len(X_test):,} muestras")
    print(f"[DATOS] Conjuntos de prueba exportados en: {x_test_path.resolve()} y {y_test_path.resolve()}\n")

    return X_train, X_test, y_train, y_test


def build_candidate_pipelines() -> Dict[str, Tuple[Pipeline, Dict[str, List[Any]]]]:
    """
    Define los pipelines de scikit-learn con StandardScaler y las mallas
    de hiperparámetros para los 3 algoritmos supervisados de la planificación oficial.

    Returns
    -------
    Dict[str, Tuple[Pipeline, Dict[str, List[Any]]]]
        Diccionario con nombre de modelo, pipeline y cuadrícula de parámetros.
    """
    models: Dict[str, Tuple[Pipeline, Dict[str, List[Any]]]] = {
        "Regresión Logística (Ridge L2)": (
            Pipeline([
                ("scaler", StandardScaler()),
                ("clf", LogisticRegression(
                    penalty="l2",
                    solver="lbfgs",
                    max_iter=1000,
                    random_state=42
                ))
            ]),
            {
                "clf__C": [0.01, 0.1, 1.0, 10.0]
            }
        ),
        "K-Nearest Neighbors (k-NN)": (
            Pipeline([
                ("scaler", StandardScaler()),
                ("clf", KNeighborsClassifier(metric="euclidean"))
            ]),
            {
                "clf__n_neighbors": [3, 5, 7, 9],
                "clf__weights": ["uniform", "distance"]
            }
        ),
        "Support Vector Machines (SVM RBF)": (
            Pipeline([
                ("scaler", StandardScaler()),
                ("clf", SVC(
                    kernel="rbf",
                    probability=True,
                    cache_size=1000,
                    tol=1e-2,
                    max_iter=2000,
                    random_state=42
                ))
            ]),
            {
                "clf__C": [0.5, 1.0, 2.0]
            }
        )
    }

    return models


def train_and_optimize_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_output_path: Path | str = "models/poverty_model.joblib"
) -> Tuple[Pipeline, Dict[str, Dict[str, Any]]]:
    """
    Ejecuta la validación cruzada estratificada (5-folds) para optimizar hiperparámetros
    utilizando F1-score como métrica guía, selecciona el mejor estimador y lo serializa.

    Parameters
    ----------
    X_train : pd.DataFrame
        Matriz de características de entrenamiento.
    y_train : pd.Series
        Vector objetivo de entrenamiento.
    model_output_path : Path | str
        Ruta destino para guardar el pipeline ganador con joblib.

    Returns
    -------
    Tuple[Pipeline, Dict[str, Dict[str, Any]]]
        Pipeline entrenado ganador y diccionario consolidado de resultados.
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    candidate_pipelines = build_candidate_pipelines()
    results: Dict[str, Dict[str, Any]] = {}

    best_overall_score = -1.0
    winning_model_name = ""
    winning_pipeline: Any = None

    print("=" * 105)
    print("FASE 3: MODELADO SUPERVISADO Y OPTIMIZACIÓN DE HIPERPARÁMETROS (5-FOLD STRATIFIED CV)")
    print("=" * 105)

    for model_name, (pipeline, param_grid) in candidate_pipelines.items():
        print(f"[ENTRENAMIENTO] Optimizando {model_name}...")
        start_time = time.time()

        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring="f1",
            cv=cv,
            n_jobs=-1,
            refit=True
        )
        grid_search.fit(X_train, y_train)

        elapsed = time.time() - start_time
        best_idx = grid_search.best_index_
        mean_f1 = float(grid_search.cv_results_["mean_test_score"][best_idx])
        std_f1 = float(grid_search.cv_results_["std_test_score"][best_idx])
        best_params = grid_search.best_params_

        results[model_name] = {
            "mean_f1": mean_f1,
            "std_f1": std_f1,
            "best_params": best_params,
            "best_estimator": grid_search.best_estimator_,
            "elapsed_seconds": elapsed
        }

        print(f"      - F1-Score CV: {mean_f1:.4f} (+/- {std_f1:.4f}) en {elapsed:.1f}s")
        print(f"      - Hiperparámetros óptimos: {best_params}\n")

        if mean_f1 > best_overall_score:
            best_overall_score = mean_f1
            winning_model_name = model_name
            winning_pipeline = grid_search.best_estimator_

    # Imprimir tabla comparativa formal
    print("=" * 105)
    print("TABLA COMPARATIVA DE RENDIMIENTO EN VALIDACIÓN CRUZADA (MÉTRICA GUÍA: F1-SCORE)")
    print("=" * 105)
    print(f"{'Algoritmo':<35} {'F1-Score CV':>14} {'Desv. Est.':>14} {'Hiperparámetros Óptimos':<38}")
    print("-" * 105)

    for m_name, m_data in results.items():
        params_str = str(m_data["best_params"])
        if len(params_str) > 36:
            params_str = params_str[:33] + "..."
        print(f"{m_name:<35} {m_data['mean_f1']:>14.4f} {m_data['std_f1']:>14.4f} {params_str:<38}")

    print("-" * 105)
    print(f"[MODELO GANADOR] Seleccionado: {winning_model_name} (F1-Score CV = {best_overall_score:.4f})\n")

    # Reentrenar el pipeline ganador sobre el 100% del split de entrenamiento (70%)
    print(f"[REENTRENAMIENTO] Reentrenando pipeline ganador sobre el 100% de X_train ({len(X_train):,} filas)...")
    winning_pipeline.fit(X_train, y_train)

    # Serialización en models/poverty_model.joblib
    dest_path = Path(model_output_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(winning_pipeline, dest_path)

    print(f"[SERIALIZACIÓN] Artefacto del modelo persistido exitosamente en: {dest_path.resolve()}")
    print("=" * 105 + "\n")

    return winning_pipeline, results


def main() -> None:
    """Función principal de ejecución del módulo de entrenamiento."""
    X_train, _, y_train, _ = load_and_split_data()
    train_and_optimize_models(X_train, y_train)


if __name__ == "__main__":
    main()
