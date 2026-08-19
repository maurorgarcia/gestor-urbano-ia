import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import re

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Gestor Urbano IA — Centro de Operaciones Municipal",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# SISTEMA DE DISEÑO CSS — PREMIUM UX/UI
# ==============================================================================
st.markdown("""
<style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Base Typography ── */
    html, body, [class*="css"], .stMarkdown, .stText, label, .stSelectbox, .stTextInput {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hero Header ── */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0f2027 70%, #203a43 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.07);
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(59,130,246,0.12) 0%, transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(16,185,129,0.08) 0%, transparent 50%);
        animation: aurora 8s ease-in-out infinite alternate;
    }
    @keyframes aurora {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(3%, 3%) rotate(3deg); }
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa, #34d399, #60a5fa);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shine 4s linear infinite;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.6);
        font-size: 0.9rem;
        font-weight: 400;
        margin-top: 0.4rem;
        position: relative;
        z-index: 1;
        letter-spacing: 0.01em;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(34,197,94,0.15);
        border: 1px solid rgba(34,197,94,0.35);
        color: #4ade80;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        position: relative;
        z-index: 1;
    }
    .hero-badge::before {
        content: '';
        width: 7px;
        height: 7px;
        background: #4ade80;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.7); }
    }

    /* ── KPI Cards — Glassmorphism ── */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1.3rem 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        margin-bottom: 0.8rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
        animation: fadeInUp 0.5s ease both;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,0.15);
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .kpi-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: rgba(255,255,255,0.45);
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 900;
        line-height: 1;
        background: linear-gradient(135deg, #e2e8f0, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .kpi-value-red {
        background: linear-gradient(135deg, #f87171, #ef4444) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    .kpi-value-blue {
        background: linear-gradient(135deg, #93c5fd, #3b82f6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    .kpi-value-green {
        background: linear-gradient(135deg, #6ee7b7, #10b981) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    .kpi-unit {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.35);
        margin-top: 0.2rem;
    }

    /* ── Priority Chips ── */
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 0.28rem 0.85rem;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .chip-critica {
        background: rgba(239,68,68,0.15);
        color: #f87171;
        border: 1px solid rgba(239,68,68,0.35);
    }
    .chip-alta {
        background: rgba(249,115,22,0.15);
        color: #fb923c;
        border: 1px solid rgba(249,115,22,0.35);
    }
    .chip-media {
        background: rgba(234,179,8,0.15);
        color: #facc15;
        border: 1px solid rgba(234,179,8,0.35);
    }
    .chip-baja {
        background: rgba(34,197,94,0.15);
        color: #4ade80;
        border: 1px solid rgba(34,197,94,0.35);
    }

    /* ── Resultado / Diagnostic Card ── */
    .result-card {
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        animation: fadeInUp 0.4s ease both;
    }
    .result-card-critica { border-left: 4px solid #ef4444; }
    .result-card-alta    { border-left: 4px solid #f97316; }
    .result-card-media   { border-left: 4px solid #eab308; }
    .result-card-baja    { border-left: 4px solid #22c55e; }

    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    .result-ticket-id {
        font-size: 1.4rem;
        font-weight: 800;
        color: #f1f5f9;
        font-family: 'Inter', monospace;
    }
    .result-meta {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        margin: 0.8rem 0;
    }
    .result-meta-item {
        background: rgba(255,255,255,0.04);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        font-size: 0.82rem;
    }
    .result-meta-label {
        color: rgba(255,255,255,0.4);
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    .result-meta-value {
        color: #e2e8f0;
        font-weight: 600;
        margin-top: 0.15rem;
    }

    /* ── Stepper de Acciones ── */
    .stepper {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        margin: 0.8rem 0;
    }
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    .step-number {
        min-width: 26px;
        height: 26px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
        font-size: 0.72rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .step-text {
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.5;
        padding-top: 2px;
    }
    .step-connector {
        width: 2px;
        height: 12px;
        background: linear-gradient(to bottom, #3b82f6, transparent);
        margin-left: 12px;
    }

    /* ── Burbuja WhatsApp ── */
    .whatsapp-bubble {
        background: linear-gradient(135deg, #075e54, #128c7e);
        border-radius: 4px 18px 18px 18px;
        padding: 1rem 1.2rem;
        font-size: 0.9rem;
        color: #e9f5f3;
        line-height: 1.6;
        position: relative;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: fadeInUp 0.4s ease both;
    }
    .whatsapp-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.6rem;
        font-size: 0.72rem;
        color: #4ade80;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .whatsapp-tick {
        font-size: 0.75rem;
        color: #4ade80;
        margin-top: 0.4rem;
        text-align: right;
    }

    /* ── Motor Badge ── */
    .motor-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.3);
        color: #a5b4fc;
        padding: 0.25rem 0.7rem;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* ── Sidebar Enhancements ── */
    .sidebar-stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .sidebar-stat-label {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.5);
        font-weight: 500;
    }
    .sidebar-stat-value {
        font-size: 1.1rem;
        font-weight: 800;
        color: #f1f5f9;
    }

    /* ── Section Labels ── */
    .section-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
        color: rgba(255,255,255,0.35);
        margin-bottom: 0.5rem;
    }

    /* ── Resumen Executive Box ── */
    .exec-box {
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.2);
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        font-size: 0.88rem;
        color: #bfdbfe;
        line-height: 1.5;
        font-style: italic;
        margin: 0.5rem 0;
    }

    /* ── Progress Bar ── */
    .progress-bar-wrap {
        background: rgba(255,255,255,0.06);
        border-radius: 50px;
        height: 8px;
        overflow: hidden;
        margin-top: 0.4rem;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 50px;
        background: linear-gradient(90deg, #10b981, #34d399);
        transition: width 1s ease;
    }
</style>
""", unsafe_allow_html=True)

# Librerías de IA
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False

# ==============================================================================
# PROMPT DEL SISTEMA MUNICIPAL
# ==============================================================================
PROMPT_SISTEMA = """Sos el motor de Inteligencia Artificial del sistema municipal "Gestor Urbano IA".
Tu tarea es procesar el texto libre de un reclamo vecinal y devolver un JSON estricto con el siguiente esquema exacto:

{
  "categoria": "Infraestructura Vial | Alumbrado Público | Higiene Urbana | Espacios Verdes | Riesgo Eléctrico / Emergencia | Tránsito y Señalización | Red Pluvial y Cloacas | Zoonosis y Control Animal",
  "subcategoria": "Nombre técnico y específico del problema (ej: Bacheo profundo, Cables con descarga, Microbasural crónico, Semáforo fuera de servicio, Poda de despeje)",
  "prioridad": "Crítica | Alta | Media | Baja",
  "justificacion_prioridad": "Explicación técnica de 1 frase del por qué de la urgencia asignada",
  "area_responsable": "Nombre formal de la secretaría o dirección municipal competente",
  "cuadrilla_sugerida": "Tipo de equipo operativo necesario (ej: Cuadrilla de Emergencias Viales, Cuadrilla de Alumbrado y Alta Tensión, Móvil de Zoonosis)",
  "recursos_necesarios": [
    "Recurso o equipamiento 1 (ej: Camión con hidroelevador)",
    "Recurso 2 (ej: Cinta de vallado y balizas)",
    "Recurso 3 (ej: Asfalto en frío / Motosierra)"
  ],
  "sla_horas": 24,
  "resumen_ejecutivo": "Resumen técnico de 1 frase para la orden de trabajo de la cuadrilla",
  "acciones_recomendadas": [
    "Paso 1 operativo inmediato",
    "Paso 2 operativo de resolución",
    "Paso 3 de verificación o cierre"
  ],
  "ubicacion_detectada": "Dirección, esquina o punto de referencia extraído del texto, o 'A coordinar con el vecino'",
  "mensaje_ciudadano": "Mensaje formal, empático y cordial para enviar al vecino (WhatsApp/SMS), indicando que su reclamo fue registrado, clasificado y derivado, mencionando el tiempo estimado."
}

CRITERIOS ESTRICTOS DE PRIORIDAD:
- Crítica (SLA 2-6 hs): Riesgo inminente para la vida o integridad física (cables cortados con chispas, derrumbes, escapes de gas, pozo ciego abierto, corte total de avenida principal).
- Alta (SLA 12-24 hs): Bache profundo frente a escuelas/hospitales, semáforo apagado en intersección peligrosa, tapa de alcantarilla faltante, rama de gran porte a punto de caer.
- Media (SLA 48-72 hs): Microbasurales, luminarias quemadas en calles residenciales, baches menores en calles secundarias, desmalezado en plazas.
- Baja (SLA 96-120 hs): Tareas programadas de embellecimiento, pintura de sendas peatonales, mantenimiento de juegos de plaza, corte de pasto preventivo.

Respondé ÚNICAMENTE con el objeto JSON válido, sin delimitadores innecesarios ni texto introductorio."""

# ==============================================================================
# INICIALIZACIÓN DEL DATASET SEMILLA (SESSION STATE)
# ==============================================================================
def inicializar_dataset():
    if "reclamos" not in st.session_state:
        st.session_state.reclamos = [
            {
                "id": "TKT-1041",
                "fecha": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
                "descripcion": "Cables de alta tensión cortados y echando chispas sobre la vereda tras la tormenta en Av. Colón 1450. Hay peligro para los peatones.",
                "categoria": "Riesgo Eléctrico / Emergencia",
                "subcategoria": "Cables con descarga en vía pública",
                "prioridad": "Crítica",
                "justificacion": "Riesgo inminente de electrocución para vecinos y transeúntes.",
                "area": "Defensa Civil y Alumbrado Público",
                "cuadrilla": "Móvil de Respuesta Rápida y Emergencias",
                "recursos": ["Móvil 4x4", "Cinta de clausura perimetral", "Herramientas aisladas 1000V"],
                "sla_horas": 4,
                "resumen": "Cables de media/alta tensión con chispa en vereda de Av. Colón 1450.",
                "acciones": ["Cordonar 50m a la redonda", "Cortar fase con distribuidora", "Reparación y aislación del tramo"],
                "ubicacion": "Av. Colón 1450",
                "estado": "En Cuadrilla",
                "canal": "Línea 147 (Telefónico)",
                "mensaje_vecino": "Estimado/a vecino/a: Su reporte urgente por cables en Av. Colón 1450 fue asignado a Defensa Civil con máxima prioridad (SLA: 4 hs). Móvil en camino."
            },
            {
                "id": "TKT-1040",
                "fecha": (datetime.now() - timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"),
                "descripcion": "Pozo de 40cm de profundidad en calle San Martín 850 justo frente a la puerta del colegio primario. Los autos y colectivos tienen que frenar a cero.",
                "categoria": "Infraestructura Vial",
                "subcategoria": "Bacheo profundo en zona escolar",
                "prioridad": "Alta",
                "justificacion": "Afecta la seguridad vial y peatonal en horario escolar con alto flujo vehicular.",
                "area": "Secretaría de Obras Viales y Pavimentación",
                "cuadrilla": "Cuadrilla de Asfalto y Bacheo Rápido",
                "recursos": ["Camión volcador", "Mezcla asfáltica en caliente", "Rodillo compactador", "Conos reflectivos"],
                "sla_horas": 24,
                "resumen": "Bache profundo frente al colegio primario en San Martín 850.",
                "acciones": ["Señalización con vallas", "Fresado y limpieza del pozo", "Relleno y compactación asfáltica"],
                "ubicacion": "San Martín 850",
                "estado": "Pendiente",
                "canal": "App Móvil Ciudadana",
                "mensaje_vecino": "Hola. Hemos registrado el reporte del bache en San Martín 850. La cuadrilla de Obras Viales fue notificada para intervenir dentro de las próximas 24 hs."
            },
            {
                "id": "TKT-1039",
                "fecha": (datetime.now() - timedelta(hours=14)).strftime("%Y-%m-%d %H:%M"),
                "descripcion": "Semáforo de la esquina de Av. Rivadavia y Belgrano quedó tildado en luz amarilla intermitente desde ayer.",
                "categoria": "Tránsito y Señalización",
                "subcategoria": "Semáforo fuera de servicio",
                "prioridad": "Alta",
                "justificacion": "Cruce de avenidas principales sin control semafórico incrementa riesgo de colisiones.",
                "area": "Dirección de Ingeniería de Tránsito",
                "cuadrilla": "Equipo Técnico Semafórico",
                "recursos": ["Móvil técnico", "Plaquetas de repuesto", "Equipo de medición electrónica"],
                "sla_horas": 12,
                "resumen": "Semáforo desincronizado en amarillo en Rivadavia y Belgrano.",
                "acciones": ["Presencia de inspector de tránsito", "Reinicio y reemplazo de plaqueta", "Prueba de ciclo completo"],
                "ubicacion": "Av. Rivadavia y Belgrano",
                "estado": "En Cuadrilla",
                "canal": "Mesa de Entradas",
                "mensaje_vecino": "Su reclamo sobre el semáforo de Rivadavia y Belgrano está en proceso. Técnicos están sincronizando el controlador."
            },
            {
                "id": "TKT-1038",
                "fecha": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                "descripcion": "Acumulación de bolsas de basura y ramas en la esquina de Jujuy y Mitre desde hace 4 días con olores molestos.",
                "categoria": "Higiene Urbana",
                "subcategoria": "Microbasural y restos de poda",
                "prioridad": "Media",
                "justificacion": "Foco de contaminación e insalubridad en área residencial.",
                "area": "Secretaría de Servicios Públicos e Higiene",
                "cuadrilla": "Cuadrilla de Recolección Especializada",
                "recursos": ["Camión compactador", "Pala mecánica", "Kit de desinfección"],
                "sla_horas": 48,
                "resumen": "Microbasural en esquina Jujuy y Mitre.",
                "acciones": ["Retiro de residuos con pala mecánica", "Barrido manual", "Fumigación del perímetro"],
                "ubicacion": "Jujuy y Mitre",
                "estado": "Resuelto",
                "canal": "WhatsApp Municipal",
                "mensaje_vecino": "Le informamos que el microbasural en Jujuy y Mitre fue retirado y el área desinfectada. ¡Gracias por avisarnos!"
            },
            {
                "id": "TKT-1037",
                "fecha": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
                "descripcion": "Luminaria pública apagada en calle Las Heras 320. La cuadra queda muy oscura de noche.",
                "categoria": "Alumbrado Público",
                "subcategoria": "Recambio de lámpara LED",
                "prioridad": "Media",
                "justificacion": "Disminución de visibilidad y prevención de seguridad comunitaria.",
                "area": "Dirección de Alumbrado y Electromecánica",
                "cuadrilla": "Móvil con Hidroelevador",
                "recursos": ["Camión grúa canasta", "Luminaria LED 150W", "Fotocélula"],
                "sla_horas": 48,
                "resumen": "Foco apagado en Las Heras 320.",
                "acciones": ["Verificación de tensión en poste", "Reemplazo por luminaria LED", "Prueba de fotocontrol"],
                "ubicacion": "Las Heras 320",
                "estado": "Resuelto",
                "canal": "Portal Web",
                "mensaje_vecino": "Su reporte por luminaria en Las Heras 320 fue resuelto exitosamente con recambio a tecnología LED."
            },
            {
                "id": "TKT-1036",
                "fecha": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
                "descripcion": "El pasto en la plaza del barrio está alto y convendría pintar los juegos infantiles que tienen pintura descascarada.",
                "categoria": "Espacios Verdes",
                "subcategoria": "Mantenimiento general de plaza",
                "prioridad": "Baja",
                "justificacion": "Mantenimiento estético y recreativo sin riesgo operativo inmediato.",
                "area": "Dirección de Parques y Espacios Verdes",
                "cuadrilla": "Cuadrilla de Jardinería y Mantenimiento Urbano",
                "recursos": ["Motoguadañas", "Pintura sintética para exteriores", "Rastrillos y bolsas de biomasa"],
                "sla_horas": 96,
                "resumen": "Corte de pasto y pintura en plaza barrial.",
                "acciones": ["Desmalezado perimetral", "Lijado y pintura de juegos", "Recolección de restos verdes"],
                "ubicacion": "Plaza Barrio Centro",
                "estado": "Pendiente",
                "canal": "Portal Web",
                "mensaje_vecino": "Gracias por su sugerencia. La puesta en valor de la plaza fue programada en el cronograma semanal de Espacios Verdes."
            }
        ]

inicializar_dataset()

# ==============================================================================
# MOTORES DE IA: GEMINI Y HEURÍSTICO AVANZADO
# ==============================================================================
def clasificar_con_gemini(texto: str, api_key: str, modelo_nombre: str = "gemini-1.5-flash") -> dict:
    """Invoca la API oficial de Google Gemini con salida estructurada en JSON."""
    if not GENAI_AVAILABLE:
        raise Exception("El paquete google-generativeai no está instalado.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=modelo_nombre,
        generation_config={
            "temperature": 0.1,
            "top_p": 0.95,
            "response_mime_type": "application/json",
        },
        system_instruction=PROMPT_SISTEMA
    )
    response = model.generate_content(f"Reclamo ciudadano:\n\"\"\"{texto}\"\"\"")
    raw = response.text.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return json.loads(raw.strip())


def clasificar_heuristico(texto: str) -> dict:
    """Motor inteligente offline con procesamiento de lenguaje y reglas especializadas."""
    t = texto.lower()

    if any(k in t for k in ["cable", "chispa", "electrocu", "fuego", "derrumbe", "gas", "peligro", "muerte", "chispas"]):
        categoria = "Riesgo Eléctrico / Emergencia"
        subcategoria = "Cables caídos o riesgo estructural"
        prioridad = "Crítica"
        justificacion = "Riesgo inminente de daño físico o electrocución en vía pública."
        area = "Defensa Civil y Alumbrado Público"
        cuadrilla = "Móvil de Intervención Rápida y Emergencias"
        recursos = ["Móvil 4x4", "Cintas de clausura de peligro", "Herramientas dieléctricas"]
        sla = 4
        acciones = [
            "Despacho prioritario de móvil de Defensa Civil",
            "Cordonar y aislar el perímetro peatonal",
            "Coordinar corte preventivo con la empresa de energía eléctrica"
        ]
    elif any(k in t for k in ["pozo", "bache", "asfalto", "calle rota", "cordon", "pavimento", "vereda"]):
        es_urgente = any(x in t for x in ["escuela", "colegio", "hospital", "grande", "colectivo", "profundo", "avenida"])
        categoria = "Infraestructura Vial"
        subcategoria = "Bacheo profundo en calzada" if es_urgente else "Reparación de calzada / Bache menor"
        prioridad = "Alta" if es_urgente else "Media"
        justificacion = "Afecta la seguridad de tránsito vehicular y transporte público."
        area = "Secretaría de Obras Viales y Pavimentación"
        cuadrilla = "Cuadrilla de Asfalto y Bacheo Rápido"
        recursos = ["Camión volcador", "Asfalto en caliente", "Rodillo compactador", "Señalización reflectiva"]
        sla = 24 if es_urgente else 48
        acciones = [
            "Inspección técnica preliminar del bache",
            "Señalización preventiva con balizas",
            "Fresado, relleno asfáltico y compactación"
        ]
    elif any(k in t for k in ["semaforo", "semáforo", "señal", "estaciona", "choque", "rampa", "cartel"]):
        categoria = "Tránsito y Señalización"
        subcategoria = "Falla semafórica en intersección" if "semaforo" in t or "semáforo" in t else "Señalética vial dañada"
        prioridad = "Alta" if "semaforo" in t or "semáforo" in t else "Media"
        justificacion = "Alteración en el ordenamiento y seguridad de las intersecciones viales."
        area = "Dirección de Ingeniería de Tránsito y Transporte"
        cuadrilla = "Equipo Técnico de Señalización y Semáforos"
        recursos = ["Móvil técnico", "Controladores electrónicos de repuesto", "Instrumental de medición"]
        sla = 12 if "semaforo" in t or "semáforo" in t else 48
        acciones = [
            "Envío de inspector de tránsito para ordenamiento manual",
            "Revisión y reprogramación de la placa controladora",
            "Verificación de sincronismo de onda verde"
        ]
    elif any(k in t for k in ["luz", "luminaria", "foco", "oscura", "farola", "poste"]):
        categoria = "Alumbrado Público"
        subcategoria = "Recambio y mantenimiento de luminarias LED"
        prioridad = "Media" if "oscura" in t or "insegur" in t else "Baja"
        justificacion = "Disminución de visibilidad nocturna y afectación de la seguridad barrial."
        area = "Dirección de Alumbrado y Electromecánica"
        cuadrilla = "Cuadrilla de Alumbrado con Hidroelevador"
        recursos = ["Camión hidroelevador", "Artefactos LED 150W", "Fotocélulas y fusibles"]
        sla = 48
        acciones = [
            "Comprobación de suministro en la caja seccionadora",
            "Reemplazo de lámpara por artefacto LED",
            "Prueba de encendido y fotocontrol"
        ]
    elif any(k in t for k in ["basura", "mugre", "olor", "contenedor", "escombros", "microbasural", "bolsas"]):
        categoria = "Higiene Urbana"
        subcategoria = "Limpieza de microbasural y residuos especiales"
        prioridad = "Media"
        justificacion = "Foco de insalubridad, malos olores y proliferación de vectores."
        area = "Secretaría de Servicios Públicos e Higiene"
        cuadrilla = "Cuadrilla de Limpieza y Recolección Pesada"
        recursos = ["Camión compactador", "Pala cargadora frontal", "Líquido desinfectante"]
        sla = 48
        acciones = [
            "Retiro de residuos acumulados con pala mecánica",
            "Barrido y despeje total de la calzada",
            "Fumigación y colocación de cartel disuasorio"
        ]
    elif any(k in t for k in ["arbol", "árbol", "rama", "pasto", "plaza", "parque", "poda", "maleza"]):
        peligro = any(x in t for x in ["caer", "peligro", "cable", "sobre auto", "quebrad"])
        categoria = "Espacios Verdes"
        subcategoria = "Poda de emergencia por riesgo de caída" if peligro else "Poda y mantenimiento de espacios verdes"
        prioridad = "Alta" if peligro else "Baja"
        justificacion = "Riesgo de desprendimiento sobre bienes o personas." if peligro else "Mantenimiento estético programable."
        area = "Dirección de Espacios Verdes y Arbolado"
        cuadrilla = "Cuadrilla de Poda en Altura y Desmalezado"
        recursos = ["Motosierras telescópicas", "Grúa con cesta", "Camión chipeador de ramas"]
        sla = 24 if peligro else 96
        acciones = [
            "Evaluación fitosanitaria del ejemplar arbóreo",
            "Corte controlado de ramas con riesgo de caída",
            "Chipeado de ramas y limpieza de vereda"
        ]
    else:
        categoria = "Atención Ciudadana General"
        subcategoria = "Solicitud vecinal multipropósito"
        prioridad = "Media"
        justificacion = "Reclamo general recibido para derivación operativa."
        area = "Centro de Gestión y Participación Ciudadana"
        cuadrilla = "Equipo de Inspectores de Atención Vecinal"
        recursos = ["Móvil de inspección", "Formulario digital de inspección"]
        sla = 72
        acciones = [
            "Contacto telefónico o mensaje de validación con el vecino",
            "Inspección de campo por operador municipal",
            "Asignación a la secretaría correspondiente"
        ]

    match = re.search(r'(?:en|calle|av\.|avenida|esquina|frente a)\s+([A-Za-z0-9\s]+?)(?:\.|,|$)', texto, re.IGNORECASE)
    ubicacion = match.group(1).strip() if match else "Ubicación a determinar"

    return {
        "categoria": categoria,
        "subcategoria": subcategoria,
        "prioridad": prioridad,
        "justificacion_prioridad": justificacion,
        "area_responsable": area,
        "cuadrilla_sugerida": cuadrilla,
        "recursos_necesarios": recursos,
        "sla_horas": sla,
        "resumen_ejecutivo": f"Reclamo de {subcategoria.lower()} registrado en {ubicacion}.",
        "acciones_recomendadas": acciones,
        "ubicacion_detectada": ubicacion,
        "mensaje_ciudadano": f"Estimado/a vecino/a: Hemos registrado su solicitud sobre {categoria.lower()} ({subcategoria}). El trámite fue derivado a {area} con una respuesta estimada de {sla} hs. ¡Gracias por colaborar con el cuidado de nuestra ciudad!"
    }


# ==============================================================================
# HELPERS DE PRIORIDAD
# ==============================================================================
PRIO_CONFIG = {
    "Crítica": {"css": "chip-critica", "card": "result-card-critica", "icon": "🔴", "color": "#ef4444"},
    "Alta":    {"css": "chip-alta",    "card": "result-card-alta",    "icon": "🟠", "color": "#f97316"},
    "Media":   {"css": "chip-media",   "card": "result-card-media",   "icon": "🟡", "color": "#eab308"},
    "Baja":    {"css": "chip-baja",    "card": "result-card-baja",    "icon": "🟢", "color": "#22c55e"},
}

# ==============================================================================
# BARRA LATERAL — CONFIGURACIÓN Y ESTADO
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Configuración del Sistema")

    st.markdown("#### 🤖 Motor de Inteligencia")
    modo_ia = st.radio(
        "Modo de análisis:",
        ["Simulación Inteligente (Offline/Demo)", "Google Gemini API (Online)"],
        index=0,
        label_visibility="collapsed"
    )

    gemini_key = ""
    modelo_elegido = "gemini-1.5-flash"

    if modo_ia == "Google Gemini API (Online)":
        gemini_key = st.text_input(
            "Gemini API Key:",
            value=os.environ.get("GEMINI_API_KEY", ""),
            type="password",
            help="Obtené tu key gratuita en aistudio.google.com"
        )
        modelo_elegido = st.selectbox(
            "Modelo:",
            ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        )
        if not gemini_key:
            st.info("ℹ️ Sin API Key activa. Modo simulación.")

    st.divider()

    total_rec = len(st.session_state.reclamos)
    criticos_rec = sum(1 for r in st.session_state.reclamos if r["prioridad"] == "Crítica")
    resueltos_rec = sum(1 for r in st.session_state.reclamos if r["estado"] == "Resuelto")
    tasa_res = round((resueltos_rec / total_rec * 100)) if total_rec else 0

    st.markdown("#### 📊 Estado de Operaciones")
    st.markdown(f"""
    <div class="sidebar-stat-card">
        <span class="sidebar-stat-label">Total Tickets</span>
        <span class="sidebar-stat-value">{total_rec}</span>
    </div>
    <div class="sidebar-stat-card" style="border-color:rgba(239,68,68,0.2);">
        <span class="sidebar-stat-label">🔴 Críticos Activos</span>
        <span class="sidebar-stat-value" style="color:#f87171;">{criticos_rec}</span>
    </div>
    <div class="sidebar-stat-card" style="border-color:rgba(34,197,94,0.2);">
        <span class="sidebar-stat-label">✅ Resueltos</span>
        <span class="sidebar-stat-value" style="color:#4ade80;">{resueltos_rec}/{total_rec}</span>
    </div>
    <div style="margin-top:0.3rem;">
        <div style="font-size:0.72rem; color:rgba(255,255,255,0.4); margin-bottom:0.3rem;">Tasa de resolución: {tasa_res}%</div>
        <div class="progress-bar-wrap">
            <div class="progress-bar-fill" style="width:{tasa_res}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🗑️ Reiniciar Dataset de Prueba", use_container_width=True):
        st.session_state.reclamos = []
        inicializar_dataset()
        st.rerun()


# ==============================================================================
# HERO HEADER
# ==============================================================================
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🏙️ Gestor Urbano IA</div>
        <div class="hero-subtitle">Centro de Operaciones Inteligente — Clasificación, Priorización y Ruteo de Reclamos Municipales con IA</div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div style="height:100%; display:flex; align-items:center; justify-content:flex-end; padding-top:0.5rem;">
        <span class="hero-badge">Sistema Operativo</span>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PESTAÑAS PRINCIPALES
# ==============================================================================
tab_ingreso, tab_dashboard, tab_bandeja, tab_docs = st.tabs([
    "📝 Mesa de Entradas",
    "📊 Dashboard & KPIs",
    "🗂️ Bandeja de Tickets",
    "ℹ️ Metodología & Prompt"
])


# ==============================================================================
# PESTAÑA 1: MESA DE ENTRADAS / NUEVO RECLAMO
# ==============================================================================
with tab_ingreso:
    col_form, col_res = st.columns([1.1, 0.9], gap="large")

    with col_form:
        with st.container(border=True):
            st.subheader("📋 Ingreso de Reporte Ciudadano")

            st.caption("⚡ **Casos de prueba rápidos — clic para cargar:**")
            e1, e2, e3 = st.columns(3)
            if e1.button("💥 Cables con chispas", use_container_width=True):
                st.session_state["in_reclamo"] = "Urgente: Hay cables de luz cortados sobre la vereda echando chispas tras la tormenta en Av. Colón 450. Pasan chicos caminando, es un peligro de muerte."
                st.session_state["in_canal"] = "Línea 147 (Telefónico)"
                st.session_state["in_vecino"] = "Carlos Gómez (11-4567-8901)"
            if e2.button("🕳️ Pozo frente a escuela", use_container_width=True):
                st.session_state["in_reclamo"] = "Hay un bache muy profundo en calle San Martín 1200 justo en la puerta del colegio. Los autos y colectivos tienen que frenar de golpe para no romper el tren delantero."
                st.session_state["in_canal"] = "App Móvil Ciudadana"
                st.session_state["in_vecino"] = "María Rodríguez (11-9876-5432)"
            if e3.button("🗑️ Basura acumulada", use_container_width=True):
                st.session_state["in_reclamo"] = "Hace 5 días que no pasa el camión recolector en la esquina de Belgrano y Jujuy. Hay un microbasural enorme, olor insoportable y perros rompiendo bolsas."
                st.session_state["in_canal"] = "WhatsApp Municipal"
                st.session_state["in_vecino"] = "Vecinos de Belgrano y Jujuy"

            c_can, c_vec = st.columns([1, 1])
            with c_can:
                canal_sel = st.selectbox(
                    "Canal de Recepción:",
                    ["Portal Web", "Línea 147 (Telefónico)", "WhatsApp Municipal", "App Móvil Ciudadana", "Mesa de Entradas"],
                    index=["Portal Web", "Línea 147 (Telefónico)", "WhatsApp Municipal", "App Móvil Ciudadana", "Mesa de Entradas"].index(
                        st.session_state.get("in_canal", "Portal Web"))
                )
            with c_vec:
                nombre_vecino = st.text_input(
                    "Datos del Vecino (Opcional):",
                    value=st.session_state.get("in_vecino", ""),
                    placeholder="Ej: Juan Pérez / 11-4567-8900"
                )

            texto_in = st.text_area(
                "Descripción del problema en lenguaje natural:",
                value=st.session_state.get("in_reclamo", ""),
                placeholder="Ej: Hay un pozo muy grande en la calle San Martín frente a la escuela...",
                height=130
            )

            btn_analizar = st.button("🚀 Analizar, Priorizar y Derivar con IA", type="primary", use_container_width=True)

    with col_res:
        with st.container(border=True):
            st.subheader("⚡ Diagnóstico en Tiempo Real")

            if btn_analizar:
                if not texto_in.strip():
                    st.warning("⚠️ Ingresá la descripción del problema antes de procesar.")
                else:
                    with st.spinner("🤖 Analizando con IA..."):
                        res = None
                        motor = ""

                        if modo_ia == "Google Gemini API (Online)" and gemini_key:
                            try:
                                res = clasificar_con_gemini(texto_in, gemini_key, modelo_elegido)
                                motor = f"Google Gemini · {modelo_elegido}"
                                motor_icon = "✨"
                            except Exception as e:
                                st.error(f"Error Gemini API ({e}). Usando motor de respaldo.")
                                res = clasificar_heuristico(texto_in)
                                motor = "Motor Heurístico · Respaldo"
                                motor_icon = "⚙️"
                        else:
                            res = clasificar_heuristico(texto_in)
                            motor = "Motor Heurístico · Offline"
                            motor_icon = "⚙️"

                        nuevo_id = f"TKT-{1042 + len(st.session_state.reclamos)}"
                        ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M")

                        registro = {
                            "id": nuevo_id,
                            "fecha": ahora_str,
                            "descripcion": texto_in,
                            "categoria": res.get("categoria", "General"),
                            "subcategoria": res.get("subcategoria", "General"),
                            "prioridad": res.get("prioridad", "Media"),
                            "justificacion": res.get("justificacion_prioridad", "-"),
                            "area": res.get("area_responsable", "Servicios Generales"),
                            "cuadrilla": res.get("cuadrilla_sugerida", "Cuadrilla Municipal"),
                            "recursos": res.get("recursos_necesarios", []),
                            "sla_horas": res.get("sla_horas", 48),
                            "resumen": res.get("resumen_ejecutivo", texto_in),
                            "acciones": res.get("acciones_recomendadas", []),
                            "ubicacion": res.get("ubicacion_detectada", "A coordinar"),
                            "estado": "Pendiente",
                            "canal": canal_sel,
                            "mensaje_vecino": res.get("mensaje_ciudadano", "")
                        }
                        st.session_state.reclamos.insert(0, registro)

                        prio = res.get("prioridad", "Media")
                        cfg = PRIO_CONFIG.get(prio, PRIO_CONFIG["Media"])

                        st.success(f"✅ Ticket **{nuevo_id}** generado y derivado exitosamente.")

                        # ── Tarjeta de resultado ──
                        acciones = res.get("acciones_recomendadas", [])
                        steps_html = ""
                        for i, acc in enumerate(acciones, 1):
                            connector = '<div class="step-connector"></div>' if i < len(acciones) else ""
                            steps_html += f"""
                            <div class="step-item">
                                <div class="step-number">{i}</div>
                                <div class="step-text">{acc}</div>
                            </div>
                            {connector}
                            """

                        st.markdown(f"""
                        <div class="result-card {cfg['card']}">
                            <div class="result-header">
                                <div>
                                    <div class="result-ticket-id">#{nuevo_id}</div>
                                    <div style="font-size:0.8rem; color:rgba(255,255,255,0.4); margin-top:2px;">{ahora_str} · {canal_sel}</div>
                                </div>
                                <span class="chip {cfg['css']}">{cfg['icon']} {prio}</span>
                            </div>
                            <div class="result-meta">
                                <div class="result-meta-item">
                                    <div class="result-meta-label">📂 Categoría</div>
                                    <div class="result-meta-value">{res.get('categoria')}</div>
                                </div>
                                <div class="result-meta-item">
                                    <div class="result-meta-label">🏢 Área Responsable</div>
                                    <div class="result-meta-value">{res.get('area_responsable')}</div>
                                </div>
                                <div class="result-meta-item">
                                    <div class="result-meta-label">⏱️ SLA</div>
                                    <div class="result-meta-value">{res.get('sla_horas')} horas</div>
                                </div>
                                <div class="result-meta-item">
                                    <div class="result-meta-label">📍 Ubicación</div>
                                    <div class="result-meta-value">{res.get('ubicacion_detectada')}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── Resumen ejecutivo ──
                        st.markdown(f"""
                        <div class="section-label" style="margin-top:1rem;">📌 Resumen para Cuadrilla</div>
                        <div class="exec-box">{res.get('resumen_ejecutivo')}</div>
                        """, unsafe_allow_html=True)

                        # ── Cuadrilla + Stepper ──
                        st.markdown(f"""
                        <div class="section-label" style="margin-top:1rem;">👷 Cuadrilla: <span style="color:#e2e8f0; font-weight:600; text-transform:none; letter-spacing:0;">{res.get('cuadrilla_sugerida')}</span></div>
                        <div class="section-label">🛠️ Plan de Acción Operativo</div>
                        <div class="stepper">{steps_html}</div>
                        """, unsafe_allow_html=True)

                        # ── Burbuja WhatsApp ──
                        st.markdown(f"""
                        <div class="section-label" style="margin-top:1rem;">💬 Notificación Automática al Vecino</div>
                        <div class="whatsapp-bubble">
                            <div class="whatsapp-header">📱 GESTOR URBANO IA · Municipio</div>
                            {res.get('mensaje_ciudadano')}
                            <div class="whatsapp-tick">✓✓ Entregado</div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── Motor badge ──
                        st.markdown(f"""
                        <div style="margin-top:0.8rem;">
                            <span class="motor-badge">{motor_icon} {motor}</span>
                        </div>
                        """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <div style="text-align:center; padding: 3rem 1rem; color:rgba(255,255,255,0.3);">
                    <div style="font-size:3rem; margin-bottom:1rem;">🏙️</div>
                    <div style="font-size:0.9rem;">Completá el reclamo o hacé clic en un ejemplo rápido para ver el análisis en tiempo real</div>
                </div>
                """, unsafe_allow_html=True)


# ==============================================================================
# PESTAÑA 2: DASHBOARD & KPIS MUNICIPALES
# ==============================================================================
with tab_dashboard:
    st.subheader("📊 Métricas de Operaciones Urbanas en Tiempo Real")

    if st.session_state.reclamos:
        df = pd.DataFrame(st.session_state.reclamos)

        total = len(df)
        criticos = len(df[df["prioridad"].isin(["Crítica", "Alta"])])
        sla_prom = round(df["sla_horas"].mean(), 1)
        resueltos = len(df[df["estado"] == "Resuelto"])
        tasa = round((resueltos / total) * 100, 1) if total else 0

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total de Reclamos</div>
                <div class="kpi-value">{total}</div>
                <div class="kpi-unit">tickets registrados</div>
            </div>""", unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title" style="color:#f87171;">Urgentes / Críticos</div>
                <div class="kpi-value kpi-value-red">{criticos}</div>
                <div class="kpi-unit">requieren atención inmediata</div>
            </div>""", unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">SLA Promedio</div>
                <div class="kpi-value kpi-value-blue">{sla_prom}</div>
                <div class="kpi-unit">horas de respuesta</div>
            </div>""", unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title" style="color:#4ade80;">Tasa de Resolución</div>
                <div class="kpi-value kpi-value-green">{tasa}%</div>
                <div class="kpi-unit">{resueltos} de {total} resueltos</div>
            </div>""", unsafe_allow_html=True)

        st.write("")

        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True):
                st.markdown("##### 📌 Reclamos por Categoría")
                cat_counts = df["categoria"].value_counts().reset_index()
                cat_counts.columns = ["Categoría", "Cantidad"]
                st.bar_chart(cat_counts.set_index("Categoría"), color="#3b82f6")
        with g2:
            with st.container(border=True):
                st.markdown("##### ⚡ Reclamos por Nivel de Prioridad")
                prio_order = ["Crítica", "Alta", "Media", "Baja"]
                prio_counts = df["prioridad"].value_counts().reindex(prio_order, fill_value=0).reset_index()
                prio_counts.columns = ["Prioridad", "Cantidad"]
                st.bar_chart(prio_counts.set_index("Prioridad"), color="#f97316")

        g3, g4 = st.columns(2)
        with g3:
            with st.container(border=True):
                st.markdown("##### 📱 Distribución por Canal de Ingreso")
                canal_counts = df["canal"].value_counts().reset_index()
                canal_counts.columns = ["Canal", "Cantidad"]
                st.bar_chart(canal_counts.set_index("Canal"), color="#10b981")
        with g4:
            with st.container(border=True):
                st.markdown("##### 🏢 Carga de Trabajo por Área Municipal")
                area_counts = df["area"].value_counts().reset_index()
                area_counts.columns = ["Área", "Cantidad"]
                st.bar_chart(area_counts.set_index("Área"), color="#8b5cf6")
    else:
        st.info("No hay reclamos cargados.")


# ==============================================================================
# PESTAÑA 3: BANDEJA DE CUADRILLAS & TICKETS
# ==============================================================================
with tab_bandeja:
    st.subheader("🗂️ Bandeja de Gestión de Reclamos y Cuadrillas")

    if st.session_state.reclamos:
        df_tkt = pd.DataFrame(st.session_state.reclamos)

        f1, f2, f3 = st.columns(3)
        with f1:
            filtro_prio = st.multiselect("Filtrar Prioridad:", options=df_tkt["prioridad"].unique(), default=df_tkt["prioridad"].unique())
        with f2:
            filtro_area = st.multiselect("Filtrar Área:", options=df_tkt["area"].unique(), default=df_tkt["area"].unique())
        with f3:
            filtro_est = st.multiselect("Filtrar Estado:", options=df_tkt["estado"].unique(), default=df_tkt["estado"].unique())

        df_filtrado = df_tkt[
            (df_tkt["prioridad"].isin(filtro_prio)) &
            (df_tkt["area"].isin(filtro_area)) &
            (df_tkt["estado"].isin(filtro_est))
        ]

        st.dataframe(
            df_filtrado[["id", "fecha", "categoria", "prioridad", "area", "cuadrilla", "ubicacion", "sla_horas", "estado", "canal"]],
            column_config={
                "id": "ID Ticket",
                "fecha": "Fecha",
                "categoria": "Categoría",
                "prioridad": "Prioridad",
                "area": "Área Responsable",
                "cuadrilla": "Cuadrilla Asignada",
                "ubicacion": "Ubicación",
                "sla_horas": st.column_config.NumberColumn("SLA (hs)", format="%d hs"),
                "estado": "Estado",
                "canal": "Canal"
            },
            hide_index=True,
            use_container_width=True
        )

        c_d1, c_d2 = st.columns([1, 3])
        with c_d1:
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Exportar Tickets (CSV)",
                data=csv,
                file_name=f"tickets_municipales_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.divider()
        st.markdown("#### 🔍 Ficha Técnica Completa de un Ticket")
        ticket_elegido = st.selectbox("Seleccionar Ticket:", options=df_tkt["id"].tolist())

        if ticket_elegido:
            item = next((r for r in st.session_state.reclamos if r["id"] == ticket_elegido), None)
            if item:
                prio_item = item.get("prioridad", "Media")
                cfg_item = PRIO_CONFIG.get(prio_item, PRIO_CONFIG["Media"])
                with st.container(border=True):
                    c_det1, c_det2 = st.columns([1.5, 1])
                    with c_det1:
                        st.markdown(f"### {item['id']} — {item['categoria']}")
                        st.markdown(f"**Descripción:** *\"{item['descripcion']}\"*")
                        st.markdown(f"""<div class="exec-box">{item['resumen']}</div>""", unsafe_allow_html=True)
                        st.markdown("**🛠️ Plan de Acción:**")
                        steps_ficha = "".join(
                            f'<div class="step-item"><div class="step-number">{i}</div><div class="step-text">{a}</div></div>'
                            for i, a in enumerate(item["acciones"], 1)
                        )
                        st.markdown(f'<div class="stepper">{steps_ficha}</div>', unsafe_allow_html=True)
                    with c_det2:
                        st.markdown(f"""
                        <div style="display:flex; flex-direction:column; gap:0.5rem; padding-top:0.5rem;">
                            <div class="result-meta-item">
                                <div class="result-meta-label">Prioridad · SLA</div>
                                <div class="result-meta-value"><span class="chip {cfg_item['css']}">{cfg_item['icon']} {prio_item}</span> &nbsp; {item['sla_horas']} hs</div>
                            </div>
                            <div class="result-meta-item">
                                <div class="result-meta-label">Área Responsable</div>
                                <div class="result-meta-value">{item['area']}</div>
                            </div>
                            <div class="result-meta-item">
                                <div class="result-meta-label">Cuadrilla</div>
                                <div class="result-meta-value">{item['cuadrilla']}</div>
                            </div>
                            <div class="result-meta-item">
                                <div class="result-meta-label">Ubicación · Canal</div>
                                <div class="result-meta-value">{item['ubicacion']} · {item['canal']}</div>
                            </div>
                            <div class="result-meta-item">
                                <div class="result-meta-label">Estado · Fecha</div>
                                <div class="result-meta-value">{item['estado']} · {item['fecha']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("No hay tickets disponibles.")


# ==============================================================================
# PESTAÑA 4: METODOLOGÍA, PROMPT & FACTIBILIDAD
# ==============================================================================
with tab_docs:
    st.subheader("ℹ️ Arquitectura del Sistema, Prompt Engineering y Viabilidad Económica")

    st.markdown("""
    ### 🏛️ Propósito y Problemática Resuelta
    En la gestión pública tradicional, la recepción y clasificación de reclamos es un cuello de botella manual, lento y sujeto a criterios dispares:
    - **Demoras operativas:** Un operador humano puede tardar entre 3 y 8 minutos en leer, categorizar y derivar un reclamo.
    - **Errores de ruteo:** Hasta un 25% de los tickets son derivados al área equivocada.
    - **Falta de prioridad estandarizada:** No se discrimina adecuadamente una emergencia crítica (ej. cables con chispas) de una tarea ordinaria.

    **Gestor Urbano IA** resuelve esta problemática aplicando un **Modelo de Lenguaje (LLM)** con un **Prompt de Sistema Estructurado con Salida JSON**.
    """)

    with st.container(border=True):
        st.markdown("#### 🧠 Prompt Estructurado del Sistema (System Instruction)")
        st.code(PROMPT_SISTEMA, language="text")

    st.markdown("""
    ---
    ### 💰 Factibilidad Económica y ROI (Return on Investment)

    | Métrica | Proceso Manual Tradicional | Gestor Urbano IA (Gemini 1.5 Flash) |
    |---|---|---|
    | **Tiempo por reclamo** | 3 a 8 minutos | **< 2 segundos** |
    | **Disponibilidad** | Lunes a Viernes (8 a 18 hs) | **24/7/365 en tiempo real** |
    | **Costo por reclamo** | ~$0.50 - $1.20 USD (costo hora operador) | **$0.000015 USD (~$0.015 por 1.000 reclamos)** |
    | **Consumo de tokens** | N/A | ~200 tokens input / ~150 tokens output |
    | **Costo mensual (10.000 reclamos)** | ~$8.000 USD | **~$0.15 USD / mes** |

    > **Conclusión:** La solución es **100% viable económica y técnicamente**, escalable a cualquier municipio del país con un costo computacional prácticamente nulo.
    """)