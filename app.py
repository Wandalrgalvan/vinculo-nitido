import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- 2. ESTILO VISUAL (CORREGIDO Y MÍSTICO) ---
st.markdown("""
    <style>
    /* Fondo Degradado */
    .stApp {
        background: rgb(45,0,70);
        background: linear-gradient(160deg, rgba(45,0,70,1) 0%, rgba(20,0,40,1) 50%, rgba(0,0,20,1) 100%);
        color: #FFFFFF;
    }
    
    /* Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #1A0525;
    }
    
    /* Centrado de imagen en barra lateral */
    [data-testid="stSidebar"] > div:first-child {
        text-align: center;
        align-items: center;
    }

    /* Botones Dorados */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDC830 100%);
        color: #000000;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        padding: 12px 24px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.6);
    }
    
    /* Cajas de texto */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: #F0F2F6 !important;
        color: #000000 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXIÓN GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_usuario(clave):
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        usuario = df[df['usuario'] == str(clave)]
        if not usuario.empty: return usuario.iloc[0].to_dict()
        return None
    except: return None

def guardar_datos(datos):
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        if str(datos['usuario']) in df['usuario'].values:
            idx = df[df['usuario'] == str(datos['usuario'])].index[0]
            for k, v in datos.items(): df.at[idx, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True)
        conn.update(worksheet="vinculo_db", data=df)
    except: pass

# --- 4. MOTOR IA ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def consultar_ia(prompt):
    if not api_key: return "Error: Falta API Key."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return "Error consultando a la IA."
    except: return "Error de conexión."

# --- 5. GESTIÓN DE ESTADO (MEMORIA TEMPORAL) ---
if 'usuario_vip' not in st.session_state:
    st.session_state.usuario_vip = None
if 'trial_usado' not in st.session_state:
    st.session_state.trial_usado = False

# --- 6. BARRA LATERAL ---
with st.sidebar:
    # IMAGEN INDESTRUCTIBLE (Usamos un Emoji gigante o Icono SVG inline)
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 80px; margin: 0;'>🦋</h1>
            <h2 style='color: #D4AF37; margin-top: -20px;'>Zona Soberana</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # ZONA DE LOGIN
    if st.session_state.usuario_vip is None:
        st.markdown("### 🔐 Ingreso VIP")
        input_clave = st.text_input("Tu Clave de Acceso:", type="password", placeholder="Ej: MARIA_01")
        if st.button("INGRESAR"):
            if input_clave:
                data = cargar_usuario(input_clave)
                if data:
                    st.session_state.usuario_vip = data
                    st.success(f"¡Bienvenida {data['nombre_el']}!")
                    st.rerun()
                else:
                    st.error("Clave no encontrada o incorrecta.")
            else:
                st.warning("Escribí tu clave.")
        
        st.write("---")
        st.info("¿Querés acceso ilimitado?")
        st.link_button("💎 Comprar Pase VIP", "https://mercadopago.com.ar") # Tu link real
        
    else:
        # SI YA ESTÁ LOGUEADA
        vip = st.session_state.usuario_vip
        st.success("✅ Sesión Activa")
        st.write(f"Vínculo: **{vip['nombre_el']}**")
        
        if st.button("Cerrar Sesión"):
            st.session_state.usuario_vip = None
            st.rerun()

# --- 7. INTERFAZ PRINCIPAL ---
st.title("💎 Vínculo Nítido")

# LÓGICA DE PESTAÑAS SEGÚN SI ES VIP O NO
if st.session_state.usuario_vip:
    # --- MODO VIP (FULL) ---
    tab1, tab2 = st.tabs(["🔬 Laboratorio (Chat)", "👑 Consejera Real"])
    
    with tab1:
        st.info(f"Analizando a **{vip['nombre_el']}** con historial completo.")
        chat = st.text_area("Pegá el chat completo:", height=200)
        if st.button("DECODIFICAR (VIP)"):
            if chat:
                with st.spinner("Procesando trauma, apego y lenguaje no verbal..."):
                    prompt = f"Analiza este chat de {vip['nombre_el']} ({vip['edad']} años, historia: {vip['historia']}). Chat: {chat}. Dame Diagnóstico, Verdad Biológica y Consejo Soberano."
                    st.markdown(consultar_ia(prompt))
    
    with tab2:
        consulta = st.text_area("¿Qué te preocupa hoy?")
        if st.button("PEDIR CONSEJO"):
            if consulta:
                prompt = f"Consejera experta. Usuaria con problema con {vip['nombre_el']}. Consulta: {consulta}. Dame estrategia de alto valor."
                st.markdown(consultar_ia(prompt))

else:
    # --- MODO GRATIS (DEMO LIMITADA) ---
    st.markdown("### 👋 Bienvenida al Detector de Mentiras")
    st.write("Probá el poder de la IA con **un solo mensaje**. Para análisis completos, necesitás el Pase VIP.")
    
    if not st.session_state.trial_usado:
        test_chat = st.text_area("Pegá UN mensaje confuso que te mandó él:", height=100, placeholder="Ej: 'No sos vos, soy yo...'")
        
        if st.button("🔍 ANALIZAR GRATIS"):
            if test_chat:
                with st.spinner("Analizando patrones..."):
                    prompt = f"Analiza brevemente este mensaje de un hombre a una mujer: '{test_chat}'. ¿Qué significa realmente? Sé directa."
                    res = consultar_ia(prompt)
                    st.markdown(f"### 👁️ Traducción:\n{res}")
                    st.markdown("---")
                    st.warning("⚠️ **Has gastado tu prueba gratuita.**")
                    st.session_state.trial_usado = True # BLOQUEAMOS
                    st.balloons()
            else:
                st.warning("Escribí algo para probar.")
    else:
        # PANTALLA DE BLOQUEO DESPUÉS DE USAR
        st.error("🔒 **Prueba Finalizada**")
        st.markdown("### ¿Querés saber toda la verdad?")
        st.write("Tu intuición te trajo hasta acá. No te quedes con la duda.")
        st.write("El Pase VIP incluye:")
        st.markdown("""
        - ✅ Análisis ilimitados de chats largos.
        - ✅ Historial de memoria (la IA recuerda tu caso).
        - ✅ Consejera 24/7.
        """)
        st.link_button("💎 COMPRAR ACCESO AHORA", "https://mercadopago.com.ar")
