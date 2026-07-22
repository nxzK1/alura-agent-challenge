import os
 
import requests
import streamlit as st
from dotenv import load_dotenv
 
load_dotenv()
 
API_URL = os.environ.get("API_URL", "http://localhost:8000")
 
# Si más adelante se quiere mostrar la fuente (ej. en una vista interna/
# administrativa), basta con cambiar esto a True — el resto del código ya
# está preparado para eso.
MOSTRAR_FUENTES = False
 
NOMBRE_ASISTENTE = "Asistente virtual MIA - Clinicas FICIntegra"
 
DESCRIPCION_PUEDE = [
    "Turnos y cómo agendarlos",
    "Coberturas médicas y convenios con aseguradoras",
    "Políticas de cancelación y reagendamiento",
    "Instrucciones antes y después de tu consulta",
    "Privacidad y acceso a tu historial clínico",
]
 
DESCRIPCION_NO_PUEDE = [
    "Dar diagnósticos médicos ni interpretar síntomas",
    "Recetar o recomendar medicamentos",
    "Reemplazar una consulta con un profesional de salud",
    "Responder temas fuera de la información de la clínica",
]
 
PREGUNTAS_SUGERIDAS = [
    "¿Qué debo llevar a mi primera consulta?",
    "¿Cuántas horas de ayuno necesito antes de un análisis de sangre?",
    "¿Qué pasa si falto a mi cita sin avisar?",
    "¿Cómo solicito mi historial clínico?",
]
 
# --- Paletas: verdes con tonos azulados, calma y armonía entre sí ----------
LIGHT = {
    "bg": "#EAF2EF",
    "surface": "#FFFFFF",
    "ink": "#122320",
    "ink_soft": "#4B615B",
    "primary": "#1F7A66",
    "primary_dark": "#14503F",
    "accent_blue": "#2F7FA0",
    "border": "#CFE3DD",
    "user_bubble": "linear-gradient(135deg, #1F7A66 0%, #2F7FA0 100%)",
    "user_text": "#FFFFFF",
    "agent_bubble": "linear-gradient(135deg, #FFFFFF 0%, #E3F1EE 100%)",
    "agent_border": "#B9DED3",
    "header_bg": "#FFFFFF",
}
 
DARK = {
    "bg": "#0D1A18",
    "surface": "#152724",
    "ink": "#E6F2EE",
    "ink_soft": "#9FC1B7",
    "primary": "#3FB39A",
    "primary_dark": "#1F7A66",
    "accent_blue": "#5AA9C9",
    "border": "#25423C",
    "user_bubble": "linear-gradient(135deg, #1F7A66 0%, #2A6E8C 100%)",
    "user_text": "#F3FBF9",
    "agent_bubble": "linear-gradient(135deg, #152724 0%, #16302B 100%)",
    "agent_border": "#2B4A43",
    "header_bg": "#152724",
}
 
st.set_page_config(
    page_title=f"{NOMBRE_ASISTENTE} · Asistente Virtual FIC-Integra",
    page_icon="🩺",
    layout="centered",
)
 
if "modo_oscuro" not in st.session_state:
    st.session_state.modo_oscuro = False
 
_, col_toggle = st.columns([4, 1])
with col_toggle:
    st.session_state.modo_oscuro = st.toggle("🌙", value=st.session_state.modo_oscuro)
 
C = DARK if st.session_state.modo_oscuro else LIGHT
 
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');
 
    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans', sans-serif;
        color: {C["ink"]};
    }}
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stDecoration"],
    footer {{
        background-color: {C["bg"]} !important;
    }}
    [data-testid="stBottom"] {{
        background-color: {C["bg"]} !important;
    }}
    [data-testid="stBottom"] * {{
        background-color: transparent !important;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}
 
    /* Encabezado estilo "pestaña de carpeta de paciente" */
    .clinic-header {{
        background: {C["header_bg"]};
        border: 1px solid {C["border"]};
        border-radius: 14px 14px 4px 4px;
        border-top: 5px solid {C["primary"]};
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.8rem;
    }}
    .clinic-header h1 {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 1.6rem;
        color: {C["ink"]};
        margin: 0 0 0.15rem 0;
    }}
    .clinic-header p {{
        color: {C["ink_soft"]};
        margin: 0;
        font-size: 0.92rem;
    }}
 
    /* Burbujas de chat con color propio (verde-azulado), en vez del
       contenedor gris por defecto de Streamlit */
    .msg-user {{
        background: {C["user_bubble"]};
        color: {C["user_text"]};
        padding: 0.7rem 1rem;
        border-radius: 14px 14px 4px 14px;
        line-height: 1.45;
    }}
    .msg-agent {{
        background: {C["agent_bubble"]};
        color: {C["ink"]};
        border: 1px solid {C["agent_border"]};
        padding: 0.7rem 1rem;
        border-radius: 14px 14px 14px 4px;
        line-height: 1.45;
    }}
 
    /* Etiquetas de fuente, estilo "ticket" (solo si MOSTRAR_FUENTES=True) */
    .fuente-tag {{
        display: inline-block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        color: #8A5A20;
        background: #FCEFDC;
        border: 1px dashed #C98A3B;
        border-radius: 4px;
        padding: 0.12rem 0.5rem;
        margin: 0.35rem 0.3rem 0 0;
    }}
 
    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] > div,
    div[data-testid="stChatMessageContent"] {{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        padding: 0.2rem 0 !important;
    }}
 
    div[data-testid="stHorizontalBlock"] button {{
        font-size: 0.82rem;
        border-radius: 999px;
        border: 1px solid {C["primary"]};
        color: {C["primary"]};
    }}
    div[data-testid="stHorizontalBlock"] button:hover {{
        background: {C["primary"]};
        color: white;
    }}
 
    [data-testid="stChatInput"] {{
        background-color: {C["surface"]} !important;
        border: 1px solid {C["border"]} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input {{
        background-color: {C["surface"]} !important;
        color: {C["ink"]} !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder {{
        color: {C["ink_soft"]} !important;
        opacity: 1;
    }}
    [data-testid="stExpander"] *,
    [data-testid="stExpander"] summary {{
        color: {C["ink"]} !important;
    }}
    .st-emotion-cache-1wmy9hl,
    .st-emotion-cache-1y4o2gk,
    .stMarkdownContainer p,
    .stMarkdownContainer li,
    .stMarkdownContainer strong {{
        color: {C["ink"]} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
 
st.markdown(
    f"""
    <div class="clinic-header">
        <h1>🩺 {NOMBRE_ASISTENTE}</h1>
        <p>Asistente virtual de Clínica FIC-Integra.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
with st.expander(f"¿Qué puede y qué no puede responder {NOMBRE_ASISTENTE}?"):
    col_puede, col_no_puede = st.columns(2)
    with col_puede:
        st.markdown("**✅ Puede ayudarte con:**")
        for item in DESCRIPCION_PUEDE:
            st.markdown(f"- {item}")
    with col_no_puede:
        st.markdown("**🚫 No puede:**")
        for item in DESCRIPCION_NO_PUEDE:
            st.markdown(f"- {item}")
 
if "ultima_pregunta" not in st.session_state:
    st.session_state.ultima_pregunta = None
    st.session_state.ultima_respuesta = None
    st.session_state.ultimas_fuentes = []
 
# --- Preguntas sugeridas (solo si no se ha hecho ninguna pregunta aún) -----
if not st.session_state.ultima_pregunta:
    st.caption("Prueba con alguna de estas preguntas:")
    columnas = st.columns(2)
    for i, pregunta in enumerate(PREGUNTAS_SUGERIDAS):
        if columnas[i % 2].button(pregunta, use_container_width=True):
            st.session_state.pregunta_sugerida = pregunta
 
 
def preguntar_al_agente(pregunta: str) -> dict:
    """Llama al endpoint /preguntar de la API y devuelve respuesta + fuentes."""
    respuesta = requests.post(
        f"{API_URL}/preguntar",
        json={"pregunta": pregunta},
        timeout=60,
    )
    respuesta.raise_for_status()
    return respuesta.json()
 
 
def mostrar_mensaje(rol: str, texto: str, fuentes: list) -> None:
    es_usuario = rol == "user"
    avatar = "🧑" if es_usuario else "🩺"
    clase = "msg-user" if es_usuario else "msg-agent"
    with st.chat_message(rol, avatar=avatar):
        st.markdown(f'<div class="{clase}">{texto}</div>', unsafe_allow_html=True)
        if MOSTRAR_FUENTES and fuentes:
            tags = "".join(f'<span class="fuente-tag">📄 {f}</span>' for f in fuentes)
            st.markdown(tags, unsafe_allow_html=True)
 
 
# --- Entrada de la pregunta (sugerida o escrita a mano) ---------------------
pregunta_input = st.chat_input("Escribe tu pregunta...")
pregunta_sugerida = st.session_state.pop("pregunta_sugerida", None)
pregunta = pregunta_input or pregunta_sugerida
 
if pregunta:
    # Cada pregunta nueva REEMPLAZA la anterior en pantalla — no se
    # acumula un historial visible, a diferencia de un chat tradicional.
    st.session_state.ultima_pregunta = pregunta
 
    with st.spinner("Consultando los documentos..."):
        try:
            resultado = preguntar_al_agente(pregunta)
            st.session_state.ultima_respuesta = resultado["respuesta"]
            st.session_state.ultimas_fuentes = resultado.get("fuentes", [])
        except requests.exceptions.RequestException:
            st.session_state.ultima_respuesta = (
                "No pude conectarme con el servidor del agente. "
                "Verifica que la API esté corriendo."
            )
            st.session_state.ultimas_fuentes = []
 
# --- Mostrar solo el último intercambio (si existe) -------------------------
if st.session_state.ultima_pregunta:
    mostrar_mensaje("user", st.session_state.ultima_pregunta, [])
    mostrar_mensaje("assistant", st.session_state.ultima_respuesta, st.session_state.ultimas_fuentes)