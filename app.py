import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- ESTILO VISUAL MÍSTICO ---
st.markdown("""
    <style>
    /* Fondo */
    .stApp {
        background: rgb(45,0,70);
        background: linear-gradient(160deg, rgba(45,0,70,1) 0%, rgba(20,0,40,1) 50%, rgba(0,0,20,1) 100%);
        color: #FFFFFF;
    }
    
    /* Barra Lateral */
    section[data-testid="stSidebar"] { background-color: #1A0525; }
    [data-testid="stSidebar"] > div:first-child { text-align: center; }

    /* Botones Dorados */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDC830 100%);
        color: black; font-weight: bold; border-radius: 25px; border: none; width: 100%;
        text-transform: uppercase; margin-top: 10px;
    }
    
    /* Inputs */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: #F0F2F6 !important; color: black !important; border-radius: 10px;
    }
    
    /* Efecto Borroso (Censura) */
    .blur-text {
        color: transparent; text-shadow: 0 0 10px rgba(255,255,255,0.7); user-select: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A BASE DE DATOS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def gestionar_usuario(clave):
    """Busca o Crea usuario automáticamente."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        usuario = df[df['usuario'] == str(clave)]
        
        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        else:
            # CREAR USUARIO NUEVO
            nuevo = {
                "usuario": clave, "nombre_el": "", "edad": 0, 
                "historia": "No especificado", "apego": "No especificado", "resumen_sesiones": ""
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            conn.update(worksheet="vinculo_db", data=df)
            return nuevo
    except: return None

def guardar_historial(usuario_dict, nuevo_resumen):
    """Guarda memoria en el Excel."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        idx = df[df['usuario'] == str(usuario_dict['usuario'])].index[0]
        historial_viejo = str(usuario_dict.get('resumen_sesiones', ''))
        df.at[idx, 'resumen_sesiones'] = f"{nuevo_resumen} | {historial_viejo}"[:4000]
        conn.update(worksheet="vinculo_db", data=df)
    except: pass

def actualizar_perfil(datos):
    """Actualiza datos del sujeto."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        idx = df[df['usuario'] == str(datos['usuario'])].index[0]
        for k, v in datos.items(): df.at[idx, k] = v
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except: return False

# --- MOTOR IA (EL AUTO-DETECT QUE ARREGLA ERRORES) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def obtener_modelo_valido(api_key):
    """Busca qué modelo funciona realmente."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            for modelo in datos.get('models', []):
                if 'generateContent' in modelo.get('supportedGenerationMethods', []):
                    if 'gemini' in modelo['name']: return modelo['name']
            return "models/gemini-pro"
        return None
    except: return None

def consultar_ia(prompt):
    if not api_key: return "Error: Falta API Key."
    modelo = obtener_modelo_valido(api_key)
    if not modelo: return "Error de conexión con Google AI."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/{modelo}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Error ({res.status_code}): Intenta de nuevo."
    except Exception as e: return f"Error: {str(e)}"

# --- ESTADO DE SESIÓN ---
if 'vip_user' not in st.session_state:
    st.session_state.vip_user = None

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin:0;'>🦋</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Zona Soberana</h3>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.vip_user is None:
        st.info("🔐 **ACCESO VIP**")
        clave = st.text_input("Ingresá tu Clave:", type="password", help="Si compraste el pase, usá la clave que recibiste.")
        if st.button("INGRESAR"):
            if clave:
                with st.spinner("Verificando..."):
                    user = gestionar_usuario(clave)
                    if user:
                        st.session_state.vip_user = user
                        st.rerun()
                    else:
                        st.error("Error de conexión.")
        
        st.write("---")
        st.caption("¿Solo mirando?")
        st.write("Usá las pestañas gratuitas de la derecha 👉")
        st.link_button("💎 Comprar Pase VIP", "https://mercadopago.com.ar")

    else:
        # USUARIA LOGUEADA
        vip = st.session_state.vip_user
        st.success(f"Hola, Soberana.")
        
        with st.expander("⚙️ Perfil de ÉL (Datos Clave)", expanded=True):
            with st.form("perfil"):
                nombre = st.text_input("Nombre:", value=vip['nombre_el'])
                edad = st.number_input("Edad:", value=int(vip['edad']) if vip['edad'] else 0)
                historia = st.selectbox("Historia:", ["No especificado", "Padres Divorciados", "Padre Ausente", "Violencia", "Narcisismo"], index=0)
                apego = st.selectbox("Apego:", ["No especificado", "Evitativo", "Ansioso", "Seguro"], index=0)
                
                if st.form_submit_button("💾 Guardar Datos"):
                    vip['nombre_el'] = nombre
                    vip['edad'] = edad
                    vip['historia'] = historia
                    vip['apego'] = apego
                    if actualizar_perfil(vip):
                        st.session_state.vip_user = vip
                        st.toast("Perfil Actualizado")
                        st.rerun()

        if st.button("Cerrar Sesión"):
            st.session_state.vip_user = None
            st.rerun()

# --- PANTALLA PRINCIPAL ---
st.title("💎 Vínculo Nítido")

# PESTAÑAS (Las gratuitas primero)
tab_apego, tab_detector, tab_vip = st.tabs(["🎁 Test Apego (Gratis)", "🕵️‍♀️ Detector (Gratis)", "🔥 VIP Total"])

# --- TAB 1: TEST DE APEGO (GRATIS Y RÁPIDO) ---
with tab_apego:
    st.header("Descubrí su Estilo de Apego")
    st.write("Respondé rápido para identificar su patrón:")
    
    p1 = st.radio("1. Cuando hay mucha intimidad emocional, él:", 
                  ["Se aleja, se enfría o pide 'espacio'", 
                   "Se pone intenso y necesita validación constante", 
                   "Se mantiene tranquilo y comunica lo que siente"])
    
    p2 = st.radio("2. Ante un conflicto o reclamo tuyo:", 
                  ["Evita el tema, se va o te aplica la Ley del Hielo", 
                   "Explota, te culpa y da vuelta la tortilla", 
                   "Escucha e intenta buscar una solución"])
    
    if st.button("VER DIAGNÓSTICO DE APEGO"):
        st.divider()
        if "aleja" in p1 or "Evita" in p2:
            st.error("🚨 **Resultado: APEGO EVITATIVO**")
            st.write("Su sistema nervioso interpreta la intimidad como una pérdida de libertad. No es que no te quiera, es que tiene **miedo**. Su estrategia es desactivarse para regularse.")
        elif "intenso" in p1 or "Explota" in p2:
            st.warning("🥺 **Resultado: APEGO ANSIOSO / REACTIVO**")
            st.write("Tiene terror al abandono. Sus reacciones exageradas son intentos (mal adaptados) de reconectar con vos.")
        else:
            st.success("✅ **Resultado: APEGO SEGURO**")
            st.write("Parece tener herramientas emocionales sanas. Si sentís inseguridad, revisá tus propios patrones.")
            
        st.info("💡 **¿Querés saber qué hacer con este diagnóstico?** Pasate a la pestaña VIP para la estrategia.")

# --- TAB 2: DETECTOR DE MENTIRAS (GANCHO DE VENTA) ---
with tab_detector:
    st.subheader("¿Te mandó un mensaje confuso?")
    st.write("Pegalo acá. La IA te dirá la verdad, pero la estrategia es para las VIP.")
    
    msg = st.text_area("Pegá el mensaje:", height=100, placeholder="Ej: No sos vos, soy yo...")
    
    if st.button("🔍 ANALIZAR VERDAD"):
        if msg:
            with st.spinner("Analizando..."):
                prompt = f"Analiza este mensaje: '{msg}'. Dime qué significa realmente y si es manipulación. NO DES CONSEJOS."
                res = consultar_ia(prompt)
                
                st.markdown(f"### 👁️ La Verdad Cruda:")
                st.write(res)
                
                st.divider()
                st.markdown("### 👑 Estrategia Soberana (Bloqueado)")
                st.markdown("""
                <div class="blur-text">
                Para responder a esto con dignidad, debes aplicar el silencio estratégico por 12 horas. 
                Luego responde: "Entiendo que necesites espacio..."
                </div>
                """, unsafe_allow_html=True)
                
                st.warning("🔒 **Para ver la respuesta exacta, ingresá tu Clave VIP.**")

# --- TAB 3: ZONA VIP (FULL) ---
with tab_vip:
    if st.session_state.vip_user is None:
        st.info("🔒 **Zona Restringida**")
        st.write("Ingresá tu clave en la barra lateral (izquierda) para desbloquear:")
        st.markdown("- 🧬 Análisis con Neurociencia")
        st.markdown("- 🧠 Memoria del Vínculo")
        st.markdown("- 👑 Consejera Personal")
        st.stop()
    
    # SI TIENE CLAVE:
    vip = st.session_state.vip_user
    st.success(f"🔓 **Laboratorio Abierto:** Analizando a {vip.get('nombre_el', 'Sujeto')}")
    
    modo = st.radio("Herramienta:", ["🔬 Análisis de Chat", "👑 Consejera Real"], horizontal=True)
    
    if modo == "🔬 Análisis de Chat":
        chat_vip = st.text_area("Pegá la conversación completa:", height=200)
        if st.button("✨ DECODIFICAR CON CIENCIA"):
            if chat_vip:
                historial = vip.get('resumen_sesiones', '')
                prompt = f"""
                Actúa como Wanda Soberana (Experta en Neurociencia y Relaciones).
                SUJETO: {vip['nombre_el']}, {vip['edad']} años, {vip['historia']}, {vip['apego']}.
                HISTORIAL: {historial}
                CHAT: "{chat_vip}"
                
                Analiza:
                1. 🧬 **Diagnóstico Nervioso:** (Dopamina/Cortisol/Apego).
                2. 🦁 **Estrategia Evolutiva:** (¿Cazador o Recolector?).
                3. 👁️ **Traducción Real.**
                4. 👑 **Estrategia Soberana:** (Qué responder exactamente).
                
                AL FINAL escribe: "MEMORIA_DB: [Resumen de 1 linea]"
                """
                res = consultar_ia(prompt)
                
                if "MEMORIA_DB:" in res:
                    parts = res.split("MEMORIA_DB:")
                    st.markdown(parts[0])
                    guardar_historial(vip, f"{datetime.now().strftime('%d/%m')}: {parts[1].strip()}")
                else:
                    st.markdown(res)
                    
    elif modo == "👑 Consejera Real":
        consulta = st.text_area("¿Qué sentís hoy?")
        if st.button("PEDIR ESTRATEGIA"):
            if consulta:
                prompt = f"Consejera experta. Usuaria: {vip['nombre_el']} ({vip['historia']}). Problema: {consulta}. Dame consejo empoderador."
                st.markdown(consultar_ia(prompt))
