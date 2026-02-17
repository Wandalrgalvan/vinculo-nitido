import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- 2. ESTILO VISUAL MÍSTICO ---
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
    
    /* Centrado FUERTE en barra lateral */
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
    
    /* Inputs */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #F0F2F6 !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 1px solid #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXIÓN BASE DE DATOS ---
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
        # Convertimos a string para asegurar comparación
        usuario_str = str(datos['usuario'])
        
        if usuario_str in df['usuario'].values:
            idx = df[df['usuario'] == usuario_str].index[0]
            for k, v in datos.items():
                df.at[idx, k] = v
        else:
            # Convertimos el diccionario a DataFrame
            nuevo_registro = pd.DataFrame([datos])
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except Exception as e:
        print(f"Error guardando: {e}")
        return False

# --- 4. IA CIENTÍFICA ---
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
        return "Error IA."
    except: return "Error Conexión."

# --- 5. ESTADO DE SESIÓN ---
if 'usuario_vip' not in st.session_state:
    st.session_state.usuario_vip = None
if 'trial_usado' not in st.session_state:
    st.session_state.trial_usado = False

# --- 6. BARRA LATERAL (LOGIN + PERFIL DE ÉL) ---
with st.sidebar:
    # IMAGEN INDESTRUCTIBLE (Emoji Dorado Gigante)
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 80px; margin: 0; text-shadow: 0 0 20px #D4AF37;'>🦋</h1>
            <h2 style='color: #D4AF37; margin-top: -20px;'>Zona Soberana</h2>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")
    
    # --- ZONA DE LOGIN ---
    if st.session_state.usuario_vip is None:
        st.markdown("### 🔐 Acceso VIP")
        input_clave = st.text_input("Ingresá tu Clave:", type="password", placeholder="Ej: CLAVE_WANDA")
        
        if st.button("INGRESAR"):
            if input_clave:
                data = cargar_usuario(input_clave)
                if data:
                    st.session_state.usuario_vip = data
                    st.success("¡Bienvenida!")
                    st.rerun()
                else:
                    # Si no existe, damos opción de crearla al vuelo para probar
                    st.warning("Clave nueva. Creando perfil inicial...")
                    nuevo_usuario = {
                        "usuario": input_clave,
                        "nombre_el": "", "edad": 0, "historia": "", "apego": "", "resumen_sesiones": ""
                    }
                    if guardar_datos(nuevo_usuario):
                        st.session_state.usuario_vip = nuevo_usuario
                        st.rerun()
        
        st.write("---")
        st.info("¿Querés acceso total?")
        st.link_button("💎 Comprar Pase", "https://mercadopago.com.ar")

    else:
        # --- ZONA DE PERFIL (SOLO VIPs) ---
        vip = st.session_state.usuario_vip
        st.success(f"Hola, Soberana.")
        
        st.markdown("### 📁 Expediente del Vínculo")
        st.caption("Estos datos alimentan a la IA.")
        
        with st.form("perfil_form"):
            # Cargamos datos previos o dejamos vacío
            nombre_el = st.text_input("Nombre de él:", value=vip.get('nombre_el', ''))
            
            # Manejo seguro de la edad
            try:
                edad_val = int(vip.get('edad', 0))
            except:
                edad_val = 0
                
            edad_el = st.number_input("Edad:", min_value=0, max_value=90, value=edad_val)
            
            # Selectores inteligentes
            hist_prev = vip.get('historia', 'Seleccionar...')
            apego_prev = vip.get('apego', 'Seleccionar...')
            
            list_hist = ["Seleccionar...", "Ninguno", "Padres Divorciados", "Padre Ausente", "Madre Narcisista", "Violencia", "Adicciones"]
            list_apego = ["Seleccionar...", "Evitativo (Se aleja)", "Ansioso (Persigue)", "Seguro", "Desorganizado"]
            
            # Indices seguros
            idx_hist = list_hist.index(hist_prev) if hist_prev in list_hist else 0
            idx_apego = list_apego.index(apego_prev) if apego_prev in list_apego else 0
            
            historia = st.selectbox("Trauma / Historia:", list_hist, index=idx_hist)
            apego = st.selectbox("Estilo de Apego:", list_apego, index=idx_apego)
            
            if st.form_submit_button("💾 Actualizar Expediente"):
                nuevos_datos = {
                    "usuario": vip['usuario'],
                    "nombre_el": nombre_el,
                    "edad": edad_el,
                    "historia": historia,
                    "apego": apego,
                    "resumen_sesiones": vip.get('resumen_sesiones', '')
                }
                if guardar_datos(nuevos_datos):
                    st.session_state.usuario_vip = nuevos_datos
                    st.toast("Datos actualizados.")
                    st.rerun()
        
        if st.button("Cerrar Sesión"):
            st.session_state.usuario_vip = None
            st.rerun()

# --- 7. INTERFAZ PRINCIPAL ---
st.title("💎 Vínculo Nítido")

# LÓGICA: VIP vs GRATIS
if st.session_state.usuario_vip:
    # --- MODO VIP (FULL CIENCIA) ---
    vip = st.session_state.usuario_vip
    
    # Validar si faltan datos
    if not vip.get('nombre_el') or vip.get('edad') == 0:
        st.warning("⚠️ **Falta completar el expediente.** Por favor, llená los datos de él en la barra lateral para que el análisis sea preciso.")
    else:
        st.markdown(f"### Analizando a: **{vip['nombre_el']} ({vip['edad']} años)**")
        
        tab1, tab2 = st.tabs(["🔬 Laboratorio (Neurociencia)", "👑 Consejera Real"])
        
        with tab1:
            st.write("Pegá la conversación. La IA buscará patrones biológicos y de apego.")
            chat = st.text_area("Chat:", height=200)
            
            if st.button("✨ DECODIFICAR CON CIENCIA"):
                if chat:
                    with st.spinner("Analizando dopamina, cortisol y patrones evolutivos..."):
                        # EL PROMPT CIENTÍFICO QUE TE GUSTABA
                        prompt = f"""
                        Actúa como 'Wanda Soberana': experta en Neurociencia Afectiva, Psicología Evolutiva y Trauma.
                        
                        SUJETO: {vip['nombre_el']}, {vip['edad']} años.
                        HISTORIA: {vip['historia']}. APEGO: {vip['apego']}.
                        CHAT: "{chat}"
                        
                        Dame un análisis DURO y CIENTÍFICO en 4 bloques:
                        1. 🧬 **DIAGNÓSTICO NERVIOSO:** (¿Qué activa en ella? ¿Dopamina/Cortisol? ¿Qué apego muestra él?).
                        2. 🦁 **PSICOLOGÍA EVOLUTIVA:** (¿Estrategia de corto o largo plazo? ¿Cazador o Recolector?).
                        3. 👁️ **TRADUCCIÓN NÍTIDA:** (Lo que dice vs Lo que significa).
                        4. 👑 **ESTRATEGIA SOBERANA:** (Consejo de alto valor).
                        """
                        st.markdown(consultar_ia(prompt))

        with tab2:
            st.write("Desahogate. Tu mentora te escucha.")
            consulta = st.text_area("¿Qué sentís?")
            
            if st.button("PEDIR ESTRATEGIA"):
                if consulta:
                    prompt = f"""
                    Mentora de Alto Valor. Usuaria lidiando con {vip['nombre_el']} ({vip['historia']}).
                    Consulta: "{consulta}".
                    Dame consejo estratégico y empoderador.
                    """
                    st.markdown(consultar_ia(prompt))

else:
    # --- MODO GRATIS (DEMO) ---
    st.markdown("### 👋 Test de Verdad (Gratuito)")
    st.write("Probá la IA con **un mensaje**. Para análisis profundos, ingresá tu clave.")
    
    if not st.session_state.trial_usado:
        msg = st.text_area("Mensaje confuso de él:", height=100)
        if st.button("🔍 ANALIZAR AHORA"):
            if msg:
                prompt = f"Analiza este mensaje de un hombre: '{msg}'. Sé breve y directa. ¿Miente o dice la verdad?"
                st.markdown(f"### Resultado:\n{consultar_ia(prompt)}")
                st.session_state.trial_usado = True
                st.balloons()
    else:
        st.error("🔒 **Prueba finalizada.**")
        st.info("Para análisis completos con perfil psicológico, adquirí el Pase VIP.")
        st.link_button("💎 Comprar Acceso", "https://mercadopago.com.ar")
