# 📋 Bitácora Oficial de Fases y Registro de Prompts - Pro_Pobreza

Este documento es el **registro cronológico estricto de requerimientos y auditoría por fases**. Contiene la copia textual de cada prompt enviado por el usuario, las restricciones establecidas, las acciones de ingeniería realizadas, los comandos de validación ejecutados y las salidas reales de consola obtenidas.

---

## 📑 Índice de Fases

1. [Fase 1: Configuración de la Arquitectura Empresarial y Entorno MLOps](#fase-1-configuración-de-la-arquitectura-empresarial-y-entorno-mlops)
2. [Fase 2: Ingesta, Preprocesamiento de Datos y Auditoría Estadística Vectorial (`src/preprocess.py`)](#fase-2-ingesta-preprocesamiento-de-datos-y-auditoría-estadística-vectorial)
3. [Fase 3: Modelado Supervisado, GridSearchCV, Serialización y Evaluación Rigurosa (`src/train.py` y `src/evaluate.py`)](#fase-3-modelado-supervisado-gridsearchcv-serialización-y-evaluación-rigurosa)

---

## Fase 1: Configuración de la Arquitectura Empresarial y Entorno MLOps

### 📥 Prompt Original Recibido (Textual)

> ```text
> Eres un Ingeniero de Software Senior. Tu tarea inmediata es completar la estructura integral del proyecto 'Pro_Pobreza' creando todas las carpetas y archivos base que faltan según la arquitectura de grado empresarial definida para este proyecto.
> 
> Revisa la estructura actual y crea los siguientes directorios y archivos vacíos (o con docstrings base) respetando esta jerarquía exacta:
> 
> Pro_Pobreza/
> │
> ├── .github/
> │   └── workflows/
> │       └── mlops_ci.yml
> │
> ├── data/
> │   ├── raw/
> │   │   └── Sumaria-2025.csv       (ya existente)
> │   └── processed/
> │       └── enaho_processed.csv   (ya existente)
> │
> ├── models/
> │   └── .gitkeep                  (para mantener el directorio listo para el artefacto .joblib)
> │
> ├── src/
> │   ├── __init__.py               (ya existente)
> │   ├── preprocess.py             (ya existente)
> │   ├── train.py                  (nuevo)
> │   └── evaluate.py               (nuevo)
> │
> ├── api/
> │   ├── __init__.py               (nuevo)
> │   ├── schemas.py                (nuevo)
> │   └── main.py                   (nuevo)
> │
> ├── tests/
> │   ├── __init__.py               (nuevo)
> │   ├── test_data.py              (nuevo)
> │   └── test_api.py               (nuevo)
> │
> ├── app.py                        (nuevo)
> ├── Dockerfile                    (nuevo)
> ├── requirements.txt              (nuevo, incluyendo pandas, numpy, scikit-learn, joblib, matplotlib, seaborn, fastapi, uvicorn, pydantic, pytest, requests, streamlit)
> ├── .gitignore                    (nuevo, ignorando __pycache__/, .pytest_cache/, venv/, env/, y temporales)
> └── README.md                     (nuevo)
> 
> Ejecuta los comandos de sistema necesarios para crear estos directorios y archivos en el workspace actual y muestra el árbol de directorios resultante para validar su existencia.
> ```

### 🛠️ Acciones de Ingeniería Realizadas
1. Creación de todos los directorios y archivos base del proyecto respetando la jerarquía requerida.
2. Definición formal de dependencias en `requirements.txt`.
3. Creación de reglas de exclusión en `.gitignore`.
4. Instalación de paquetes faltantes en Python 3.13 (`streamlit`, `fastapi`, `uvicorn`, `pydantic`, `pytest`, `seaborn`, `httpx`).
5. Configuración de `.vscode/settings.json` para mapear el intérprete real y resolver subrayados rojos en el editor.
6. Tipado estricto en `app.py`.

### 💻 Salida de Validación en Terminal
```text
Listado de rutas de carpetas para el volumen Nuevo vol
E:.
|   .gitignore
|   app.py
|   Dockerfile
|   README.md
|   requirements.txt
|   
+---.github
|   \---workflows
|           mlops_ci.yml
|           
+---api
|       main.py
|       schemas.py
|       __init__.py
|       
+---data
|   +---processed
|   |       enaho_processed.csv
|   |       
|   \---raw
|           Sumaria-2025.csv
|           
+---models
|       .gitkeep
|       poverty_model.joblib
|       
+---src
|       evaluate.py
|       preprocess.py
|       train.py
|       __init__.py
|       
\---tests
        test_api.py
        test_data.py
        __init__.py
```

### ✅ Estado: APROBADO

---

## Fase 2: Ingesta, Preprocesamiento de Datos y Auditoría Estadística Vectorial

### 📥 Prompt Original Recibido (Textual)

> ```text
> Eres un Lead Data Engineer y ML Architect trabajando en el repositorio 'Pro_Pobreza'. 
> 
> Tu objetivo único y exclusivo en esta tarea es implementar y consolidar de forma completa y definitiva el script `src/preprocess.py` correspondiente a la FASE 2 del proyecto.
> 
> ### REGLA 1: ALCANCE CERRADO
> - Archivo permitido: Trabaja ÚNICAMENTE sobre `src/preprocess.py`.
> - Archivos prohibidos: TIENES TERMINANTEMENTE PROHIBIDO crear archivos temporales o modificar cualquier archivo dentro de `api/`, `tests/`, `.github/` o `models/`. No toques `README.md` ni `requirements.txt`.
> 
> ### REGLA 2: IMPLEMENTACIÓN DE CÓDIGO COMPLETO
> - NO utilices marcadores `# TODO`, código resumido, funciones incompletas ni puntos suspensivos (`...`).
> - Todo el código debe ser 100% operativo, modularizado mediante funciones y con tipado estático (`typing`).
> - Sigue rigurosamente estas especificaciones técnicas:
> 
> 1. Ingesta y Limpieza de Datos:
>    - Cargar `data/raw/Sumaria-2025.csv` soportando separadores `;` o `,`, codificación `latin1` y `low_memory=False`.
>    - Crear el target binario `target` a partir de `POBREZA`:
>      * Valores [1, 2] -> 1 (Pobreza extrema y no extrema / Condición de vulnerabilidad).
>      * Valor 3 -> 0 (No pobre).
>      * Descartar registros con valores nulos o fuera del rango [1, 3] en `POBREZA`.
>    - Extraer y castear las 6 características estructurales seleccionadas:
>      * `DOMINIO`: entero.
>      * `ESTRATO`: entero.
>      * `MIEPERHO`: entero (miembros del hogar).
>      * `PERCEPHO`: entero (perceptores de ingresos).
>      * `ESTRSOCIAL`: entero.
>      * `SG42`: float (limpiar cadenas monetarias con coma decimal ej. "120,50" -> 120.50, espacios en blanco y rellenar nulos con 0.0).
>    - Eliminar cualquier fila residual con valores NaN en estas 6 columnas.
> 
> 2. Fundamentación Matemática Vectorizada (NumPy):
>    Implementa las fórmulas analíticas de momentos estadísticos sin delegar en métodos opacos:
>    - Centrado respecto a la media: dx = x - np.mean(x), dy = y - np.mean(y)
>    - Varianza: variance = np.mean(dx * dx)
>    - Desviación estándar: stdev = np.sqrt(variance)
>    - Covarianza muestral: covariance = np.mean(dx * dy)
>    - Correlación de Pearson: r = covariance / (stdev_x * stdev_y)
> 
> 3. Secuencia de Ejecución y Auditoría en Terminal:
>    El script debe estructurarse para ejecutar y mostrar en consola de forma secuencial:
>    - PASO 1: Confirmación de carga de datos brutos y dimensiones iniciales.
>    - PASO 2: Tabla de Auditoría Estadística Univariada con Media, Varianza, Desviación Estándar, Mínimo y Máximo para cada una de las 6 variables predictoras.
>    - PASO 3: Tabla de Auditoría Estadística Bivariada con Covarianza y Correlación de Pearson respecto a `target`, junto con el balance de clases (frecuencia y porcentaje de clase 0 vs. clase 1).
>    - PASO 4: Resumen y Reporte Final de Integridad comprobando 0 nulos/infinitos, guardando en `data/processed/enaho_processed.csv` (UTF-8, delimitador coma `,`, `index=False`) e imprimiendo la confirmación con la ruta y dimensiones exactas (filas, columnas).
> 
> ### REGLA 3: CRITERIO DE VALIDACIÓN EJECUTABLE
> Ejecuta directamente en la terminal integrada el siguiente comando:
> `python src/preprocess.py`
> 
> Muestra la salida completa generada en la terminal desde el PASO 1 hasta el PASO 4.
> ```

### 🛠️ Acciones de Ingeniería Realizadas
1. Implementación modularizada de `src/preprocess.py` con tipado estático `typing.Dict`, `typing.List`, `typing.Tuple`.
2. Detección automática de delimitadores `;` y `,`.
3. Filtrado de registros en `POBREZA` en `[1, 3]` y mapeo a target binario (`1` vs `0`).
4. Limpieza de `SG42` (reemplazo de comas, espacios y relleno con `0.0`) y eliminación de residuales `NaN`.
5. Fórmulas analíticas vectorizadas con NumPy para momentos univariados y bivariados.
6. Exportación en `data/processed/enaho_processed.csv`.

### 💻 Salida Real de Validación en Terminal (`python src/preprocess.py`)
```text
====================================================================================================
PASO 1: CONFIRMACIÓN DE CARGA DE DATOS BRUTOS Y DIMENSIONES INICIALES
====================================================================================================
Ruta de entrada especificada: E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\data\raw\Sumaria-2025.csv
Delimitador detectado: ';' | Codificación: 'latin1' | low_memory: False
Dimensiones de entrada leídas: 33,702 filas y 161 columnas.
Columnas estructurales y variable de pobreza identificadas exitosamente.
Registros validados en 'POBREZA': 33,702 (100% conformes en rango [1, 3]).
Integridad de características estructurales: 0 filas residuales con NaN.
Observaciones estructuradas consolidadas: 33,702 registros.

====================================================================================================
PASO 2: TABLA DE AUDITORÍA ESTADÍSTICA UNIVARIADA (MOMENTOS VECTORIZADOS EN NUMPY)
====================================================================================================
Variable                Media         Varianza   Desv. Estándar         Mínimo         Máximo
----------------------------------------------------------------------------------------------------
DOMINIO                4.8643           5.5910           2.3645         1.0000         8.0000
ESTRATO                4.1883           5.9376           2.4367         1.0000         8.0000
MIEPERHO               3.1852           2.9930           1.7300         1.0000        15.0000
PERCEPHO               1.9902           0.9867           0.9933         0.0000         9.0000
ESTRSOCIAL             4.6979           1.6830           1.2973         1.0000         6.0000
SG42                 123.7279       44922.4943         211.9493         0.0000      1990.1860
----------------------------------------------------------------------------------------------------

====================================================================================================
PASO 3: TABLA DE AUDITORÍA ESTADÍSTICA BIVARIADA Y BALANCE DE CLASES
====================================================================================================
Variable           Covarianza (c/ target)    Correlación Pearson (r)   Interpretación      
----------------------------------------------------------------------------------------------------
DOMINIO                          0.047957                   0.052665   Asociación muy leve 
ESTRATO                          0.147992                   0.157704   Asociación positiva 
MIEPERHO                         0.159273                   0.239058   Asociación positiva 
PERCEPHO                         0.017025                   0.044503   Asociación muy leve 
ESTRSOCIAL                       0.096011                   0.192174   Asociación positiva 
SG42                           -16.268146                  -0.199304   Asociación inversa (protectora)
----------------------------------------------------------------------------------------------------

Balance de Clases (Variable 'target'):
  - Clase 0 [No pobre]:                    27,598 hogares ( 81.89%)
  - Clase 1 [Pobreza / Vulnerabilidad]:      6,104 hogares ( 18.11%)
  - Total Muestral Evaluado:               33,702 hogares (100.00%)
  - Relación de Desbalance (Clase 0/1):       4.52 : 1

====================================================================================================
PASO 4: RESUMEN Y REPORTE FINAL DE INTEGRIDAD
====================================================================================================
[AUDITORÍA INTEGRIDAD] Total de valores nulos (NaN) detectados:      0
[AUDITORÍA INTEGRIDAD] Total de valores infinitos (Inf) detectados:  0
[EXPORTACIÓN EXITOSA] Archivo generado en: E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\data\processed\enaho_processed.csv
[DIMENSIONES FINALES] Filas: 33,702 | Columnas: 7
[COLUMNAS PROCESADAS] ['DOMINIO', 'ESTRATO', 'MIEPERHO', 'PERCEPHO', 'ESTRSOCIAL', 'SG42', 'target']
====================================================================================================
```

### 📁 Artefactos Generados
- `data/processed/enaho_processed.csv` (33,702 filas $\times$ 7 columnas).

### ✅ Estado: APROBADO

---

## Fase 3: Modelado Supervisado, GridSearchCV, Serialización y Evaluación Rigurosa

### 📥 Prompt Original Recibido (Textual)

> ```text
> Eres un Lead ML Engineer y Especialista en Algoritmos de Aprendizaje Supervisado en el proyecto 'Pro_Pobreza'.
> 
> Tu objetivo exclusivo en esta tarea es implementar y ejecutar de forma rigurosa la FASE 3: Modelado Supervisado, Optimización de Hiperparámetros, Serialización y Evaluación Rigurosa, cumpliendo estrictamente con los 3 algoritmos de la planificación oficial y todas las métricas formales de las diapositivas de clase de la docente (matriz de confusión, precisión, recall, especificidad, F1-score y tasas de error).
> 
> ### REGLA 1: ALCANCE CERRADO
> - Archivos y directorios permitidos:
>   * Modificar/crear únicamente: `src/train.py` y `src/evaluate.py`.
>   * Directorios autorizados para escribir artefactos: `models/`, `data/processed/` y `reports/figures/` (crear las carpetas si no existen).
> - Archivos prohibidos: TIENES TERMINANTEMENTE PROHIBIDO modificar `src/preprocess.py`, ni tocar archivos en `api/`, `tests/` o `.github/`. No alteres `requirements.txt` ni `README.md`.
> 
> ### REGLA 2: IMPLEMENTACIÓN DE CÓDIGO COMPLETO
> - NO utilices `# TODO`, funciones abreviadas ni puntos suspensivos (`...`). Código 100% operativo, tipado con `typing` y documentado.
> - Especificaciones técnicas obligatorias:
> 
> #### DIRECTIVA 1: Implementación de `src/train.py`
> 1. Carga de Datos y Partición Hold-out:
>    - Leer `data/processed/enaho_processed.csv`.
>    - Separar matriz X (`DOMINIO`, `ESTRATO`, `MIEPERHO`, `PERCEPHO`, `ESTRSOCIAL`, `SG42`) y vector y (`target`).
>    - Aplicar división Hold-out estratificada: 70% entrenamiento y 30% prueba con semilla `random_state=42` y `stratify=y` para preservar la proporción de desbalance del target.
>    - Guardar los datos de prueba no vistos en `data/processed/X_test.csv` e `data/processed/y_test.csv` con `index=False`.
> 2. Prevención Estricta de Data Leakage:
>    - Cada clasificador debe acoplarse dentro de un `Pipeline` de scikit-learn con `StandardScaler()`. El escalador Z-score debe ajustarse (`fit`) exclusivamente sobre los datos de entrenamiento de cada pliegue.
> 3. Los 3 Algoritmos a Evaluar y Optimizar mediante GridSearchCV:
>    - Algoritmo 1: Regresión Logística con regularización L2 (Ridge), optimizando `clf__C` en [0.01, 0.1, 1.0, 10.0] con `max_iter=1000`.
>    - Algoritmo 2: K-Nearest Neighbors (k-NN) basado en distancias euclidianas, evaluando `clf__n_neighbors` en [3, 5, 7, 9] con pesos `weights` en ['uniform', 'distance'].
>    - Algoritmo 3: Support Vector Machines (SVM) con margen blando y kernel RBF, evaluando `clf__C` en [0.5, 1.0, 2.0] con `probability=True` y `cache_size=500`.
> 4. Validación Cruzada Estratificada y Criterio de Selección:
>    - Utilizar `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
>    - Métrica principal de optimización: `scoring='f1'` (atendiendo a la clase vulnerable positiva).
>    - Calcular la media y desviación estándar de validación cruzada para cada modelo.
> 5. Reentrenamiento y Serialización:
>    - Seleccionar el estimador con el mejor F1-score medio en validación cruzada.
>    - Reentrenar el pipeline ganador completo (escalador + modelo optimizado) sobre el 100% del split de entrenamiento (70%).
>    - Serializar el artefacto en `models/poverty_model.joblib`.
>    - Imprimir en terminal una tabla comparativa clara con el mejor F1-score y los hiperparámetros óptimos encontrados para cada uno de los 3 modelos.
> 
> #### DIRECTIVA 2: Implementación de `src/evaluate.py`
> 1. Carga de Artefactos:
>    - Cargar `models/poverty_model.joblib`, `data/processed/X_test.csv` y `data/processed/y_test.csv`.
> 2. Predicción e Inferencia:
>    - Generar predicciones binarias `y_pred = model.predict(X_test)` y probabilidades continuas `y_proba = model.predict_proba(X_test)[:, 1]`.
> 3. Métricas Formales de Clase (Fórmulas directas de las diapositivas):
>    - Extraer valores de la matriz de confusión: Verdaderos Positivos (VP), Verdaderos Negativos (VN), Falsos Positivos (FP) y Falsos Negativos (FN).
>    - Calcular e imprimir textualmente:
>      * Precisión: prec = VP / (VP + FP)
>      * Recall (Sensibilidad): recall = VP / (VP + FN)
>      * Especificidad: espec = VN / (VN + FP) = 1 - TFP
>      * Tasa de error positiva: err_plus = FN / (VP + FN)
>      * Tasa de error negativa: err_minus = FP / (VN + FP)
>      * F1-Score: F1 = 2 * (prec * recall) / (prec + recall)
>      * Accuracy y ROC-AUC.
> 4. Generación de Artefactos Visuales:
>    - Crear el directorio `reports/figures/` si no existe y exportar:
>      * `confusion_matrix.png`: Matriz de confusión visualizada con `ConfusionMatrixDisplay` anotada con valores absolutos.
>      * `roc_curve.png`: Curva ROC graficada frente a la diagonal aleatoria (AUC = 0.5) indicando el AUC obtenido.
> 5. Salida en Consola:
>    - Imprimir la matriz de confusión en formato tabular legible y el reporte formal estructurado con todas las métricas de clase calculadas sobre los datos de prueba independientes (30%).
> 
> ### REGLA 3: CRITERIO DE VALIDACIÓN EJECUTABLE
> Ejecuta secuencialmente en la terminal integrada los siguientes comandos:
> 1. `python src/train.py`
> 2. `python src/evaluate.py`
> 
> Muestra la salida completa en consola: la tabla comparativa de los 3 modelos con CV, la confirmación de guardado de `models/poverty_model.joblib`, la matriz de confusión tabular, el reporte con todas las métricas de clase (precisión, recall, especificidad, err+, err-, F1 y ROC-AUC) y la confirmación de las figuras guardadas.
> ```

### 🛠️ Acciones de Ingeniería Realizadas
1. Implementación de `src/train.py` con Hold-out 70/30 estratificado y pipelines con `StandardScaler`.
2. Evaluación paralela de los 3 clasificadores con `GridSearchCV` (`scoring='f1'`, 5 folds estratificados).
3. Selección del estimador óptimo: **k-NN** ($k=3$, pesos uniformes, F1 CV = 0.3506).
4. Reentrenamiento sobre el 100% de `X_train` ($23,591$ filas) y serialización en `models/poverty_model.joblib`.
5. Implementación de `src/evaluate.py` calculando las métricas exactas de las diapositivas de clase sobre el 30% no visto ($10,111$ muestras).
6. Generación de artefactos visuales en `reports/figures/`: `confusion_matrix.png` y `roc_curve.png`.

### 💻 Salida Real de Validación en Terminal

#### Comando 1: `python src/train.py`
```text
[DATOS] Split Hold-out estratificado (70% train / 30% test):
        - Entrenamiento: 23,591 muestras
        - Prueba no vista: 10,111 muestras
[DATOS] Conjuntos de prueba exportados en: E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\data\processed\X_test.csv y E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\data\processed\y_test.csv

=========================================================================================================
FASE 3: MODELADO SUPERVISADO Y OPTIMIZACIÓN DE HIPERPARÁMETROS (5-FOLD STRATIFIED CV)
=========================================================================================================
[ENTRENAMIENTO] Optimizando Regresión Logística (Ridge L2)...
      - F1-Score CV: 0.2903 (+/- 0.0110) en 3.2s
      - Hiperparámetros óptimos: {'clf__C': 10.0}

[ENTRENAMIENTO] Optimizando K-Nearest Neighbors (k-NN)...
      - F1-Score CV: 0.3506 (+/- 0.0236) en 0.6s
      - Hiperparámetros óptimos: {'clf__n_neighbors': 3, 'clf__weights': 'uniform'}

[ENTRENAMIENTO] Optimizando Support Vector Machines (SVM RBF)...
      - F1-Score CV: 0.1925 (+/- 0.0097) en 190.1s
      - Hiperparámetros óptimos: {'clf__C': 2.0}

=========================================================================================================
TABLA COMPARATIVA DE RENDIMIENTO EN VALIDACIÓN CRUZADA (MÉTRICA GUÍA: F1-SCORE)
=========================================================================================================
Algoritmo                              F1-Score CV     Desv. Est. Hiperparámetros Óptimos               
---------------------------------------------------------------------------------------------------------
Regresión Logística (Ridge L2)              0.2903         0.0110 {'clf__C': 10.0}                      
K-Nearest Neighbors (k-NN)                  0.3506         0.0236 {'clf__n_neighbors': 3, 'clf__weights': 'uniform'}  
Support Vector Machines (SVM RBF)           0.1925         0.0097 {'clf__C': 2.0}                       
---------------------------------------------------------------------------------------------------------
[MODELO GANADOR] Seleccionado: K-Nearest Neighbors (k-NN) (F1-Score CV = 0.3506)

[REENTRENAMIENTO] Reentrenando pipeline ganador sobre el 100% de X_train (23,591 filas)...
[SERIALIZACIÓN] Artefacto del modelo persistido exitosamente en: E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\models\poverty_model.joblib
=========================================================================================================
```

#### Comando 2: `python src/evaluate.py`
```text
=========================================================================================================
FASE 3: EVALUACIÓN RIGUROSA DE RENDIMIENTO SOBRE DATOS NO VISTOS (30% TEST HOLD-OUT)
=========================================================================================================
[CARGA] Modelo cargado desde: E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\models\poverty_model.joblib
[CARGA] Datos de prueba cargados: 10,111 observaciones no vistas.

=========================================================================================================
MATRIZ DE CONFUSIÓN (CONJUNTO DE PRUEBA INDEPENDIENTE)
=========================================================================================================
                          |   Predicho: No Pobre (0)   |  Predicho: Vulnerable (1)  |   Total Real  
---------------------------------------------------------------------------------------------------------
Real: No Pobre (0)        |           7,538            |            742             |     8,280     
Real: Vulnerable (1)      |           1,253            |            578             |     1,831     
---------------------------------------------------------------------------------------------------------
Total Predicho            |           8,791            |           1,320            |     10,111    

=========================================================================================================
REPORTE FORMAL DE MÉTRICAS DE CLASE (FÓRMULAS DIRECTAS DE DIAPOSITIVAS)
=========================================================================================================
  * Verdaderos Positivos (VP):                  578  [Hogares vulnerables clasificados correctamente]
  * Verdaderos Negativos (VN):                7,538  [Hogares no pobres clasificados correctamente]
  * Falsos Positivos (FP):                      742  [Hogares no pobres clasificados erróneamente]
  * Falsos Negativos (FN):                    1,253  [Hogares vulnerables clasificados erróneamente]
---------------------------------------------------------------------------------------------------------
  * Precisión (Precision):                   0.4379  (VP / [VP + FP])
  * Recall / Sensibilidad:                   0.3157  (VP / [VP + FN])
  * Especificidad (Specificity):             0.9104  (VN / [VN + FP] = 1 - TFP)
  * Tasa de Error Positiva (err+):           0.6843  (FN / [VP + FN] = 1 - Recall)
  * Tasa de Error Negativa (err-):           0.0896  (FP / [VN + FP] = 1 - Espec)
  * F1-Score (Media Armónica):               0.3669  (2 * [Prec * Rec] / [Prec + Rec])
  * Exactitud Global (Accuracy):             0.8027  ([VP + VN] / Total)
  * Área Bajo Curva ROC (ROC-AUC):           0.6888
=========================================================================================================

[ARTEFACTOS VISUALES EXPORTADOS]
  - Matriz de Confusión:  E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\reports\figures\confusion_matrix.png
  - Curva ROC:            E:\9semestre\Aprendizaje de maquin\Pro_Pobreza\reports\figures\roc_curve.png
=========================================================================================================
```

### 📁 Artefactos Generados
- `models/poverty_model.joblib`
- `data/processed/X_test.csv` ($10,111 \times 6$)
- `data/processed/y_test.csv` ($10,111 \times 1$)
- `reports/figures/confusion_matrix.png`
- `reports/figures/roc_curve.png`

### ✅ Estado: APROBADO
