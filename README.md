# 🇵🇪 ENAHO Poverty Prediction - Documentación Integral del Sistema

Plataforma de Inteligencia Artificial y Machine Learning de grado empresarial para la estimación de riesgo y predicción de vulnerabilidad socioeconómica y condición de pobreza en hogares del Perú, construida a partir de los microdatos oficiales de la **Encuesta Nacional de Hogares (ENAHO - Sumaria 2025)** del Instituto Nacional de Estadística e Informática (**INEI**).

> 📌 **Registro de Fases y Prompts:** Para consultar la bitácora cronológica con la transcripción textual de los requerimientos y prompts solicitados en cada fase, revise el archivo [`BITACORA_FASES.md`](BITACORA_FASES.md).

---

## 🏛️ 1. Arquitectura General del Sistema

El sistema implementa una arquitectura modular que desacopla la ingesta de microdatos, la ingeniería de características, el entrenamiento y serialización de modelos, la capa de servicio API REST y la interfaz interactiva para usuarios finales.

```
Pro_Pobreza/
│
├── .github/
│   └── workflows/
│       └── mlops_ci.yml          # Pipeline de Integración Continua (GitHub Actions)
│
├── data/
│   ├── raw/
│   │   └── Sumaria-2025.csv      # Microdatos oficiales brutos INEI (33,702 observaciones)
│   └── processed/
│       ├── enaho_processed.csv   # Dataset depurado y estandarizado (33,702 × 7)
│       ├── X_test.csv            # Matriz de características para prueba no vista (30%)
│       └── y_test.csv            # Vector objetivo para prueba no vista (30%)
│
├── models/
│   ├── .gitkeep                  # Persistencia de directorio en Git
│   └── poverty_model.joblib      # Artefacto serializado del modelo ganador (k-NN Pipeline)
│
├── reports/
│   └── figures/
│       ├── confusion_matrix.png  # Visualización anotada de la matriz de confusión
│       └── roc_curve.png         # Curva ROC con AUC frente a la diagonal aleatoria
│
├── src/
│   ├── __init__.py               # Paquete de utilidades core
│   ├── preprocess.py             # Ingesta, limpieza y auditoría estadística vectorial
│   ├── train.py                  # Partición Hold-out 70/30, GridSearchCV y serialización
│   └── evaluate.py               # Métricas formales de clase y generación de curvas
│
├── api/
│   ├── __init__.py               # Paquete API REST
│   ├── schemas.py                # Contratos Pydantic v2 de validación de entradas/salidas
│   └── main.py                   # Servicio web FastAPI y endpoints de inferencia
│
├── tests/
│   ├── __init__.py               # Paquete de pruebas unitarias
│   ├── test_data.py              # Validación de limpieza de datos e integridad
│   └── test_api.py               # Validación de endpoints y contratos HTTP
│
├── app.py                        # Dashboard interactivo para simulación (Streamlit)
├── Dockerfile                    # Receta de contenerización reproducible
├── requirements.txt              # Especificación técnica de dependencias
├── .gitignore                    # Reglas de exclusión de Git
├── BITACORA_FASES.md             # Bitácora histórica de prompts y auditorías
└── README.md                     # Documentación técnica completa del sistema
```

---

## ⚙️ 2. Instalación y Configuración del Entorno

### 2.1 Requisitos Previos
- Python 3.11 o 3.13.
- Gestor de paquetes `pip` actualizado.

### 2.2 Despliegue Local con Entorno Virtual

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# En Windows PowerShell:
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias del proyecto
pip install -r requirements.txt
```

---

## 📊 3. Módulo de Ingesta y Preprocesamiento (`src/preprocess.py`)

### 3.1 Definición de Variables y Target

- **Target Binario (`target`):** Construido a partir de la columna oficial `POBREZA` del INEI:
  - Valores `1` (Pobreza extrema) y `2` (Pobreza no extrema) $\rightarrow$ `1` (Vulnerabilidad / Pobreza).
  - Valor `3` (No pobre) $\rightarrow$ `0` (Hogar no pobre).
  - Registros nulos o fuera del rango $[1, 3]$ son descartados.
- **Variables Estructurales (Sin Data Leakage):**
  1. `DOMINIO` (`int`): Dominio geográfico regional (1 a 8).
  2. `ESTRATO` (`int`): Estrato geográfico urbano/rural según tamaño de población (1 a 8).
  3. `MIEPERHO` (`int`): Número de miembros presentes en el hogar.
  4. `PERCEPHO` (`int`): Número de perceptores de ingresos en el hogar.
  5. `ESTRSOCIAL` (`int`): Estrato socioeconómico asignado al hogar (1: Alto a 6: Muy Bajo).
  6. `SG42` (`float`): Gasto imputado por alquiler de vivienda en Soles (limpieza de comas decimales e imputación a `0.0`).

### 3.2 Prevención Rigurosa de Fuga de Datos (Data Leakage) y Enfoque PMT

El INEI clasifica oficialmente la pobreza monetaria aplicando una fórmula determinista: si $\frac{\text{GASHOG2D}}{\text{MIEPERHO}} < \text{LINEA}$, el hogar es clasificado como pobre. 

**Regla de Oro Aplicada:**
Si el modelo recibiera las variables `GASHOG2D` (Gasto Total Bruto), `INGBRUHD` (Ingreso Bruto) o `LINEA` (Línea de Pobreza Oficial), aprendería trivialmente a dividir y comparar esos valores, produciendo un $F1\text{-Score} = 100\%$ artificial (fuga de datos / memorización matemática).

Para garantizar un modelo predictivo legítimo y robusto frente a jurados y comités científicos, se implementó el enfoque internacional de **Proxy Means Testing (PMT)** (estándar de focalización socioeconómica del Banco Mundial y programas como JUNTOS):
- **Exclusión total** de `GASHOG2D`, `INGBRUHD`, `LINEA` y `LINPE` en el espacio de características $X$.
- Empleo exclusivo de variables estructurales observables y demográficas (`DOMINIO`, `ESTRATO`, `MIEPERHO`, `PERCEPHO`, `ESTRSOCIAL`) y sub-gastos puntuales de infraestructura (`SG42`).
- Las métricas obtenidas ($F1\text{-Score} = 36.69\%$, $\text{ROC-AUC} = 0.6888$, $\text{Accuracy} = 80.27\%$) corroboran un aprendizaje estadístico real y generalizable sin fuga de información.

### 3.3 Fundamentación Matemática Vectorizada (NumPy)
Los momentos estadísticos se calculan vectorialmente mediante álgebra analítica:
- **Centrado:** $dx = x - \bar{x}, \quad dy = y - \bar{y}$
- **Varianza:** $\sigma_x^2 = \text{mean}(dx \cdot dx)$
- **Desviación Estándar:** $\sigma_x = \sqrt{\sigma_x^2}$
- **Covarianza:** $\text{Cov}(x, y) = \text{mean}(dx \cdot dy)$
- **Correlación de Pearson:** $r = \frac{\text{Cov}(x, y)}{\sigma_x \cdot \sigma_y}$

### 3.3 Ejecución del Preprocesamiento
```bash
python src/preprocess.py
```
- **Salida:** Genera `data/processed/enaho_processed.csv` con **33,702 observaciones** y **7 columnas**, con 0 valores nulos y 0 infinitos.

---

## 🤖 4. Módulo de Modelado y Optimización (`src/train.py`)

### 4.1 Estrategia de Partición y Validación
- **Partición Hold-out:** 70% entrenamiento ($23,591$ observaciones) y 30% prueba ($10,111$ observaciones) con preservación estricta de la proporción del target (`stratify=y`, `random_state=42`).
- **Prevención de Fuga de Información:** Cada clasificador se entrena dentro de un `Pipeline` con `StandardScaler()`, de modo que el escalado se ajusta exclusivamente con los datos de entrenamiento de cada pliegue.
- **Optimización con `GridSearchCV`:** Se aplica validación cruzada estratificada de 5 pliegues (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) utilizando **F1-Score** como métrica guía para priorizar la clase minoritaria vulnerable.

### 4.2 Comparativa de Modelos Candidatos

| Algoritmo | Malla de Hiperparámetros Evaluada | F1-Score CV (Media) | Desv. Est. | Hiperparámetros Óptimos |
| :--- | :--- | :---: | :---: | :--- |
| **Regresión Logística (Ridge L2)** | `C` $\in [0.01, 0.1, 1.0, 10.0]$, `max_iter=1000` | `0.2903` | `±0.0110` | `{'clf__C': 10.0}` |
| **K-Nearest Neighbors (k-NN)** | `n_neighbors` $\in [3, 5, 7, 9]$, `weights` $\in [\text{'uniform'}, \text{'distance'}]$ | **`0.3506`** | **`±0.0236`** | `{'clf__n_neighbors': 3, 'clf__weights': 'uniform'}` |
| **Support Vector Machines (SVM RBF)** | `C` $\in [0.5, 1.0, 2.0]$, `kernel='rbf'`, `cache_size=500` | `0.1925` | `±0.0097` | `{'clf__C': 2.0}` |

- **Modelo Ganador:** **K-Nearest Neighbors (k-NN)** con $k=3$ y pesos uniformes.
- **Serialización:** Reentrenado sobre el 100% de `X_train` y persistido en [`models/poverty_model.joblib`](models/poverty_model.joblib).

### 4.3 Ejecución del Entrenamiento
```bash
python src/train.py
```

---

## 📈 5. Módulo de Evaluación Rigurosa (`src/evaluate.py`)

Evalúa el modelo serializado sobre el **conjunto de prueba no visto (30% Hold-out: 10,111 observaciones)** utilizando las métricas formales de clase:

### 5.1 Matriz de Confusión en Prueba
```text
                          |   Predicho: No Pobre (0)   |  Predicho: Vulnerable (1)  |   Total Real  
---------------------------------------------------------------------------------------------------------
Real: No Pobre (0)        |           7,538 (VN)       |            742 (FP)        |     8,280     
Real: Vulnerable (1)      |           1,253 (FN)       |            578 (VP)        |     1,831     
---------------------------------------------------------------------------------------------------------
Total Predicho            |           8,791            |           1,320            |     10,111    
```

### 5.2 Fórmulas y Métricas Formales Obtenidas
- **Verdaderos Positivos (VP):** $578$
- **Verdaderos Negativos (VN):** $7,538$
- **Falsos Positivos (FP):** $742$
- **Falsos Negativos (FN):** $1,253$
- **Precisión (Precision):** $\text{prec} = \frac{\text{VP}}{\text{VP} + \text{FP}} = \mathbf{0.4379}$
- **Recall (Sensibilidad):** $\text{recall} = \frac{\text{VP}}{\text{VP} + \text{FN}} = \mathbf{0.3157}$
- **Especificidad (Specificity):** $\text{espec} = \frac{\text{VN}}{\text{VN} + \text{FP}} = \mathbf{0.9104}$
- **Tasa de Error Positiva ($\text{err}^+$):** $\frac{\text{FN}}{\text{VP} + \text{FN}} = 1 - \text{Recall} = \mathbf{0.6843}$
- **Tasa de Error Negativa ($\text{err}^-$):** $\frac{\text{FP}}{\text{VN} + \text{FP}} = 1 - \text{Especificidad} = \mathbf{0.0896}$
- **F1-Score (Media Armónica):** $\frac{2 \cdot \text{prec} \cdot \text{recall}}{\text{prec} + \text{recall}} = \mathbf{0.3669}$
- **Exactitud Global (Accuracy):** $\frac{\text{VP} + \text{VN}}{\text{Total}} = \mathbf{0.8027}$ ($80.27\%$)
- **Área Bajo la Curva ROC (ROC-AUC):** $\mathbf{0.6888}$

### 5.3 Artefactos Visuales Generados
- `reports/figures/confusion_matrix.png`: Matriz de confusión con conteos absolutos.
- `reports/figures/roc_curve.png`: Curva ROC graficada frente a la diagonal aleatoria ($\text{AUC} = 0.50$).

### 5.4 Ejecución de la Evaluación
```bash
python src/evaluate.py
```

---

## 🌐 6. Capa de Servicios: API REST (`api/`)

Implementada en FastAPI con contratos Pydantic v2 para inferencia en tiempo real.

### 6.1 Endpoints Disponibles
- `GET /`: Metadatos generales del microservicio y versión.
- `GET /health`: Healthcheck operativo y confirmación de modelo en memoria.
- `POST /predict`: Inferencia en tiempo real. Recibe las 6 características estructurales y retorna la predicción (`0` o `1`), etiqueta descriptiva y probabilidad estimada.

### 6.2 Ejecución del Servidor Uvicorn
```bash
uvicorn api.main:app --reload --port 8000
```
- **Documentación Swagger UI:** `http://localhost:8000/docs`
- **Documentación ReDoc:** `http://localhost:8000/redoc`

---

## 💻 7. Interfaz de Usuario: Dashboard Streamlit (`app.py`)

Prototipo interactivo para análisis exploratorio y simulación de escenarios de vulnerabilidad familiar:
- Permite configurar los parámetros del hogar (`DOMINIO`, `ESTRATO`, `MIEPERHO`, `PERCEPHO`, `ESTRSOCIAL`, `SG42`).
- Ejecuta la predicción instantánea con barra de probabilidad de riesgo.
- Presenta métricas descriptivas y visualización del dataset procesado.

### 7.1 Ejecución de la Aplicación Web
```bash
streamlit run app.py
```
- **Acceso web:** `http://localhost:8501`

---

## 🧪 8. Suite de Pruebas Automatizadas (`tests/`)

Pruebas unitarias y de integración implementadas con `pytest`:
- `tests/test_data.py`: Verifica la depuración de moneda, imputación de nulos y coherencia del esquema procesado.
- `tests/test_api.py`: Verifica los códigos de respuesta HTTP (`200 OK`, `422 Unprocessable Entity`) ante payloads válidos e inválidos.

### 8.1 Ejecución de Pruebas
```bash
pytest -v tests/
```
- **Resultado:** 6 de 6 pruebas superadas (`100% Passed`).

---

## 🐳 9. Despliegue con Docker

Contenerización sobre imagen ligera `python:3.11-slim`:

```bash
# 1. Construir la imagen Docker
docker build -t pro-pobreza:1.0.0 .

# 2. Ejecutar contenedor de la API REST (Puerto 8000)
docker run -d -p 8000:8000 --name api-pobreza pro-pobreza:1.0.0

# 3. Ejecutar contenedor del Dashboard Streamlit (Puerto 8501)
docker run -d -p 8501:8501 --name app-pobreza pro-pobreza:1.0.0 streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🔄 10. Integración Continua (CI/CD)

Flujo automatizado en [`.github/workflows/mlops_ci.yml`](.github/workflows/mlops_ci.yml):
1. Gatillado automático en cada `push` o `pull_request` a las ramas principales.
2. Configuración de entorno Python 3.11 con caché de dependencias.
3. Instalación de paquetes de `requirements.txt`.
4. Ejecución de la suite completa de pruebas con `pytest`.
