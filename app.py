import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- 2. ESTILO VISUAL (MÍSTICO, ELEGANTE Y MOBILE-FIRST) ---
st.markdown("""
    <style>
    /* Fondo Degradado Profundo y Místico */
    .stApp {
        background: linear-gradient(180deg, #1A0525 0%, #300545 100%);
        color: #FDFDFD;
    }
    
    /* Títulos y Encabezados */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #F2C94C !important;
    }

    /* Botones Dorados (Llamado a la Acción) */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #F2994A 100%);
        color: #1A0525;
        font-weight: 800;
        border: none;
        border-radius: 12px;
        padding: 0.8rem;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(242, 201, 76, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(242, 201, 76, 0.5);
    }
    
    /* Inputs amigables (Estilo WhatsApp/Chat) */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #F3F4F6 !important;
        color: #111 !important;
        border-radius: 12px;
        border: 2px solid #D4AF37;
    }
    
    /* Efecto Borroso (Censura para ventas) */
    .blur-text {
        color: transparent;
        text-shadow: 0 0 12px rgba(255,255,255,0.6);
        filter: blur(5px);
        user-select: none;
        pointer-events: none;
    }
    
    /* Cajas de Resultado */
    .result-box {
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #F2C94C;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXIÓN A BASE DE DATOS (Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def buscar_usuario(clave):
    """Verifica si la clave existe en el Excel."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        usuario = df[df['usuario'] == str(clave)]
        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        return None
    except Exception as e:
        return None

def crear_usuario_admin(datos):
    """Función para que la Dueña cree usuarios."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        nuevo_df = pd.DataFrame([datos])
        df = pd.concat([df, nuevo_df], ignore_index=True)
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except: return False

def actualizar_perfil(datos):
    """Guarda cambios en el perfil del vínculo."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        idx = df[df['usuario'] == str(datos['usuario'])].index[0]
        for k, v in datos.items():
            df.at[idx, k] = v
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except: return False

def guardar_memoria(usuario, nueva_memoria):
    """Agrega el resumen de la sesión al historial."""
    try:
        historial_viejo = usuario.get('resumen_sesiones', '')
        usuario['resumen_sesiones'] = f"{nueva_memoria} | {historial_viejo}"[:4000]
        actualizar_perfil(usuario)
    except: pass

# --- 4. INTELIGENCIA ARTIFICIAL (CONEXIÓN DIRECTA) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def consultar_ia(prompt):
    if not api_key: return "⚠️ Error: Falta configurar la API Key."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return "La IA está tomando un respiro. Intenta de nuevo en unos segundos."
    except:
        return "Error de conexión."

# --- 5. GESTIÓN DE SESIÓN ---
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

# --- 6. BARRA LATERAL (CONTROL DE ACCESO) ---
with st.sidebar:
    # Logo Emoji Gigante (Indestructible)
    st.markdown("<div style='text-align: center; font-size: 80px; text-shadow: 0 0 20px #D4AF37;'>🦋</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37; margin-top:-10px;'>Zona Soberana</h3>", unsafe_allow_html=True)
    st.write("---")

    # --- LÓGICA DE LOGIN ---
    if st.session_state.usuario_actual is None:
        st.info("🔐 **Área de Miembros**")
        clave_ingresada = st.text_input("Tu Clave VIP:", type="password", placeholder="Ej: CLAVE_WANDA")
        
        if st.button("INGRESAR"):
            # 1. LLAVE MAESTRA (TUYA)
            if clave_ingresada == "WANDA_ADMIN":
                st.session_state.usuario_actual = {"usuario": "ADMIN", "rol": "admin"}
                st.rerun()
            
            # 2. CLIENTA
            elif clave_ingresada:
                with st.spinner("Verificando acceso..."):
                    user = buscar_usuario(clave_ingresada)
                    if user:
                        st.session_state.usuario_actual = user
                        st.success("¡Bienvenida Reina!")
                        st.rerun()
                    else:
                        st.error("Clave no encontrada.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ¿Aún no eres VIP?")
        st.caption("Desbloquea el análisis científico y tu consejera 24/7.")
        # LINK DE PAGO AQUI
        st.link_button("💎 COMPRAR PASE AHORA", "https://mercadopago.com.ar")
        
    else:
        # --- USUARIO LOGUEADO ---
        usuario = st.session_state.usuario_actual
        
        # SI ERES TÚ (ADMIN)
        if usuario.get('rol') == 'admin':
            st.warning("👑 **PANEL DE JEFA**")
            st.markdown("Crear acceso para nueva clienta:")
            nueva_clave = st.text_input("Nueva Clave (Ej: MARZO_2024):")
            
            if st.button("Crear Usuario"):
                if nueva_clave:
                    datos_nuevos = {
                        "usuario": nueva_clave, "nombre_el": "", "edad": 0, 
                        "historia": "No especificado", "apego": "No especificado", 
                        "resumen_sesiones": "", "fecha_alta": datetime.now().strftime("%Y-%m-%d")
                    }
                    if crear_usuario_admin(datos_nuevos):
                        st.success(f"✅ Clave '{nueva_clave}' creada con éxito.")
                    else:
                        st.error("Error al conectar con la base de datos.")
            
            if st.button("Salir de Admin"):
                 st.session_state.usuario_actual = None
                 st.rerun()
                    
        # SI ES UNA CLIENTA
        else:
            st.success(f"Hola, Soberana.")
            
            # Formulario de Perfil (Colapsable para no molestar)
            with st.expander("⚙️ Editar Perfil del Vínculo", expanded=False):
                with st.form("perfil_form"):
                    st.caption("Actualiza los datos de ÉL para mejorar la precisión de la IA.")
                    nom = st.text_input("Su Nombre:", value=usuario['nombre_el'])
                    edad = st.number_input("Su Edad:", value=int(usuario['edad']) if usuario['edad'] else 0)
                    hist = st.selectbox("Historia/Trauma:", ["No especificado", "Padres Divorciados", "Padre Ausente", "Violencia", "Narcisismo", "Adicciones"], index=0)
                    apego = st.selectbox("Su Apego:", ["No especificado", "Evitativo", "Ansioso", "Seguro"], index=0)
                    
                    if st.form_submit_button("💾 Guardar Cambios"):
                        usuario['nombre_el'] = nom
                        usuario['edad'] = edad
                        usuario['historia'] = hist
                        usuario['apego'] = apego
                        if actualizar_perfil(usuario):
                            st.session_state.usuario_actual = usuario
                            st.toast("Datos actualizados correctamente")
                            st.rerun()
            
            if st.button("Cerrar Sesión"):
                st.session_state.usuario_actual = None
                st.rerun()

# --- 7. PANTALLA PRINCIPAL ---
st.title("💎 Vínculo Nítido")

# PESTAÑAS ESTRATÉGICAS
tab1, tab2, tab3 = st.tabs(["🎁 Test Apego (Gratis)", "🕵️‍♀️ Detector (Gratis)", "🔥 SALA VIP"])

# --- TAB 1: TEST DE APEGO (GANCHO GRATUITO) ---
with tab1:
    st.header("Descubrí su Patrón de Apego 🧬")
    st.write("Responde estas 2 preguntas clave para entender con quién estás tratando:")
    
    with st.form("test_apego"):
        res1 = st.radio("1. Cuando la relación se vuelve íntima o emocional, él:", 
                        ["A. Se aleja, se enfría o pide 'espacio' (Miedo)", 
                         "B. Se vuelve intenso, celoso o demanda atención (Ansiedad)", 
                         "C. Se mantiene tranquilo y comunica lo que siente"])
        
        res2 = st.radio("2. Ante un conflicto o reclamo tuyo, él:", 
                        ["A. Huye, evita el tema o aplica la Ley del Hielo", 
                         "B. Explota, te culpa y da vuelta la situación", 
                         "C. Escucha e intenta buscar una solución"])
        
        submitted = st.form_submit_button("VER DIAGNÓSTICO GRATUITO")
        
        if submitted:
            st.divider()
            if "A." in res1 or "A." in res2:
                st.error("❄️ **Resultado: APEGO EVITATIVO**")
                st.markdown("""
                **Lo que pasa en su cerebro:** Su sistema nervioso interpreta la intimidad como una amenaza a su independencia. 
                No es que no te quiera, es que tiene **miedo**. Su estrategia de supervivencia es desconectarse.
                """)
            elif "B." in res1 or "B." in res2:
                st.warning("🔥 **Resultado: APEGO ANSIOSO**")
                st.markdown("""
                **Lo que pasa en su cerebro:** Tiene un sistema de alarma hiperactivo. 
                Cualquier distancia la interpreta como un abandono inminente. Su intensidad es un grito de conexión.
                """)
            else:
                st.success("✅ **Resultado: APEGO SEGURO**")
                st.write("Parece tener bases emocionales sanas. Si sientes inseguridad, revisa tus propios patrones.")
            
            st.info("💡 **¿Quieres saber la estrategia exacta para que te valore?** Pásate al VIP.")

# --- TAB 2: DETECTOR DE MENTIRAS (GANCHO CON CENSURA) ---
with tab2:
    st.subheader("¿Te mandó un mensaje confuso?")
    st.write("Pégalo aquí. La IA te dirá la cruda verdad (Diagnóstico Gratis), pero la estrategia es VIP.")
    
    msg_free = st.text_area("Mensaje de él:", height=100, placeholder="Ej: No eres tú, soy yo... o te deja en visto.")
    
    if st.button("🔍 ANALIZAR VERDAD"):
        if msg_free:
            with st.spinner("Analizando subtexto y psicología masculina..."):
                prompt = f"""
                Actúa como una experta en psicología masculina. Analiza este mensaje: "{msg_free}".
                1. Traduce qué significa realmente (sin filtros).
                2. Dime qué siente él (Miedo, ego, manipulación).
                NO DES CONSEJOS. Solo el diagnóstico.
                """
                res = consultar_ia(prompt)
                
                st.markdown(f"<div class='result-box'><h4>👁️ La Verdad:</h4>{res}</div>", unsafe_allow_html=True)
                
                st.markdown("#### 👑 Estrategia Soberana (Bloqueada)")
                st.markdown("""
                <div class='blur-text'>
                Para recuperar tu poder, aplica la técnica del espejo invertido.
                No respondas por 4 horas. Luego envía exactamente:
                "Entiendo que necesites espacio, avísame cuando..."
                </div>
                """, unsafe_allow_html=True)
                
                st.warning("🔒 **Para desbloquear la respuesta exacta, ingresá tu Clave VIP.**")

# --- TAB 3: ZONA VIP (EL PRODUCTO REAL) ---
with tab3:
    if st.session_state.usuario_actual is None or st.session_state.usuario_actual.get('rol') == 'admin':
        st.info("🔒 **Zona Restringida**")
        st.write("Ingresa tu clave en la barra lateral para acceder al Laboratorio de Neurociencia.")
        st.stop()
        
    u = st.session_state.usuario_actual
    nombre_sujeto = u.get('nombre_el', 'Él')
    if not nombre_sujeto: nombre_sujeto = "Tu Vínculo"
    
    st.success(f"🔓 **Laboratorio VIP Activado:** Analizando a {nombre_sujeto}")
    
    modo = st.radio("Selecciona Herramienta:", ["🔬 Análisis de Chat Profundo", "👑 Consejera Privada"], horizontal=True)
    
    if modo == "🔬 Análisis de Chat Profundo":
        st.write("Pega la conversación completa. Analizaré historial, apego y patrones.")
        chat_vip = st.text_area("Conversación:", height=200)
        
        if st.button("✨ DECODIFICAR MENTE MASCULINA"):
            if chat_vip:
                historial = u.get('resumen_sesiones', '')
                
                # EL PROMPT MAESTRO
                prompt = f"""
                Actúa como 'Wanda Soberana': Experta en Neurociencia Afectiva, Psicología Evolutiva y Mentora de Mujeres.
                Tu tono es empático, de "hermana mayor experta", seguro y cálido.
                
                PERFIL DE ÉL:
                - Nombre: {nombre_sujeto}
                - Edad: {u['edad']}
                - Apego: {u['apego']}
                - Historia/Trauma: {u['historia']}
                - Contexto Previo: {historial}
                
                CHAT A ANALIZAR: "{chat_vip}"
                
                Analiza esto para ELLA (la usuaria) siguiendo estos 4 pasos:
                
                1. 🧬 **LO QUE PASA EN SU CEREBRO (Ciencia):** Explica qué químicos o miedos se activaron en él. ¿Busca dopamina barata? ¿Se activó su amígdala por miedo?
                
                2. 💔 **VALIDACIÓN EMOCIONAL (Empatía):**
                   Valida lo que ella debe estar sintiendo ante esto. Hazla sentir comprendida.
                
                3. 👁️ **TRADUCCIÓN NÍTIDA:**
                   "Lo que dice" vs "Lo que realmente significa". Sé cruda pero amable.
                
                4. 👑 **ESTRATEGIA SOBERANA (Acción):**
                   Dile exactamente qué hacer o qué responder para recuperar su dignidad y valor.
                
                AL FINAL, en una línea nueva escribe: "MEMORIA_DB: [Resumen de 1 frase de lo ocurrido hoy]"
                """
                
                with st.spinner("Consultando bases de datos de psicología evolutiva..."):
                    res = consultar_ia(prompt)
                    
                    if "MEMORIA_DB:" in res:
                        partes = res.split("MEMORIA_DB:")
                        st.markdown(partes[0])
                        guardar_memoria(u, f"{datetime.now().strftime('%d/%m')}: {partes[1].strip()}")
                        st.toast("🧠 Memoria del vínculo guardada.")
                    else:
                        st.markdown(res)
                
    elif modo == "👑 Consejera Privada":
        st.write("¿Cómo te sientes hoy? ¿Necesitas un consejo rápido o ánimo?")
        consulta = st.text_area("Cuéntame:")
        
        if st.button("PEDIR APOYO"):
            if consulta:
                prompt = f"""
                Eres una Mentora Empática y Experta en Relaciones.
                La usuaria está lidiando con {nombre_sujeto} ({u['apego']}, {u['historia']}).
                Ella dice: "{consulta}".
                
                Dale un consejo corto, amoroso pero firme. Recuérdale su valor.
                """
                st.markdown(f"<div class='result-box'>{consultar_ia(prompt)}</div>", unsafe_allow_html=True)
