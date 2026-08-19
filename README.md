# 🏙️ Gestor Urbano IA — Centro de Operaciones Municipal Inteligente

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gestor-urbano-ia-jgntgbseevvvp8vpstt6bw.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/maurorgarcia/gestor-urbano-ia)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Model](https://img.shields.io/badge/IA%20Model-Google%20Gemini%201.5%20Flash-orange?logo=google)](https://aistudio.google.com/)

> **Proyecto Final — Curso de Prompt Engineering para Programadores | Coderhouse**  
> **Estudiante:** Mauro García  
> **Año:** 2025  

---

## 📌 Enlaces del Proyecto

* 🌐 **Aplicación Web Desplegada (Streamlit Cloud):**  
  👉 **[https://gestor-urbano-ia-jgntgbseevvvp8vpstt6bw.streamlit.app/](https://gestor-urbano-ia-jgntgbseevvvp8vpstt6bw.streamlit.app/)**
* 🐙 **Repositorio en GitHub:**  
  👉 **[https://github.com/maurorgarcia/gestor-urbano-ia](https://github.com/maurorgarcia/gestor-urbano-ia)**

---

## 📖 Descripción del Proyecto

**Gestor Urbano IA** es una solución de gobierno digital (*GovTech*) diseñada para automatizar la recepción, clasificación, priorización y derivación de reclamos ciudadanos en municipios y gobiernos locales mediante Inteligencia Artificial Generativa.

### 🛑 La Problemática
En la gestión municipal tradicional:
1. **Entrada caótica:** Los vecinos reportan incidencias en lenguaje coloquial a través de múltiples canales (Línea 147, WhatsApp, formularios web) sin conocer qué secretaría es la competente.
2. **Triaje manual y lento:** Operadores humanos tardan de 3 a 8 minutos por ticket en leer, categorizar y derivar manualmente los reclamos, causando cuellos de botella y hasta un 25% de asignaciones erróneas.
3. **Falta de priorización objetiva:** Casos críticos con riesgo de vida (ej. cables de alta tensión caídos, escapes de gas, pozos frente a escuelas) quedan en la misma cola de espera que tareas de mantenimiento estético (ej. pintura de cordones).

### 💡 La Solución
**Gestor Urbano IA** procesa el texto en lenguaje natural en **menos de 2 segundos**, asignando de forma instantánea:
* 📂 **Categoría y Subcategoría técnica.**
* ⚡ **Nivel de Prioridad estandarizado** (🔴 Crítica, 🟠 Alta, 🟡 Media, 🟢 Baja) con justificación técnica.
* 🏢 **Área y Subsecretaría Municipal Responsable.**
* ⏱️ **Tiempo Máximo de Respuesta (SLA en horas)**.
* 👷 **Cuadrilla Operativa y Recursos Específicos** (ej. *Camión hidroelevador*, *Herramientas dieléctricas*, *Asfalto en caliente*).
* 🛠️ **Plan de Acción Operativo paso a paso** para la orden de trabajo.
* 💬 **Notificación Automática y Empática al Vecino** lista para WhatsApp/SMS con número de seguimiento.

---

## ✨ Funcionalidades Principales

1. **📝 Mesa de Entradas Multicanal:**
   - Admite reportes desde Portal Web, Línea 147, WhatsApp Municipal, App Móvil y Mesa de Entradas.
   - Botones de **prueba rápida con 1 clic** (*Cables con chispas*, *Pozo frente a escuela*, *Basura acumulada*).
2. **📊 Dashboard & KPIs Municipales en Tiempo Real:**
   - Métricas de tickets totales, urgentes, SLA promedio y tasa de resolución.
   - Gráficos estadísticos interactivos de reclamos por categoría, prioridad, canal y área de gobierno.
3. **🗂️ Bandeja de Cuadrillas & CRM de Tickets:**
   - Tabla interactiva con filtros combinados (Prioridad, Área y Estado).
   - Visor de ficha técnica completa de cada ticket.
   - **Exportación de reportes a formato CSV**.
4. **🧠 Doble Motor de Inteligencia Artificial:**
   - **Online:** Conexión directa con la API oficial de **Google Gemini** (`gemini-1.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`).
   - **Offline/Demo:** Motor heurístico inteligente con procesamiento de lenguaje natural para pruebas sin API Key.

---

## 🧠 Arquitectura de Prompt Engineering

El sistema utiliza un **Prompt de Sistema Estructurado con Salida JSON Estricta** para garantizar que los modelos de lenguaje devuelvan datos predecibles, tipados y listos para ser consumidos por sistemas de bases de datos:

```json
{
  "categoria": "Infraestructura Vial | Alumbrado Público | Higiene Urbana | Espacios Verdes | Riesgo Eléctrico / Emergencia | Tránsito y Señalización | Red Pluvial y Cloacas | Zoonosis",
  "subcategoria": "Nombre técnico del problema",
  "prioridad": "Crítica | Alta | Media | Baja",
  "justificacion_prioridad": "Explicación técnica de la urgencia asignada",
  "area_responsable": "Nombre de la secretaría municipal competente",
  "cuadrilla_sugerida": "Equipo operativo necesario",
  "recursos_necesarios": ["Recurso 1", "Recurso 2"],
  "sla_horas": 24,
  "resumen_ejecutivo": "Resumen técnico para la orden de trabajo",
  "acciones_recomendadas": ["Paso 1", "Paso 2", "Paso 3"],
  "ubicacion_detectada": "Dirección o punto de referencia extraído",
  "mensaje_ciudadano": "Respuesta cordial y empática para el vecino"
}
```

---

## 💰 Factibilidad Económica y ROI

| Indicador | Proceso Manual Tradicional | Gestor Urbano IA (Gemini 1.5 Flash) |
|---|---|---|
| **Tiempo de respuesta** | 3 a 8 minutos | **< 2 segundos** |
| **Disponibilidad** | Lun a Vie (8 a 18 hs) | **24/7/365 en tiempo real** |
| **Costo por reclamo** | ~$0.50 - $1.20 USD (hora operador) | **~$0.000015 USD** (~200 tokens) |
| **Costo mensual (10.000 reclamos)** | ~$8.000 USD | **~$0.15 USD / mes** |

> **Conclusión de Viabilidad:** La solución tiene un costo tecnológico prácticamente despreciable frente a los miles de dólares mensuales en horas-hombre de triaje manual, demostrando una **altísima viabilidad económica y retorno de inversión (ROI)** para cualquier municipio.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+ / 3.14
* **Framework Web:** [Streamlit](https://streamlit.io/)
* **Procesamiento de Datos:** [Pandas](https://pandas.pydata.org/)
* **Motor de IA Generativa:** [Google Generative AI SDK](https://ai.google.dev/) (`google-generativeai`)
* **Gestión de Entorno:** `python-dotenv`
* **Despliegue:** [Streamlit Community Cloud](https://streamlit.io/cloud)

---

## 🚀 Instalación y Ejecución Local

Si deseas clonar y ejecutar este proyecto en tu computadora:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/maurorgarcia/gestor-urbano-ia.git
   cd gestor-urbano-ia
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Configurar API Key de Gemini:**
   Crea un archivo `.env` en la raíz del proyecto:
   ```env
   GEMINI_API_KEY=tu_api_key_aqui
   ```
   *(Si no configuras una API Key, la app funcionará automáticamente con el motor simulado inteligente).*

5. **Iniciar la aplicación:**
   ```bash
   streamlit run app.py
   ```

6. Abrir en el navegador: **`http://localhost:8501`** (o `http://127.0.0.1:8501`).

---

## 👤 Autor

* **Estudiante:** Mauro García
* **Proyecto Final:** Curso de *Prompt Engineering para Programadores*
* **Institución:** CoderHouse
