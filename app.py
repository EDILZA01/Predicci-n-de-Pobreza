"""
ENAHO Poverty & Socioeconomic Vulnerability Predictor - Streamlit Dashboard
===========================================================================
Plataforma Empresarial MLOps con 2 Pestañas Estructuradas:
  - Pestaña 1: Household Assessment (Evaluación en tiempo real con mapas y dispersión)
  - Pestaña 2: Model Performance & MLOps (Métricas formales, benchmark y artefactos)
Fondo Deep Blue, Tipografía 100% Blanca y Mapas Claros de Alto Contraste.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

DEFAULT_API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
DATASET_PATH = Path("data/processed/enaho_processed.csv")

# Coordenadas geográficas oficiales de los 8 dominios del INEI en el Perú
REGIONAL_DATA: Dict[int, Dict[str, Any]] = {
    1: {"name_es": "Costa Norte", "name_en": "North Coast", "lat": -5.20, "lon": -80.63, "poverty_rate": 24.6},
    2: {"name_es": "Costa Centro", "name_en": "Center Coast", "lat": -14.07, "lon": -75.73, "poverty_rate": 21.2},
    3: {"name_es": "Costa Sur", "name_en": "South Coast", "lat": -17.19, "lon": -70.93, "poverty_rate": 15.8},
    4: {"name_es": "Sierra Norte", "name_en": "North Highlands", "lat": -7.16, "lon": -78.51, "poverty_rate": 38.4},
    5: {"name_es": "Sierra Centro", "name_en": "Center Highlands", "lat": -12.07, "lon": -75.21, "poverty_rate": 34.1},
    6: {"name_es": "Sierra Sur", "name_en": "South Highlands", "lat": -14.28, "lon": -71.50, "poverty_rate": 42.7},
    7: {"name_es": "Selva / Amazonía", "name_en": "Jungle / Amazon", "lat": -4.50, "lon": -74.50, "poverty_rate": 32.5},
    8: {"name_es": "Lima Metropolitana", "name_en": "Metropolitan Lima", "lat": -12.0464, "lon": -77.0428, "poverty_rate": 18.9},
}

# Diccionario de Textos Bilingües
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "es": {
        "page_title": "Predictor de Pobreza ENAHO | Plataforma MLOps",
        "header_title": "🇵🇪 ENAHO - Predictor de Pobreza y Vulnerabilidad",
        "header_subtitle": "Sistema Empresarial de Soporte a Decisiones basado en la Encuesta Nacional de Hogares (INEI Perú)",
        "tab1_title": "🏠 Household Assessment (Evaluación en Tiempo Real)",
        "tab2_title": "📊 Model Performance & MLOps (Rendimiento del Modelo)",
        "sidebar_config": "⚙️ Configuración del Sistema",
        "backend_url_label": "URL del Microservicio FastAPI",
        "backend_url_help": "Dirección base del microservicio REST de inferencia",
        "backend_online": "🟢 Backend Online",
        "backend_offline": "🟡 Backend Standby / Offline",
        "backend_offline_hint": "Inicie: uvicorn api.main:app --port 8000",
        "methodology_title": "📋 Metodología del Modelo",
        "methodology_desc": """
- **Fuente Oficial:** INEI ENAHO (Sumaria 2025)
- **Pipeline:** StandardScaler + k-NN Optimizado
- **Validación:** 5-Fold Stratified Cross-Validation
- **Regla:** Clasificación Binaria Supervisada
- **Latencia:** < 50ms por inferencia REST
        """,
        "presets_title": "⚡ Perfiles de Prueba Rápida",
        "preset_urban": "🏢 Cargar Perfil Urbano (No Pobre)",
        "preset_rural": "🌾 Cargar Perfil Rural (Vulnerable)",
        "step1_title": "1️⃣ Parámetros Geográficos y Regionales",
        "step2_title": "2️⃣ Demografía y Equipamiento del Hogar",
        "domain_label": "Dominio Geográfico (DOMINIO)",
        "domain_help": "Dominio regional según estratificación geográfica del INEI",
        "stratum_label": "Estrato Poblacional (ESTRATO)",
        "stratum_help": "Estrato por tamaño poblacional y área urbana/rural",
        "socio_label": "Estrato Socioeconómico (ESTRSOCIAL)",
        "socio_help": "Estrato del marco censal (1: Alto a 6: Muy Bajo)",
        "mieperho_label": "Miembros Presentes en el Hogar (MIEPERHO)",
        "mieperho_help": "Residentes habituales que comparten la olla común (P204=1)",
        "percepho_label": "Perceptores de Ingresos (PERCEPHO)",
        "percepho_help": "Miembros de 14 años a más que generan ingresos",
        "percepho_warning": "⚠️ Advertencia: El número de perceptores no puede superar el total de miembros.",
        "sg42_label": "Gasto Mensual en Equipamiento / Tecnología S/. (SG42)",
        "sg42_help": "Gasto mensual o tenencia en equipos del hogar (TV, audio, computadoras en Soles)",
        "btn_predict": "⚡ EJECUTAR EVALUACIÓN DE VULNERABILIDAD",
        "btn_predict_spinner": "Consultando microservicio REST de inferencia...",
        "results_title": "3️⃣ Diagnóstico y Resultados de la Evaluación",
        "status_poor": "🚨 Estado: Hogar en Condición de Vulnerabilidad / Pobreza",
        "status_non_poor": "✅ Estado: Hogar Clasificado como No Pobre",
        "metric_prob": "Probabilidad Estimada de Pobreza",
        "metric_prob_help": "Probabilidad calculada por el pipeline k-NN optimizado",
        "metric_risk": "Nivel de Riesgo",
        "metric_risk_help": "Bajo (<35%), Medio (35%-65%), Alto (>65%)",
        "metric_dep": "Ratio de Dependencia Familiar",
        "metric_dep_help": "Carga familiar: Total Miembros / Perceptores Activos",
        "gauge_title": "Índice Acumulado de Vulnerabilidad:",
        "gauge_caption": "Puntaje: {score:.4f} / 1.0000 | Diagnóstico: {status}",
        "raw_json_title": "🔍 Payload de Respuesta JSON (REST API)",
        "map_section_title": "4️⃣ Mapa Oficial del Perú: Ubicación del Hogar",
        "map_section_desc": "Visualización geoespacial clara sobre el territorio peruano con demarcación territorial y costera.",
        "map_style_label": "Estilo del Mapa",
        "map_style_light": "🗺️ Mapa Claro Oficial (Recomendado)",
        "map_style_satellite": "🛰️ Vista Satelital",
        "scatter_title": "5️⃣ Visualización Multidimensional Integral (6 Variables)",
        "scatter_desc": "Compara el hogar evaluado frente a la distribución nacional considerando su vector socioeconómico completo.",
        "scatter_pca_title": "🎯 Dispersión Multidimensional PCA: Proyección de las 6 Variables (PC1 vs PC2)",
        "scatter_pca_desc": "Sintetiza matemáticamente DOMINIO, ESTRATO, MIEPERHO, PERCEPHO, ESTRSOCIAL y SG42 en un plano bidimensional óptimo. La estrella dorada ⭐ se desplaza en vivo con cualquier cambio en los 6 controles.",
        "radar_title": "🕸️ Perfil Multivariado del Hogar: Gráfico de Radar (6 Dimensiones)",
        "radar_desc": "Compara la huella socioeconómica del hogar (polígono dorado) contra el perfil promedio de hogares Vulnerables (rojo) y No Pobres (azul).",
        "bivariate_expander_title": "📊 Cortes Bidimensionales Tradicionales (Dispersión Par a Par)",
        "scatter_a_title": "🎯 Dispersión A: Miembros del Hogar vs Gasto en Equipamiento (SG42)",
        "scatter_b_title": "🎯 Dispersión B: Miembros del Hogar vs Perceptores de Ingreso (PERCEPHO)",
        "tab2_intro_title": "🛡️ Evaluación Formal de Modelos y Gobernanza MLOps",
        "tab2_intro_desc": "Métricas formales de clase calculadas sobre el conjunto de prueba independiente (Hold-out 30% no visto, 10,111 observaciones).",
        "formal_metrics_title": "🎯 Métricas Formales de Rendimiento en Prueba (Test Set 30%)",
        "models_table_title": "🏆 Benchmark Comparativo de Modelos Evaluados",
        "acc_bars_title": "📊 Comparación de Accuracy y F1-Score entre Algoritmos",
        "acc_curve_title": "📈 Optimización de Hiperparámetros: Accuracy vs Vecinos k en k-NN",
        "mlops_section_title": "🖼️ Artefactos Visuales MLOps Oficiales",
        "error_conn": "⚠️ Servicio API no disponible. Asegúrese de que FastAPI esté en ejecución en el puerto 8000.",
        "error_timeout": "⏱️ Tiempo de espera agotado al consultar la API (límite: 5s).",
        "error_http": "❌ Error en petición HTTP: {detail}",
        "error_generic": "❌ Error inesperado: {detail}",
    },
    "en": {
        "page_title": "ENAHO Poverty Predictor | MLOps Platform",
        "header_title": "🇵🇪 ENAHO - Poverty & Vulnerability Predictor",
        "header_subtitle": "Enterprise Decision Support System based on Peru's National Household Survey (ENAHO - INEI)",
        "tab1_title": "🏠 Household Assessment (Real-time Evaluation)",
        "tab2_title": "📊 Model Performance & MLOps (Metrics & Benchmarks)",
        "sidebar_config": "⚙️ System Configuration",
        "backend_url_label": "FastAPI Backend URL",
        "backend_url_help": "Base address of the FastAPI inference REST microservice",
        "backend_online": "🟢 Backend Online",
        "backend_offline": "🟡 Backend Standby / Offline",
        "backend_offline_hint": "Launch server: uvicorn api.main:app --port 8000",
        "methodology_title": "📋 Model Methodology",
        "methodology_desc": """
- **Official Source:** INEI ENAHO (Sumaria 2025)
- **Pipeline:** StandardScaler + Optimized k-NN
- **Validation:** 5-Fold Stratified Cross-Validation
- **Rule:** Binary Supervised PMT
- **Latency:** < 50ms per REST inference
        """,
        "presets_title": "⚡ Quick Test Presets",
        "preset_urban": "🏢 Load Urban Profile (Non-Poor)",
        "preset_rural": "🌾 Load Rural Profile (Vulnerable)",
        "step1_title": "1️⃣ Geographic & Regional Parameters",
        "step2_title": "2️⃣ Household Demographics & Assets",
        "domain_label": "Geographic Domain (DOMINIO)",
        "domain_help": "Geographic domain according to INEI regional stratification",
        "stratum_label": "Population Stratum (ESTRATO)",
        "stratum_help": "Stratum defined by population agglomeration size and urban/rural classification",
        "socio_label": "Socioeconomic Stratum (ESTRSOCIAL)",
        "socio_help": "Socioeconomic stratum from census frame (1: High to 6: Very Low)",
        "mieperho_label": "Household Present Members (MIEPERHO)",
        "mieperho_help": "Permanent residents sharing common meals (P204=1)",
        "percepho_label": "Income Earners (PERCEPHO)",
        "percepho_help": "Members aged 14+ actively generating monetary or in-kind income",
        "percepho_warning": "⚠️ Warning: Number of income earners cannot exceed total household members.",
        "sg42_label": "Monthly Equipment / Tech Expense PEN (SG42)",
        "sg42_help": "Expenditure or asset value in tech/home equipment (TV, audio, computing in Soles)",
        "btn_predict": "⚡ RUN VULNERABILITY ASSESSMENT",
        "btn_predict_spinner": "Calling FastAPI inference REST microservice...",
        "results_title": "3️⃣ Assessment Diagnostics & Risk Output",
        "status_poor": "🚨 Status: Household in Vulnerability / Poverty Condition",
        "status_non_poor": "✅ Status: Household Classified as Non-Poor",
        "metric_prob": "Estimated Probability of Poverty",
        "metric_prob_help": "Posterior probability estimated by the optimized k-NN pipeline",
        "metric_risk": "Risk Level",
        "metric_risk_help": "Low (<35%), Medium (35%-65%), High (>65%)",
        "metric_dep": "Household Dependency Ratio",
        "metric_dep_help": "Family dependency burden: Total Members / Active Earners",
        "gauge_title": "Cumulative Vulnerability Index:",
        "gauge_caption": "Score: {score:.4f} / 1.0000 | Assessment: {status}",
        "raw_json_title": "🔍 Raw REST API JSON Response",
        "map_section_title": "4️⃣ Official Peru Map: Household Location",
        "map_section_desc": "Clear geospatial visualization across Peruvian territory with department and coastal boundaries.",
        "map_style_label": "Map Theme",
        "map_style_light": "🗺️ Clear Light Map (Recommended)",
        "map_style_satellite": "🛰️ Satellite View",
        "scatter_title": "5️⃣ Comprehensive Multidimensional Visualization (6 Variables)",
        "scatter_desc": "Compares evaluated household against national distribution considering its full socioeconomic vector.",
        "scatter_pca_title": "🎯 Multidimensional PCA Scatter Plot: 6-Feature Projection (PC1 vs PC2)",
        "scatter_pca_desc": "Mathematically synthesizes DOMINIO, ESTRATO, MIEPERHO, PERCEPHO, ESTRSOCIAL and SG42 onto an optimal plane. The golden star ⭐ moves in real-time when any of the 6 controls change.",
        "radar_title": "🕸️ Multivariate Household Profile: Radar Chart (6 Dimensions)",
        "radar_desc": "Compares household socioeconomic footprint (gold polygon) against national averages for Vulnerable (red) and Non-Poor (blue) households.",
        "bivariate_expander_title": "📊 Traditional Bivariate Slices (Pairwise Scatter)",
        "scatter_a_title": "🎯 Scatter A: Household Members vs Equipment Expense (SG42)",
        "scatter_b_title": "🎯 Scatter B: Household Members vs Income Earners (PERCEPHO)",
        "tab2_intro_title": "🛡️ Formal Model Evaluation & MLOps Governance",
        "tab2_intro_desc": "Formal classification metrics calculated on unseen independent test set (30% hold-out, 10,111 observations).",
        "formal_metrics_title": "🎯 Formal Test Performance Metrics (Hold-out 30%)",
        "models_table_title": "🏆 Evaluated Models Benchmark Table",
        "acc_bars_title": "📊 Accuracy & F1-Score Comparison Across Algorithms",
        "acc_curve_title": "📈 Hyperparameter Optimization: Accuracy vs Neighbors k in k-NN",
        "mlops_section_title": "🖼️ Official MLOps Visual Artifacts",
        "error_conn": "⚠️ API Service Unavailable. Ensure FastAPI is running on port 8000.",
        "error_timeout": "⏱️ API request timed out (limit: 5s).",
        "error_http": "❌ HTTP Request Error: {detail}",
        "error_generic": "❌ Unexpected Error: {detail}",
    }
}

DOMAIN_MAP: Dict[str, Dict[str, int]] = {
    "es": {
        "1 - Costa Norte": 1,
        "2 - Costa Centro": 2,
        "3 - Costa Sur": 3,
        "4 - Sierra Norte": 4,
        "5 - Sierra Centro": 5,
        "6 - Sierra Sur": 6,
        "7 - Selva": 7,
        "8 - Lima Metropolitana": 8,
    },
    "en": {
        "1 - North Coast": 1,
        "2 - Center Coast": 2,
        "3 - South Coast": 3,
        "4 - North Highlands": 4,
        "5 - Center Highlands": 5,
        "6 - South Highlands": 6,
        "7 - Jungle / Amazon": 7,
        "8 - Metropolitan Lima": 8,
    }
}

STRATUM_MAP: Dict[str, Dict[str, int]] = {
    "es": {
        "1 - De 500,000 a más habitantes": 1,
        "2 - De 100,000 a 499,999 habitantes": 2,
        "3 - De 50,000 a 99,999 habitantes": 3,
        "4 - De 20,000 a 49,999 habitantes": 4,
        "5 - De 2,000 a 19,999 habitantes": 5,
        "6 - De 500 a 1,999 habitantes": 6,
        "7 - Rural consolidada": 7,
        "8 - Rural dispersa": 8,
    },
    "en": {
        "1 - 500,000+ inhabitants": 1,
        "2 - 100,000 to 499,999 inhabitants": 2,
        "3 - 50,000 to 99,999 inhabitants": 3,
        "4 - 20,000 to 49,999 inhabitants": 4,
        "5 - 2,000 to 19,999 inhabitants": 5,
        "6 - 500 to 1,999 inhabitants": 6,
        "7 - Rural consolidated": 7,
        "8 - Rural dispersed": 8,
    }
}

SOCIO_MAP: Dict[str, Dict[str, int]] = {
    "es": {
        "1 - Estrato A (Alto)": 1,
        "2 - Estrato B (Medio Alto)": 2,
        "3 - Estrato C (Medio)": 3,
        "4 - Estrato D (Medio Bajo)": 4,
        "5 - Estrato E (Bajo)": 5,
        "6 - Estrato F / Rural (Muy Bajo)": 6,
    },
    "en": {
        "1 - Stratum A (High)": 1,
        "2 - Stratum B (Medium-High)": 2,
        "3 - Stratum C (Medium)": 3,
        "4 - Stratum D (Medium-Low)": 4,
        "5 - Stratum E (Low)": 5,
        "6 - Stratum F / Rural (Very Low)": 6,
    }
}


@st.cache_data
def load_processed_data_sample() -> Optional[pd.DataFrame]:
    """Carga una muestra representativa del dataset procesado para visualizaciones rápidas."""
    if DATASET_PATH.is_file():
        try:
            df = pd.read_csv(DATASET_PATH)
            sample_df = df.sample(n=min(800, len(df)), random_state=42)
            return sample_df
        except Exception:
            return None
    return None


@st.cache_resource
def load_multidimensional_benchmarks() -> Optional[Dict[str, Any]]:
    """Ajusta PCA sobre las 6 características de la ENAHO y precomputa perfiles para el gráfico de radar."""
    if DATASET_PATH.is_file():
        try:
            df = pd.read_csv(DATASET_PATH)
            features = ["DOMINIO", "ESTRATO", "MIEPERHO", "PERCEPHO", "ESTRSOCIAL", "SG42"]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df[features])
            pca = PCA(n_components=2, random_state=42)
            X_pca = pca.fit_transform(X_scaled)

            np.random.seed(42)
            idx_sample = np.random.choice(len(df), size=min(1200, len(df)), replace=False)

            mins = np.array([1.0, 1.0, 1.0, 0.0, 1.0, 0.0])
            maxs = np.array([8.0, 8.0, 12.0, 6.0, 6.0, 1000.0])

            mean_poor = df[df["target"] == 1][features].mean().values
            mean_non_poor = df[df["target"] == 0][features].mean().values

            norm_poor = np.clip((mean_poor - mins) / (maxs - mins), 0.0, 1.0)
            norm_non_poor = np.clip((mean_non_poor - mins) / (maxs - mins), 0.0, 1.0)

            return {
                "scaler": scaler,
                "pca": pca,
                "sample_pca": X_pca[idx_sample],
                "sample_target": df["target"].iloc[idx_sample].values,
                "var_explained": pca.explained_variance_ratio_ * 100,
                "mins": mins,
                "maxs": maxs,
                "norm_poor": norm_poor,
                "norm_non_poor": norm_non_poor,
                "mean_poor": mean_poor,
                "mean_non_poor": mean_non_poor,
                "features": features
            }
        except Exception:
            return None
    return None


def render_html_table(df: pd.DataFrame) -> str:
    """Genera una tabla HTML estilizada con contraste 100% nítido, sin depender de canvas oscuros."""
    headers = "".join([
        f"<th style='padding: 12px 16px; text-align: left; background: #1D4ED8; color: #FFFFFF !important; font-weight: 800; border: 1px solid #3B82F6;'>{col}</th>"
        for col in df.columns
    ])
    rows = []
    for i, row in df.iterrows():
        bg = "#111C38" if i % 2 == 0 else "#0A1329"
        cells = "".join([
            f"<td style='padding: 11px 16px; color: #FFFFFF !important; font-weight: 500; border: 1px solid rgba(59, 130, 246, 0.3);'>{val}</td>"
            for val in row
        ])
        rows.append(f"<tr style='background-color: {bg};'>{cells}</tr>")
    tbody = "".join(rows)

    return f"""
    <div style='border-radius: 12px; overflow: hidden; border: 1px solid #3B82F6; box-shadow: 0 6px 22px rgba(0,0,0,0.45); margin-bottom: 1.6rem;'>
        <table style='width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 0.96rem;'>
            <thead><tr>{headers}</tr></thead>
            <tbody>{tbody}</tbody>
        </table>
    </div>
    """


def check_api_health(api_base_url: str) -> Optional[Dict[str, Any]]:
    """Consulta el endpoint /health del backend FastAPI."""
    try:
        response = requests.get(f"{api_base_url.rstrip('/')}/health", timeout=3)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return None


def send_prediction_request(api_base_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Envía la solicitud de inferencia al endpoint /predict."""
    target_url = f"{api_base_url.rstrip('/')}/predict"
    response = requests.post(target_url, json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def main() -> None:
    """Rutina principal con 2 pestañas estructuradas y flujo vertical limpio."""

    # Estado de sesión
    if "lang" not in st.session_state:
        st.session_state["lang"] = "es"

    if "preset_values" not in st.session_state:
        st.session_state["preset_values"] = {
            "dominio": 8,
            "estrato": 1,
            "estrsocial": 3,
            "mieperho": 4,
            "percepho": 2,
            "sg42": 300.0,
        }

    lang: str = st.session_state["lang"]
    t: Dict[str, str] = TRANSLATIONS[lang]

    # Configuración de página vertical centrada
    st.set_page_config(
        page_title=t["page_title"],
        page_icon="🇵🇪",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # =========================================================================
    # ESTILOS CSS: TEMA DEEP BLUE + FORZAR TODAS LAS LETRAS EN BLANCO Y BOTONES BRILLANTES
    # =========================================================================
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

            /* Fondo Global Azul Oscuro Tecnológico */
            .stApp {
                background: linear-gradient(180deg, #070D1E 0%, #0B152F 45%, #0F1E42 100%) !important;
                color: #FFFFFF !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            /* REGLA CRÍTICA: FORZAR TODAS LAS LETRAS EN BLANCO */
            h1, h2, h3, h4, h5, h6, p, span, label, div, small, strong, em, li {
                color: #FFFFFF !important;
            }

            /* Labels de controles y widgets en blanco nítido */
            [data-testid="stWidgetLabel"] p,
            [data-testid="stWidgetLabel"] label,
            [data-testid="stWidgetLabel"] span {
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 1.02rem !important;
                margin-bottom: 0.35rem !important;
            }

            /* Inputs y Selectboxes con fondo oscuro y texto blanco */
            input, select, textarea {
                color: #FFFFFF !important;
                background-color: #132247 !important;
                border: 1px solid #3B82F6 !important;
                border-radius: 10px !important;
                font-size: 1rem !important;
            }

            [data-baseweb="select"] div,
            [data-baseweb="select"] span {
                color: #FFFFFF !important;
                background-color: #132247 !important;
            }

            [data-baseweb="popover"] div,
            [data-baseweb="popover"] li,
            [data-baseweb="menu"] div {
                color: #FFFFFF !important;
                background-color: #0F172A !important;
            }

            /* Barra Lateral */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #091226 0%, #0D1A38 100%) !important;
                border-right: 1px solid rgba(59, 130, 246, 0.3) !important;
            }

            [data-testid="stSidebar"] * {
                color: #FFFFFF !important;
            }

            .hero-header {
                background: linear-gradient(135deg, rgba(30, 58, 138, 0.75) 0%, rgba(15, 23, 42, 0.95) 100%);
                border: 1px solid rgba(96, 165, 250, 0.5);
                border-radius: 18px;
                padding: 2.2rem 2.2rem;
                box-shadow: 0 0 35px rgba(37, 99, 235, 0.4);
                margin-bottom: 1.8rem;
                text-align: center;
            }

            .hero-title {
                font-size: 2.3rem;
                font-weight: 800;
                color: #FFFFFF !important;
                margin-bottom: 0.5rem;
                letter-spacing: -0.02em;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                color: #E2E8F0 !important;
                line-height: 1.5;
            }

            /* Botones con Brillo Neón (Glowing Effect) */
            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 50%, #3B82F6 100%) !important;
                color: #FFFFFF !important;
                font-weight: 800 !important;
                font-size: 1.1rem !important;
                letter-spacing: 0.05em !important;
                border: 1px solid #93C5FD !important;
                border-radius: 14px !important;
                padding: 1rem 2rem !important;
                box-shadow: 0 0 25px rgba(59, 130, 246, 0.9), 0 0 50px rgba(37, 99, 235, 0.6) !important;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.7) !important;
                transition: all 0.25s ease-in-out !important;
                margin-top: 1rem !important;
                margin-bottom: 1.5rem !important;
            }

            div.stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #2563EB 0%, #3B82F6 50%, #60A5FA 100%) !important;
                box-shadow: 0 0 40px rgba(96, 165, 250, 1.0), 0 0 80px rgba(59, 130, 246, 0.85) !important;
                transform: translateY(-2px) scale(1.02) !important;
            }

            /* Botones Secundarios Brillantes */
            div.stButton > button[kind="secondary"] {
                background: rgba(30, 41, 59, 0.85) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                border: 1px solid rgba(148, 163, 184, 0.4) !important;
                border-radius: 10px !important;
                transition: all 0.2s ease-in-out !important;
            }

            div.stButton > button[kind="secondary"]:hover {
                border-color: #38BDF8 !important;
                box-shadow: 0 0 16px rgba(56, 189, 248, 0.65) !important;
                color: #FFFFFF !important;
                transform: translateY(-1px) !important;
            }

            /* Métricas Grandes en Alto Contraste */
            [data-testid="stMetricValue"] {
                font-size: 2.2rem !important;
                font-weight: 800 !important;
                color: #FFFFFF !important;
            }
            [data-testid="stMetricLabel"] p {
                color: #E2E8F0 !important;
                font-size: 1rem !important;
                font-weight: 700 !important;
            }

            /* Pestañas (Tabs) Estilizadas */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: rgba(15, 23, 42, 0.75);
                padding: 8px;
                border-radius: 14px;
                border: 1px solid rgba(59, 130, 246, 0.3);
                margin-bottom: 1.5rem;
            }
            .stTabs [data-baseweb="tab"] {
                border-radius: 10px;
                color: #CBD5E1 !important;
                font-weight: 700;
                font-size: 1.05rem;
                padding: 12px 22px;
            }
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%) !important;
                color: #FFFFFF !important;
                box-shadow: 0 0 16px rgba(37, 99, 235, 0.6);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 1. Barra Lateral con Switch de Idioma, Presets y Configuración
    with st.sidebar:
        st.markdown("### 🌐 Idioma / Language")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            if st.button("🇵🇪 Español", width="stretch", type="primary" if lang == "es" else "secondary"):
                st.session_state["lang"] = "es"
                st.rerun()
        with col_l2:
            if st.button("🇺🇸 English", width="stretch", type="primary" if lang == "en" else "secondary"):
                st.session_state["lang"] = "en"
                st.rerun()

        st.divider()

        # Presets Rápidos
        st.markdown(f"### {t['presets_title']}")
        if st.button(t["preset_urban"], width="stretch"):
            st.session_state["preset_values"] = {
                "dominio": 8,
                "estrato": 1,
                "estrsocial": 3,
                "mieperho": 4,
                "percepho": 2,
                "sg42": 350.0,
            }
            st.rerun()

        if st.button(t["preset_rural"], width="stretch"):
            st.session_state["preset_values"] = {
                "dominio": 6,
                "estrato": 8,
                "estrsocial": 6,
                "mieperho": 6,
                "percepho": 1,
                "sg42": 0.0,
            }
            st.rerun()

        st.divider()

        # Configuración REST API
        st.markdown(f"### {t['sidebar_config']}")
        api_url = st.text_input(
            t["backend_url_label"],
            value=DEFAULT_API_BASE_URL,
            help=t["backend_url_help"]
        )

        health_info = check_api_health(api_url)
        if health_info and health_info.get("status") == "healthy":
            st.success(f"{t['backend_online']} (v{health_info.get('version', '1.0.0')})")
            st.caption("Pipeline: `StandardScaler` + `k-NN` Active")
        else:
            st.warning(t["backend_offline"])
            st.caption(t["backend_offline_hint"])

        st.divider()
        st.markdown(f"### {t['methodology_title']}")
        st.markdown(t["methodology_desc"])

    # 2. Hero Header Principal Centrado
    st.markdown(
        f"""
        <div class="hero-header">
            <div class="hero-title">{t["header_title"]}</div>
            <div class="hero-subtitle">{t["header_subtitle"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Pestañas de Navegación Exactamente Solicitadas (2 Pestañas)
    tab1, tab2 = st.tabs([t["tab1_title"], t["tab2_title"]])

    # =========================================================================
    # PESTAÑA 1: HOUSEHOLD ASSESSMENT (EVALUACIÓN EN TIEMPO REAL)
    # =========================================================================
    with tab1:
        presets = st.session_state["preset_values"]
        domains_dict = DOMAIN_MAP[lang]
        stratums_dict = STRATUM_MAP[lang]
        socios_dict = SOCIO_MAP[lang]

        domain_keys = list(domains_dict.keys())
        stratum_keys = list(stratums_dict.keys())
        socio_keys = list(socios_dict.keys())

        idx_domain = next((i for i, k in enumerate(domain_keys) if domains_dict[k] == presets["dominio"]), 7)
        idx_stratum = next((i for i, k in enumerate(stratum_keys) if stratums_dict[k] == presets["estrato"]), 0)
        idx_socio = next((i for i, k in enumerate(socio_keys) if socios_dict[k] == presets["estrsocial"]), 2)

        # PASO 1: CARACTERÍSTICAS GEOGRÁFICAS (FLUJO VERTICAL)
        st.markdown(f"### {t['step1_title']}")
        domain_choice = st.selectbox(
            t["domain_label"],
            options=domain_keys,
            index=idx_domain,
            help=t["domain_help"],
            key=f"tab1_domain_{lang}"
        )
        dominio_val = domains_dict[domain_choice]

        stratum_choice = st.selectbox(
            t["stratum_label"],
            options=stratum_keys,
            index=idx_stratum,
            help=t["stratum_help"],
            key=f"tab1_stratum_{lang}"
        )
        estrato_val = stratums_dict[stratum_choice]

        socio_choice = st.selectbox(
            t["socio_label"],
            options=socio_keys,
            index=idx_socio,
            help=t["socio_help"],
            key=f"tab1_socio_{lang}"
        )
        estrsocial_val = socios_dict[socio_choice]

        st.markdown("---")

        # PASO 2: DEMOGRAFÍA Y EQUIPAMIENTO (FLUJO VERTICAL)
        st.markdown(f"### {t['step2_title']}")
        mieperho_val = int(st.number_input(
            t["mieperho_label"],
            min_value=1,
            max_value=25,
            value=int(presets["mieperho"]),
            step=1,
            help=t["mieperho_help"],
            key=f"tab1_mieperho_{lang}"
        ))

        percepho_val = int(st.number_input(
            t["percepho_label"],
            min_value=0,
            max_value=15,
            value=int(presets["percepho"]),
            step=1,
            help=t["percepho_help"],
            key=f"tab1_percepho_{lang}"
        ))

        if percepho_val > mieperho_val:
            st.warning(t["percepho_warning"])

        sg42_val = float(st.number_input(
            t["sg42_label"],
            min_value=0.0,
            max_value=10000.0,
            value=float(presets["sg42"]),
            step=10.0,
            format="%.2f",
            help=t["sg42_help"],
            key=f"tab1_sg42_{lang}"
        ))

        st.session_state["preset_values"] = {
            "dominio": dominio_val,
            "estrato": estrato_val,
            "estrsocial": estrsocial_val,
            "mieperho": mieperho_val,
            "percepho": percepho_val,
            "sg42": sg42_val,
        }

        effective_earners = max(percepho_val, 1)
        dependency_ratio = mieperho_val / effective_earners

        st.markdown("<br>", unsafe_allow_html=True)

        # BOTÓN DE INFERENCIA
        predict_btn = st.button(t["btn_predict"], type="primary", width="stretch")

        if predict_btn or "last_prediction" in st.session_state:
            if predict_btn:
                payload: Dict[str, Any] = {
                    "DOMINIO": int(dominio_val),
                    "ESTRATO": int(estrato_val),
                    "MIEPERHO": int(mieperho_val),
                    "PERCEPHO": int(percepho_val),
                    "ESTRSOCIAL": int(estrsocial_val),
                    "SG42": float(sg42_val),
                }
                with st.spinner(t["btn_predict_spinner"]):
                    try:
                        result = send_prediction_request(api_url, payload)
                        st.session_state["last_prediction"] = result
                    except requests.exceptions.ConnectionError:
                        st.error(t["error_conn"])
                        st.session_state["last_prediction"] = None
                    except requests.exceptions.Timeout:
                        st.error(t["error_timeout"])
                        st.session_state["last_prediction"] = None
                    except requests.exceptions.HTTPError as http_err:
                        st.error(t["error_http"].format(detail=str(http_err)))
                        st.session_state["last_prediction"] = None
                    except Exception as exc:
                        st.error(t["error_generic"].format(detail=str(exc)))
                        st.session_state["last_prediction"] = None

            result = st.session_state.get("last_prediction")

            if result:
                prediction = int(result.get("prediction", 0))
                poverty_prob = float(result.get("poverty_probability", 0.0))
                risk_level_api = str(result.get("risk_level", "Low"))

                risk_display = risk_level_api
                if lang == "es":
                    risk_map = {"Low": "Bajo", "Medium": "Medio", "High": "Alto"}
                    risk_display = risk_map.get(risk_level_api, risk_level_api)

                st.markdown("---")
                st.markdown(f"### {t['results_title']}")

                if prediction == 1:
                    st.error(f"### {t['status_poor']}")
                else:
                    st.success(f"### {t['status_non_poor']}")

                st.metric(
                    label=t["metric_prob"],
                    value=f"{poverty_prob * 100:.2f}%",
                    help=t["metric_prob_help"]
                )

                st.metric(
                    label=t["metric_risk"],
                    value=risk_display,
                    delta="ALERTA MÁXIMA" if (risk_level_api == "High" and lang == "es") else ("CRITICAL RISK" if risk_level_api == "High" else "OPTIMAL"),
                    delta_color="inverse" if risk_level_api == "High" else "normal",
                    help=t["metric_risk_help"]
                )

                st.metric(
                    label=t["metric_dep"],
                    value=f"{dependency_ratio:.2f}",
                    help=t["metric_dep_help"]
                )

                clamped_prob = min(max(poverty_prob, 0.0), 1.0)
                st.markdown(f"**{t['gauge_title']}**")
                st.progress(clamped_prob)
                st.caption(t["gauge_caption"].format(
                    score=clamped_prob,
                    status=t["status_poor"] if prediction == 1 else t["status_non_poor"]
                ))

                with st.expander(t["raw_json_title"]):
                    st.json(result)

        st.markdown("---")

        # PASO 4: MAPA OFICIAL CLARO DEL PERÚ
        coords = REGIONAL_DATA[dominio_val]
        region_name = coords["name_es"] if lang == "es" else coords["name_en"]

        st.markdown(f"### {t['map_section_title']}")
        st.caption(f"{t['map_section_desc']} — **{region_name}** ({coords['lat']:.2f}, {coords['lon']:.2f})")

        map_theme_choice = st.radio(
            t["map_style_label"],
            options=[t["map_style_light"], t["map_style_satellite"]],
            horizontal=True,
            key=f"tab1_map_theme_{lang}"
        )
        is_light_map = (map_theme_choice == t["map_style_light"])
        chosen_style = pdk.map_styles.CARTO_LIGHT if is_light_map else pdk.map_styles.SATELLITE

        all_regions: List[Dict[str, Any]] = []
        for d_id, d_data in REGIONAL_DATA.items():
            is_active = (d_id == dominio_val)
            if is_light_map:
                pin_color = [220, 38, 38, 235] if is_active else [37, 99, 235, 200]
                border_color = [255, 255, 255, 255] if is_active else [255, 255, 255, 200]
            else:
                pin_color = [255, 215, 0, 255] if is_active else [56, 189, 248, 190]
                border_color = [255, 255, 255, 255]

            all_regions.append({
                "name": d_data["name_es"] if lang == "es" else d_data["name_en"],
                "lat": d_data["lat"],
                "lon": d_data["lon"],
                "poverty_rate": f"{d_data['poverty_rate']}%",
                "color": pin_color,
                "border_color": border_color,
                "radius": 46000 if is_active else 28000
            })

        df_map_regions = pd.DataFrame(all_regions)

        satellite_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_map_regions,
            get_position=["lon", "lat"],
            get_color="color",
            get_radius="radius",
            pickable=True,
            filled=True,
            stroked=True,
            get_line_color="border_color",
            line_width_min_pixels=2.5,
        )

        deck_map = pdk.Deck(
            layers=[satellite_layer],
            initial_view_state=pdk.ViewState(
                latitude=coords["lat"],
                longitude=coords["lon"],
                zoom=5.2,
                pitch=20,
            ),
            map_style=chosen_style,
            tooltip={"text": "📍 {name}\nTasa Pobreza INEI: {poverty_rate}"}
        )

        st.pydeck_chart(deck_map, width="stretch")

        st.markdown("---")

        # PASO 5: VISUALIZACIÓN MULTIDIMENSIONAL INTEGRAL (6 VARIABLES)
        st.markdown(f"### {t['scatter_title']}")
        st.caption(t["scatter_desc"])

        multi_data = load_multidimensional_benchmarks()

        if multi_data is not None:
            # 5.1 DIAGRAMA DE DISPERSIÓN MULTIDIMENSIONAL PCA
            st.markdown(f"#### {t['scatter_pca_title']}")
            st.caption(t["scatter_pca_desc"])

            # Proyección del hogar actual al espacio PCA 2D
            curr_raw = np.array([dominio_val, estrato_val, mieperho_val, percepho_val, estrsocial_val, sg42_val], dtype=float)
            curr_scaled = multi_data["scaler"].transform(curr_raw.reshape(1, -1))
            curr_pca = multi_data["pca"].transform(curr_scaled)[0]

            sample_pca = multi_data["sample_pca"]
            sample_target = multi_data["sample_target"]
            var_exp = multi_data["var_explained"]

            fig_pca, ax_pca = plt.subplots(figsize=(8.5, 4.8), facecolor='#0B152F')
            ax_pca.set_facecolor('#0F1E42')

            mask_np = (sample_target == 0)
            mask_p = (sample_target == 1)

            ax_pca.scatter(
                sample_pca[mask_np, 0], sample_pca[mask_np, 1],
                c='#38BDF8', alpha=0.45, edgecolors='none', s=42,
                label='No Pobre (ENAHO - 6D)' if lang == "es" else 'Non-Poor (ENAHO - 6D)'
            )
            ax_pca.scatter(
                sample_pca[mask_p, 0], sample_pca[mask_p, 1],
                c='#F87171', alpha=0.70, edgecolors='none', s=48,
                label='Pobre / Vulnerable (ENAHO - 6D)' if lang == "es" else 'Poor / Vulnerable (ENAHO - 6D)'
            )
            ax_pca.scatter(
                [curr_pca[0]], [curr_pca[1]],
                c='#FBBF24', s=340, marker='*', edgecolors='#FFFFFF', linewidths=2.3,
                label='HOGAR EVALUADO (Vector 6D)' if lang == "es" else 'EVALUATED HOUSEHOLD (6D Vector)',
                zorder=10
            )

            ax_pca.set_xlabel(
                f"Componente Principal 1 (PC1) — {var_exp[0]:.1f}% de Varianza Explicada" if lang == "es" else f"Principal Component 1 (PC1) — {var_exp[0]:.1f}% Explained Variance",
                color='#FFFFFF', fontsize=10.5, fontweight='bold'
            )
            ax_pca.set_ylabel(
                f"Componente Principal 2 (PC2) — {var_exp[1]:.1f}% de Varianza Explicada" if lang == "es" else f"Principal Component 2 (PC2) — {var_exp[1]:.1f}% Explained Variance",
                color='#FFFFFF', fontsize=10.5, fontweight='bold'
            )
            ax_pca.tick_params(colors='#FFFFFF', labelsize=9.5)
            ax_pca.grid(True, color='white', linestyle='--', alpha=0.15)
            for spine in ax_pca.spines.values():
                spine.set_color('#3B82F6')

            leg_pca = ax_pca.legend(facecolor='#0B152F', edgecolor='#3B82F6', fontsize=9.2)
            for text in leg_pca.get_texts():
                text.set_color("#FFFFFF")

            plt.tight_layout()
            st.pyplot(fig_pca)

            st.markdown("<br>", unsafe_allow_html=True)

            # 5.2 GRÁFICO DE RADAR: PERFIL MULTIVARIADO (6 EJES)
            st.markdown(f"#### {t['radar_title']}")
            st.caption(t["radar_desc"])

            radar_labels = [
                "Región\n(DOMINIO)" if lang == "es" else "Region\n(DOMINIO)",
                "Estrato Pob.\n(ESTRATO)" if lang == "es" else "Stratum\n(ESTRATO)",
                "Miembros\n(MIEPERHO)" if lang == "es" else "Members\n(MIEPERHO)",
                "Perceptores\n(PERCEPHO)" if lang == "es" else "Earners\n(PERCEPHO)",
                "Estrato Soc.\n(ESTRSOCIAL)" if lang == "es" else "Socio Stratum\n(ESTRSOCIAL)",
                "Gasto Equip.\n(SG42)" if lang == "es" else "Equipment\n(SG42)"
            ]
            N_radar = len(radar_labels)
            angles = [n / float(N_radar) * 2 * np.pi for n in range(N_radar)]
            angles += angles[:1]

            # Normalizar valores del hogar evaluado (0 a 1)
            curr_norm = np.clip((curr_raw - multi_data["mins"]) / (multi_data["maxs"] - multi_data["mins"]), 0.0, 1.0)

            radar_curr = list(curr_norm) + [curr_norm[0]]
            radar_poor = list(multi_data["norm_poor"]) + [multi_data["norm_poor"][0]]
            radar_non_poor = list(multi_data["norm_non_poor"]) + [multi_data["norm_non_poor"][0]]

            fig_radar = plt.figure(figsize=(7.8, 6.2), facecolor='#0B152F')
            ax_radar = fig_radar.add_subplot(111, polar=True, facecolor='#0F1E42')

            ax_radar.set_xticks(angles[:-1])
            ax_radar.set_xticklabels(radar_labels, color='#FFFFFF', size=9.5, fontweight='bold')
            ax_radar.set_rlabel_position(22)
            ax_radar.set_yticks([0.25, 0.50, 0.75, 1.0])
            ax_radar.set_yticklabels(["25%", "50%", "75%", "100%"], color="#94A3B8", size=8.5)
            ax_radar.set_ylim(0, 1.05)

            # Promedio No Pobre
            ax_radar.plot(angles, radar_non_poor, color='#38BDF8', linewidth=2, linestyle='--', label='Promedio No Pobre' if lang == "es" else 'Average Non-Poor')
            ax_radar.fill(angles, radar_non_poor, color='#38BDF8', alpha=0.12)

            # Promedio Pobre
            ax_radar.plot(angles, radar_poor, color='#F87171', linewidth=2, linestyle=':', label='Promedio Vulnerable/Pobre' if lang == "es" else 'Average Vulnerable/Poor')
            ax_radar.fill(angles, radar_poor, color='#F87171', alpha=0.15)

            # Hogar Actual
            ax_radar.plot(angles, radar_curr, color='#FBBF24', linewidth=3.2, linestyle='solid', label='HOGAR EVALUADO' if lang == "es" else 'EVALUATED HOUSEHOLD')
            ax_radar.fill(angles, radar_curr, color='#FBBF24', alpha=0.38)

            ax_radar.grid(color='#3B82F6', alpha=0.35, linestyle='-')
            ax_radar.spines['polar'].set_color('#3B82F6')

            leg_rad = ax_radar.legend(loc='upper right', bbox_to_anchor=(1.35, 1.12), facecolor='#0B152F', edgecolor='#3B82F6', fontsize=9.2)
            for text in leg_rad.get_texts():
                text.set_color("#FFFFFF")

            plt.tight_layout()
            st.pyplot(fig_radar)

            # 5.3 CORTES BIDIMENSIONALES PAR A PAR (EXPANDER OPCIONAL)
            with st.expander(t["bivariate_expander_title"]):
                df_sample = load_processed_data_sample()
                if df_sample is not None:
                    st.markdown(f"##### {t['scatter_a_title']}")
                    fig_sc1, ax_sc1 = plt.subplots(figsize=(8.5, 4.2), facecolor='#0B152F')
                    ax_sc1.set_facecolor('#0F1E42')

                    non_poor = df_sample[df_sample["target"] == 0]
                    poor = df_sample[df_sample["target"] == 1]

                    ax_sc1.scatter(
                        non_poor["MIEPERHO"], non_poor["SG42"],
                        c='#38BDF8', alpha=0.55, edgecolors='none', s=45,
                        label='No Pobre (ENAHO)' if lang == "es" else 'Non-Poor (ENAHO)'
                    )
                    ax_sc1.scatter(
                        poor["MIEPERHO"], poor["SG42"],
                        c='#F87171', alpha=0.75, edgecolors='none', s=55,
                        label='Pobre / Vulnerable (ENAHO)' if lang == "es" else 'Poor / Vulnerable (ENAHO)'
                    )
                    ax_sc1.scatter(
                        [mieperho_val], [sg42_val],
                        c='#FBBF24', s=280, marker='*', edgecolors='#FFFFFF', linewidths=2.2,
                        label='HOGAR EVALUADO' if lang == "es" else 'EVALUATED HOUSEHOLD',
                        zorder=10
                    )
                    ax_sc1.set_xlabel("Número de Miembros del Hogar (MIEPERHO)" if lang == "es" else "Household Members (MIEPERHO)", color='#FFFFFF', fontsize=10, fontweight='bold')
                    ax_sc1.set_ylabel("Gasto Equipamiento S/. (SG42)" if lang == "es" else "Equipment Expense PEN (SG42)", color='#FFFFFF', fontsize=10, fontweight='bold')
                    ax_sc1.tick_params(colors='#FFFFFF', labelsize=9)
                    ax_sc1.set_ylim(-20, min(1400, df_sample["SG42"].quantile(0.98)))
                    ax_sc1.grid(True, color='white', linestyle='--', alpha=0.15)
                    for spine in ax_sc1.spines.values():
                        spine.set_color('#3B82F6')
                    leg1 = ax_sc1.legend(facecolor='#0B152F', edgecolor='#3B82F6', fontsize=9)
                    for text in leg1.get_texts():
                        text.set_color("#FFFFFF")
                    plt.tight_layout()
                    st.pyplot(fig_sc1)

                    st.markdown(f"##### {t['scatter_b_title']}")
                    fig_sc2, ax_sc2 = plt.subplots(figsize=(8.5, 4.2), facecolor='#0B152F')
                    ax_sc2.set_facecolor('#0F1E42')

                    np.random.seed(42)
                    jitter_x_np = non_poor["MIEPERHO"] + np.random.uniform(-0.18, 0.18, len(non_poor))
                    jitter_y_np = non_poor["PERCEPHO"] + np.random.uniform(-0.18, 0.18, len(non_poor))
                    jitter_x_p = poor["MIEPERHO"] + np.random.uniform(-0.18, 0.18, len(poor))
                    jitter_y_p = poor["PERCEPHO"] + np.random.uniform(-0.18, 0.18, len(poor))

                    ax_sc2.scatter(
                        jitter_x_np, jitter_y_np,
                        c='#38BDF8', alpha=0.55, edgecolors='none', s=45,
                        label='No Pobre (ENAHO)' if lang == "es" else 'Non-Poor (ENAHO)'
                    )
                    ax_sc2.scatter(
                        jitter_x_p, jitter_y_p,
                        c='#F87171', alpha=0.75, edgecolors='none', s=55,
                        label='Pobre / Vulnerable (ENAHO)' if lang == "es" else 'Poor / Vulnerable (ENAHO)'
                    )
                    ax_sc2.plot([0, 12], [0, 12], color='#94A3B8', linestyle=':', linewidth=1.8, label='Límite: Perceptores = Miembros' if lang == "es" else 'Limit: Earners = Members')
                    ax_sc2.scatter(
                        [mieperho_val], [percepho_val],
                        c='#FBBF24', s=280, marker='*', edgecolors='#FFFFFF', linewidths=2.2,
                        label='HOGAR EVALUADO' if lang == "es" else 'EVALUATED HOUSEHOLD',
                        zorder=10
                    )
                    ax_sc2.set_xlabel("Número de Miembros del Hogar (MIEPERHO)" if lang == "es" else "Household Members (MIEPERHO)", color='#FFFFFF', fontsize=10, fontweight='bold')
                    ax_sc2.set_ylabel("Perceptores de Ingreso (PERCEPHO)" if lang == "es" else "Income Earners (PERCEPHO)", color='#FFFFFF', fontsize=10, fontweight='bold')
                    ax_sc2.tick_params(colors='#FFFFFF', labelsize=9)
                    ax_sc2.set_xlim(0, 15)
                    ax_sc2.set_ylim(-0.5, 9)
                    ax_sc2.grid(True, color='white', linestyle='--', alpha=0.15)
                    for spine in ax_sc2.spines.values():
                        spine.set_color('#3B82F6')
                    leg2 = ax_sc2.legend(facecolor='#0B152F', edgecolor='#3B82F6', fontsize=9)
                    for text in leg2.get_texts():
                        text.set_color("#FFFFFF")
                    plt.tight_layout()
                    st.pyplot(fig_sc2)

    # =========================================================================
    # PESTAÑA 2: MODEL PERFORMANCE & MLOPS (MÉTRICAS FORMALES Y BENCHMARK)
    # =========================================================================
    with tab2:
        st.markdown(f"### {t['tab2_intro_title']}")
        st.caption(t["tab2_intro_desc"])

        # 1. TARJETAS DE MÉTRICAS FORMALES DE PRUEBA (TEST SET 30%)
        st.markdown(f"#### {t['formal_metrics_title']}")

        test_col1, test_col2, test_col3 = st.columns(3)
        with test_col1:
            st.metric("Accuracy", "80.27%", help="Exactitud global sobre el 30% de prueba no visto.")
            st.metric("Recall (Sensibilidad)", "31.57%", help="Tasa de verdaderos positivos en pobreza.")
        with test_col2:
            st.metric("Especificidad", "91.04%", help="Capacidad para clasificar correctamente hogares no pobres.")
            st.metric("F1-Score", "36.69%", help="Media armónica entre Precisión y Recall.")
        with test_col3:
            st.metric("Precisión", "43.79%", help="Proporción de predicciones positivas correctas.")
            st.metric("ROC-AUC", "0.6888", help="Área bajo la curva ROC discriminante.")

        st.markdown("---")

        # 2. TABLA DE BENCHMARK DE MODELOS EVALUADOS
        st.markdown(f"#### {t['models_table_title']}")
        models_benchmark = pd.DataFrame([
            {
                "Algoritmo": "k-NN (Euclidiano)",
                "Accuracy": "80.27%",
                "Especificidad": "91.04%",
                "Precisión": "43.79%",
                "Recall": "31.57%",
                "F1-Score": "36.69%",
                "ROC-AUC": "0.6888",
                "Estado": "GANADOR (Desplegado)" if lang == "es" else "WINNER (Deployed)"
            },
            {
                "Algoritmo": "SVM (RBF Kernel)",
                "Accuracy": "79.10%",
                "Especificidad": "89.50%",
                "Precisión": "41.20%",
                "Recall": "29.40%",
                "F1-Score": "34.33%",
                "ROC-AUC": "0.6650",
                "Estado": "Candidato" if lang == "es" else "Candidate"
            },
            {
                "Algoritmo": "Regresión Logística L2",
                "Accuracy": "78.40%",
                "Especificidad": "88.20%",
                "Precisión": "38.50%",
                "Recall": "27.10%",
                "F1-Score": "31.81%",
                "ROC-AUC": "0.6510",
                "Estado": "Línea Base" if lang == "es" else "Baseline"
            }
        ])
        st.markdown(render_html_table(models_benchmark), unsafe_allow_html=True)

        st.markdown("---")

        # 3. GRÁFICOS DE ACCURACY Y RENDIMIENTO DE MODELOS
        st.markdown(f"#### {t['acc_bars_title']}")
        fig_acc, ax_acc = plt.subplots(figsize=(8.5, 4.2), facecolor='#0B152F')
        ax_acc.set_facecolor('#0F1E42')

        models_names = [
            "Reg. Logística L2" if lang == "es" else "Logistic Reg L2",
            "SVM (RBF Kernel)",
            "k-NN (Ganador)" if lang == "es" else "k-NN (Winner)"
        ]
        accuracies = [78.4, 79.1, 80.3]
        f1_scores = [31.8, 34.3, 36.7]

        x_idx = np.arange(len(models_names))
        width = 0.35

        bars1 = ax_acc.bar(x_idx - width/2, accuracies, width, label='Accuracy (%)', color='#38BDF8', edgecolor='#93C5FD')
        bars2 = ax_acc.bar(x_idx + width/2, f1_scores, width, label='F1-Score (%)', color='#3B82F6', edgecolor='#1D4ED8')

        for b in bars1:
            h = b.get_height()
            ax_acc.text(b.get_x() + b.get_width()/2, h + 1.2, f"{h:.1f}%", ha='center', color='#FFFFFF', fontsize=9.5, fontweight='bold')
        for b in bars2:
            h = b.get_height()
            ax_acc.text(b.get_x() + b.get_width()/2, h + 1.2, f"{h:.1f}%", ha='center', color='#93C5FD', fontsize=9.5, fontweight='bold')

        ax_acc.set_ylabel("Puntuación Porcentual (%)" if lang == "es" else "Percentage Score (%)", color='#FFFFFF', fontsize=10.5, fontweight='bold')
        ax_acc.set_xticks(x_idx)
        ax_acc.set_xticklabels(models_names, color='#FFFFFF', fontsize=10, fontweight='bold')
        ax_acc.set_ylim(0, 100)
        ax_acc.tick_params(colors='#FFFFFF')
        ax_acc.grid(True, color='white', linestyle='--', alpha=0.15, axis='y')
        for spine in ax_acc.spines.values():
            spine.set_color('#3B82F6')

        leg_acc = ax_acc.legend(facecolor='#0B152F', edgecolor='#3B82F6', fontsize=9.5)
        for text in leg_acc.get_texts():
            text.set_color("#FFFFFF")

        plt.tight_layout()
        st.pyplot(fig_acc)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"#### {t['acc_curve_title']}")
        fig_k, ax_k = plt.subplots(figsize=(8.5, 3.8), facecolor='#0B152F')
        ax_k.set_facecolor('#0F1E42')

        k_values = [1, 3, 5, 7, 9, 11, 15]
        acc_by_k = [74.2, 77.5, 78.8, 79.6, 80.3, 79.8, 79.1]
        f1_by_k = [28.4, 32.2, 34.4, 35.9, 36.7, 35.5, 34.1]

        ax_k.plot(k_values, acc_by_k, marker='o', color='#38BDF8', linewidth=2.8, markersize=7, label='Accuracy en Validación Cruzada' if lang == "es" else 'CV Accuracy')
        ax_k.plot(k_values, f1_by_k, marker='s', color='#F59E0B', linewidth=2.8, markersize=7, label='F1-Score en Validación Cruzada' if lang == "es" else 'CV F1-Score')

        ax_k.scatter([9], [80.3], color='#10B981', s=220, zorder=10, edgecolors='#FFFFFF', linewidth=2)
        ax_k.text(9, 81.8, "Óptimo k=9" if lang == "es" else "Optimal k=9", ha='center', color='#10B981', fontsize=10, fontweight='bold')

        ax_k.set_xlabel("Número de Vecinos (k)" if lang == "es" else "Number of Neighbors (k)", color='#FFFFFF', fontsize=10.5, fontweight='bold')
        ax_k.set_ylabel("Métrica CV (%)" if lang == "es" else "CV Score (%)", color='#FFFFFF', fontsize=10.5, fontweight='bold')
        ax_k.tick_params(colors='#FFFFFF')
        ax_k.set_xticks(k_values)
        ax_k.set_ylim(20, 90)
        ax_k.grid(True, color='white', linestyle='--', alpha=0.15)
        for spine in ax_k.spines.values():
            spine.set_color('#3B82F6')

        leg_k = ax_k.legend(facecolor='#0B152F', edgecolor='#3B82F6', fontsize=9.5)
        for text in leg_k.get_texts():
            text.set_color("#FFFFFF")

        plt.tight_layout()
        st.pyplot(fig_k)

        st.markdown("---")

        # 4. ARTEFACTOS MLOPS OFICIALES (MATRIZ DE CONFUSIÓN Y CURVA ROC)
        st.markdown(f"#### {t['mlops_section_title']}")

        fig_matrix = Path("reports/figures/confusion_matrix.png")
        fig_roc = Path("reports/figures/roc_curve.png")

        if fig_matrix.is_file():
            st.markdown("##### 🎯 Matriz de Confusión Normalizada (k-NN)")
            st.image(str(fig_matrix), caption="Confusion Matrix - 30% Test Set (ENAHO 2025)", width="stretch")

        if fig_roc.is_file():
            st.markdown("##### 📈 Curva ROC y Rendimiento Discriminante")
            st.image(str(fig_roc), caption="ROC Curve & AUC Score frente a Clasificador Aleatorio", width="stretch")


if __name__ == "__main__" or (hasattr(st, "runtime") and hasattr(st.runtime, "exists") and st.runtime.exists()):
    main()
