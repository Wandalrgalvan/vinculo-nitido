import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN (TÍTULO Y DISEÑO) ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- 2. ESTILO VISUAL MÍSTICO Y "MOBILE FIRST" ---
st.markdown("""
    <style>
    /* Fondo Degradado Místico */
    .stApp {
        background: rgb(45,0,70);
        background: linear-gradient(160deg, rgba(45,0,70,1) 0%, rgba(20,0,40,1) 50%, rgba(0,0,20,1) 100%);
        color: #FFFFFF;
    }
    
    /* Cajas de Texto (Más parecidas a WhatsApp) */
    .stTextArea>div>div>textarea {
        background-color: #F0F2F6 !important;
        color: #111 !important;
        border-radius: 15px !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Botones Dorados (Llamado a la acción) */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDC830 100%);
        color: black;
        font-weight: bold;
        border-radius: 25px;
        border: none;
        width: 100%;
        padding: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover { transform: scale(1.02); }

    /* Efecto de "Censura" para el modo gratis */
    .blur-text {
        color: transparent;
        text-shadow: 0 0 8px rgba(255,255,255,0.5);
        user-select: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXIÓN A GOOGLE SHEETS (BASE DE DATOS) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def gestionar_usuario(clave):
    """Sistema de Auto-Login: Busca o Crea usuario en el Excel"""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        usuario = df[df['usuario'] == str(clave)]
        
        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        else:
            # Si la clave es válida (la que vos vendiste), creamos el perfil
            nuevo = {
                "usuario": clave, "nombre_el": "", "edad": 0, 
                "historia": "No especificado", "apego": "No especificado", "resumen_sesiones": ""
            }
            # Guardamos en Excel
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            conn.update(worksheet="vinculo_db", data=df)
            return nuevo
    except: return None

def guardar_historial(usuario_dict, nuevo_resumen):
    """Guarda el resumen de la sesión en el Excel"""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        idx = df[df['usuario'] == str(usuario_dict['usuario'])].index[0]
        
        # Concatenamos el historial nuevo con el viejo
        historial_viejo = str(usuario_dict.get('resumen_sesiones', ''))
        df.at[idx, 'resumen_sesiones'] = f"{nuevo_resumen} | {historial_viejo}"[:5000] # Límite de caracteres
        
        conn.update(worksheet="vinculo_db", data=df)
    except: pass

# --- 4. CEREBRO IA (CON PROMPT DE LA SOBERANA) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def consultar_ia(prompt):
    if not api_key: return "Error: Falta API Key"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return "Error en la IA. Intenta de nuevo."
    except: return "Error de conexión."

# --- 5. LÓGICA DE SESIÓN ---
if 'vip_user' not in st.session_state:
    st.session_state.vip_user = None

# --- 6. BARRA LATERAL (EL ACCESO) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🦋</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Zona Soberana</h3>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.vip_user is None:
        st.info("💎 ¿Tenés tu Pase VIP?")
        clave = st.text_input("Ingresá tu Clave de Acceso:", type="password")
        if st.button("INGRESAR"):
            if clave:
                user = gestionar_usuario(clave)
                if user:
                    st.session_state.vip_user = user
                    st.rerun()
                else:
                    st.error("Clave incorrecta. Revisá tu mail de compra.")
        
        st.write("---")
        st.markdown("### ¿No tenés clave?")
        st.write("Dormí tranquila hoy. Obtené respuestas inmediatas.")
        # LINK DE PAGO REAL (Automatización)
        st.link_button("👉 OBTENER ACCESO YA", "https://link.mercadopago.com.ar/tu_link_aca")

    else:
        # USUARIA LOGUEADA
        vip = st.session_state.vip_user
        st.success(f"Hola, Soberana.")
        
        # PERFIL DEL SUJETO (Simplificado)
        with st.expander("⚙️ Configurar a ÉL", expanded=True):
            with st.form("perfil"):
                nombre = st.text_input("Nombre:", value=vip['nombre_el'])
                edad = st.number_input("Edad:", value=int(vip['edad']) if vip['edad'] else 0)
                historia = st.selectbox("Historia:", ["Normal", "Padres Divorciados", "Padre Ausente", "Violencia/Adicciones", "Narcisismo"], index=0)
                if st.form_submit_button("Guardar Perfil"):
                    # Aquí iría la lógica de guardar perfil completo (simplificado para el ejemplo)
                    st.toast("Perfil actualizado")

        if st.button("Cerrar Sesión"):
            st.session_state.vip_user = None
            st.rerun()

# --- 7. PANTALLA PRINCIPAL ---
st.title("💎 Vínculo Nítido")

# PESTAÑAS ESTRATÉGICAS
tab_free, tab_vip, tab_help = st.tabs(["🎁 Prueba Gratis", "🔥 Análisis VIP", "🆘 Consejera"])

# --- PESTAÑA 1: EL GANCHO (Diagnóstico Gratis, Solución Paga) ---
with tab_free:
    st.subheader("¿Qué te dijo él?")
    st.write("Pegá ese mensaje que te tiene dando vueltas. Te diré qué significa, pero la estrategia es VIP.")
    
    chat_free = st.text_area("Pegá el mensaje acá:", height=100, placeholder="Ej: 'No sos vos, soy yo...'")
    
    if st.button("🔍 ANALIZAR VERDAD"):
        if chat_free:
            with st.spinner("Analizando micro-expresiones y patrones..."):
                # PROMPT GANCHO
                prompt = f"""
                Actúa como Wanda Soberana. Analiza este mensaje: "{chat_free}".
                1. Dime qué significa realmente (Traducción cruda).
                2. Dime qué patrón psicológico es (Gaslighting, Breadcrumbing, etc).
                3. NO DES NINGÚN CONSEJO. Solo el diagnóstico doloroso.
                """
                resultado = consultar_ia(prompt)
                
                st.markdown(f"### 👁️ La Realidad:")
                st.write(resultado)
                
                st.divider()
                st.markdown("### 👑 Estrategia Soberana (Bloqueada)")
                st.markdown("""
                <div class="blur-text">
                Para responder esto con dignidad y recuperar tu poder, deberías aplicar la técnica del espejo invertido. 
                No le contestes inmediatamente. Espera 4 horas y dile exactamente lo siguiente: 
                "Entiendo perfectamente..."
                </div>
                """, unsafe_allow_html=True)
                
                st.warning("🔒 **¿Querés leer la estrategia y saber qué responder?**")
                st.write("No cometas el error de responder desde la ansiedad.")
                st.link_button("💎 DESBLOQUEAR RESPUESTA AHORA", "https://link.mercadopago.com.ar/tu_link_aca")

# --- PESTAÑA 2: VIP (FULL POWER) ---
with tab_vip:
    if st.session_state.vip_user is None:
        st.info("🔒 Ingresá tu clave en la barra lateral para acceder al Laboratorio.")
        st.stop()
    
    vip = st.session_state.vip_user
    st.markdown(f"### 🔬 Laboratorio: Analizando a {vip.get('nombre_el', 'Sujeto')}")
    
    chat_vip = st.text_area("Pegá la conversación COMPLETA:", height=200)
    
    if st.button("✨ DECODIFICAR CON CIENCIA"):
        if chat_vip:
            historial = vip.get('resumen_sesiones', '')
            with st.spinner("Consultando base de datos de Neurociencia y Trauma..."):
                
                # --- EL PROMPT MAESTRO DE LA SOBERANA (RECUPERADO) ---
                prompt_maestro = f"""
                Actúa como 'Wanda Soberana': Experta en Neurociencia Afectiva, Psicología Evolutiva y Relaciones de Alto Valor.
                
                DATOS DEL SUJETO:
                - Edad: {vip.get('edad')}
                - Historia/Trauma: {vip.get('historia')}
                - Historial Previo del Vínculo: {historial}
                
                CHAT A ANALIZAR: "{chat_vip}"
                
                Analiza PROFUNDAMENTE en 4 pasos:
                
                1. 🧬 **BIOLOGÍA Y NEUROCIENCIA:**
                   - ¿Qué cóctel químico busca él? (Dopamina rápida, validación).
                   - ¿Qué está activando en ELLA? (Adicción al refuerzo intermitente, Cortisol).
                   
                2. 🦁 **PSICOLOGÍA EVOLUTIVA & APEGO:**
                   - Diagnóstico de Apego (Evitativo, Ansioso, Desorganizado).
                   - Estrategia reproductiva: ¿Cazador (Inversión) o Recolector (Oportunista)?
                   
                3. 👁️ **TRADUCCIÓN NÍTIDA:**
                   - Lo que dice: "..."
                   - Lo que realmente piensa: "..." (Sé cruda).
                   
                4. 👑 **ESTRATEGIA SOBERANA (ACCIONABLE):**
                   - Exactamente qué responder (Copy-Paste).
                   - O si debe aplicar Contacto Cero.
                   - Cómo recuperar el marco de poder.
                
                AL FINAL, escribe: "MEMORIA_DB: [Resumen de 1 linea de lo que pasó hoy para guardar en el excel]"
                """
                
                respuesta = consultar_ia(prompt_maestro)
                
                # Lógica para mostrar respuesta y guardar memoria
                if "MEMORIA_DB:" in respuesta:
                    partes = respuesta.split("MEMORIA_DB:")
                    texto_visible = partes[0]
                    memoria_nueva = partes[1].strip()
                    
                    st.markdown(texto_visible)
                    
                    # Guardamos automáticamente en segundo plano
                    guardar_historial(vip, f"{datetime.now().strftime('%d/%m')}: {memoria_nueva}")
                    st.toast("🧠 Memoria del vínculo actualizada en tu expediente.")
                else:
                    st.markdown(respuesta)

# --- PESTAÑA 3: CONSEJERA ---
with tab_vip: # Reutilizamos lógica VIP
    pass # Ya está en las tabs de arriba, solo agregamos contenido aquí si queremos separar
