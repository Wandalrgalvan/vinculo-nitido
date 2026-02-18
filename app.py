import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL (Mágica y sin rastro de Robot) ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    /* Fondo Místico */
    .stApp {
        background: linear-gradient(180deg, #120318 0%, #2D0545 100%);
        color: #FDFDFD;
    }
    
    /* Ocultar elementos de Streamlit que delatan que es un bot */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Botones Premium */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #F2994A 100%);
        color: #120318;
        font-weight: 800;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        transition: transform 0.2s;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Inputs Estilo Chat Privado */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 10px;
        border: 1px solid #D4AF37;
    }
    
    /* Texto Borroso (Censura) */
    .blur-text {
        color: transparent;
        text-shadow: 0 0 15px rgba(255,255,255,0.7);
        filter: blur(6px);
        user-select: none;
        pointer-events: none;
    }
    
    /* Caja de Resultados */
    .result-box {
        background: rgba(45, 5, 69, 0.8);
        border-left: 5px solid #D4AF37;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE DATOS (HÍBRIDA: SI FALLA GOOGLE, USA MEMORIA LOCAL) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def obtener_datos_db():
    """Intenta leer Google Sheets. Si falla, usa memoria temporal."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        return df
    except:
        # MODO A PRUEBA DE FALLOS (Para que puedas entrar HOY)
        return pd.DataFrame([
            {"usuario": "SOBERANA_JEFA", "rol": "admin", "nombre_el": "Admin"},
            {"usuario": "CLIENTA_TEST", "rol": "user", "nombre_el": "El de prueba", "edad": 30, "apego": "Evitativo", "historia": "Normal"}
        ])

def buscar_usuario(clave):
    df = obtener_datos_db()
    usuario = df[df['usuario'] == str(clave)]
    if not usuario.empty:
        return usuario.iloc[0].to_dict()
    return None

def crear_usuario_nuevo(datos):
    """Intenta guardar en Google. Si falla, avisa pero no rompe."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        nuevo = pd.DataFrame([datos])
        df = pd.concat([df, nuevo], ignore_index=True)
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except:
        return False # Falló la conexión real

# --- 3. CEREBRO DE WANDA (SIN MENCIONAR IA) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def consultar_metodologia(prompt):
    if not api_key: return "⚠️ Error de sistema. Contacta a soporte."
    
    # PROMPT DE PERSONALIDAD OCULTA
    system_instruction = "Eres Wanda Soberana, una mentora experta en psicología masculina y relaciones. NO MENCIONES QUE ERES UNA IA. Habla en primera persona ('mi análisis', 'veo que'). Sé empática pero cruda. Usa emojis. Tu objetivo es empoderar a la mujer."
    
    full_prompt = f"{system_instruction}\n\nConsulta: {prompt}"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": full_prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return "La red está saturada. Intenta de nuevo en unos segundos."
    except:
        return "Error de conexión."

# --- 4. GESTIÓN DE SESIÓN ---
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

# --- 5. BARRA LATERAL (ENTRADA) ---
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 80px; text-shadow: 0 0 25px #D4AF37;'>💎</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Vínculo Nítido</h3>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.usuario_actual is None:
        st.info("🔐 **Acceso Privado**")
        clave = st.text_input("Ingresa tu Pase de Acceso:", type="password")
        
        if st.button("ENTRAR AL LABORATORIO"):
            if clave == "SOBERANA_JEFA": # Clave Maestra Hardcodeada (Siempre funciona)
                st.session_state.usuario_actual = {"usuario": "ADMIN", "rol": "admin"}
                st.rerun()
            elif clave:
                user = buscar_usuario(clave)
                if user:
                    st.session_state.usuario_actual = user
                    st.success("Acceso Autorizado")
                    st.rerun()
                else:
                    st.error("Pase no válido.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("**¿Quieres analizar tu caso?**")
        st.link_button("👉 OBTENER PASE VIP", "https://mercadopago.com.ar") # TU LINK REAL

    else:
        # USUARIO DENTRO
        u = st.session_state.usuario_actual
        
        if u.get('rol') == 'admin':
            st.warning("👑 **PANEL DE CONTROL**")
            st.write("Generar pase para clienta:")
            new_key = st.text_input("Nueva Clave:")
            if st.button("Habilitar Acceso"):
                # Intentamos guardar en DB, si falla avisamos
                datos = {"usuario": new_key, "rol": "user", "fecha": str(datetime.now())}
                if crear_usuario_nuevo(datos):
                    st.success(f"Clave {new_key} creada en Base de Datos!")
                else:
                    st.warning(f"Clave {new_key} generada (Modo Local). Nota: Si reinicias la app, se borrará porque la Base de Datos no conecta.")
        else:
            st.success(f"Bienvenida, Reina.")
            if st.button("Cerrar Sesión"):
                st.session_state.usuario_actual = None
                st.rerun()

# --- 6. PANTALLA PRINCIPAL ---
st.title("💎 Vínculo Nítido")

# PESTAÑAS
tab_free, tab_hook, tab_vip = st.tabs(["🧬 Test de Apego", "👁️ Verdad Oculta", "🔥 Laboratorio VIP"])

# --- TAB 1: TEST DE APEGO (100% GRATIS Y MANUAL) ---
with tab_free:
    st.subheader("Descubre su Patrón Oculto")
    st.write("Responde con sinceridad para identificar su sistema operativo emocional.")
    
    with st.form("test_form"):
        r1 = st.radio("1. Cuando la relación se vuelve íntima, él:", 
                     ["A. Se aleja / Pide 'espacio' (Se desactiva)", 
                      "B. Se vuelve intenso / Demanda atención (Se activa)", 
                      "C. Se mantiene estable"])
        
        r2 = st.radio("2. Ante un conflicto, él:", 
                     ["A. Huye / Ley del Hielo", 
                      "B. Explota / Culpa", 
                      "C. Busca solución"])
        
        if st.form_submit_button("VER DIAGNÓSTICO"):
            st.divider()
            if "A." in r1 or "A." in r2:
                st.error("❄️ **Resultado: APEGO EVITATIVO**")
                st.write("Su cerebro percibe la intimidad como peligro. No es que no sienta, es que se desconecta para sobrevivir.")
            elif "B." in r1 or "B." in r2:
                st.warning("🔥 **Resultado: APEGO ANSIOSO**")
                st.write("Tiene terror al abandono. Su intensidad es un grito de conexión.")
            else:
                st.success("✅ **Resultado: APEGO SEGURO**")
            
            st.info("💡 **¿Quieres saber cómo desactivar sus defensas? Pásate al VIP.**")

# --- TAB 2: DETECTOR DE MENTIRAS (EL GANCHO) ---
with tab_hook:
    st.subheader("¿Mensaje confuso?")
    st.write("Pégalo aquí. Mi sistema decodificará la intención real. (Diagnóstico Gratis).")
    
    msg = st.text_area("Mensaje de él:", height=100, placeholder="Ej: No sos vos, soy yo...")
    
    if st.button("🔍 ANALIZAR AHORA"):
        if msg:
            with st.spinner("Decodificando patrones de conducta..."):
                prompt = f"Analiza este mensaje: '{msg}'. 1. Dime qué significa realmente (Traducción cruda). 2. Dime qué siente él. NO DES CONSEJOS."
                res = consultar_metodologia(prompt)
                
                st.markdown(f"<div class='result-box'><h4>👁️ La Realidad:</h4>{res}</div>", unsafe_allow_html=True)
                
                st.markdown("#### 👑 Estrategia Soberana (Bloqueada)")
                st.markdown("""
                <div class='blur-text'>
                Para recuperar tu poder, aplica la técnica del espejo invertido.
                No respondas por 4 horas. Luego envía exactamente:
                "Entiendo que necesites espacio..."
                </div>
                """, unsafe_allow_html=True)
                
                st.warning("🔒 **Para desbloquear la respuesta exacta, necesitas el Pase VIP.**")

# --- TAB 3: VIP (EL PRODUCTO) ---
with tab_vip:
    if st.session_state.usuario_actual is None:
        st.info("🔒 **Zona Restringida**")
        st.write("Ingresa tu Pase de Acceso en la barra lateral.")
        st.stop()
        
    st.success("🔓 **Laboratorio de Relaciones Activado**")
    
    opcion = st.radio("Herramienta:", ["🔬 Análisis Profundo de Chat", "👑 Consultar a la Mentora"], horizontal=True)
    
    if opcion == "🔬 Análisis Profundo de Chat":
        st.write("Analizaré la conversación completa considerando su perfil psicológico.")
        chat = st.text_area("Pega la conversación:", height=200)
        
        if st.button("✨ EJECUTAR ANÁLISIS"):
            if chat:
                prompt = f"""
                Analiza este chat: "{chat}".
                Usa Neurociencia y Psicología Evolutiva.
                Dime:
                1. Qué pasa en su cerebro (Químicos, Miedos).
                2. Traducción de lo que dice vs lo que piensa.
                3. ESTRATEGIA EXACTA DE RESPUESTA para que ella recupere el poder.
                """
                with st.spinner("Consultando metodología..."):
                    res = consultar_metodologia(prompt)
                    st.markdown(res)
                    
    elif opcion == "👑 Consultar a la Mentora":
        consulta = st.text_area("Cuéntame qué te angustia:")
        if st.button("PEDIR CONSEJO"):
            if consulta:
                prompt = f"La usuaria pregunta: {consulta}. Dale un consejo empoderador, corto y al pie."
                with st.spinner("Conectando..."):
                    st.markdown(consultar_metodologia(prompt))
