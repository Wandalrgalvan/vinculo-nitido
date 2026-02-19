import streamlit as st
import requests
from datetime import datetime
import json

# --- CONFIG VISUAL Y PSICOLOGÍA DEL COLOR ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    /* Paleta Océano Clínico: Reduce ansiedad, transmite autoridad y contención */
    .stApp { background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; }
    h1, h2, h3 { color: #5EEAD4 !important; font-weight: 300; }
    
    /* Botones Teal: Llamado a la acción claro y calmante */
    .stButton>button {
        background: linear-gradient(90deg, #14B8A6 0%, #0D9488 100%);
        color: #FFFFFF; font-weight: bold; border-radius: 8px; border: none; width: 100%; padding: 12px; transition: all 0.3s ease;
    }
    .stButton>button:hover { filter: brightness(1.1); }
    
    /* Inputs minimalistas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important; color: white !important; border: 1px solid #334155; border-radius: 6px;
    }
    
    /* Cajas de resultado y Chat */
    .result-box { background: rgba(15, 23, 42, 0.6); padding: 25px; border-left: 4px solid #5EEAD4; border-radius: 8px; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .chat-user { background: rgba(20, 184, 166, 0.1); padding: 15px; border-radius: 8px 8px 0px 8px; margin-bottom: 10px; border-right: 3px solid #14B8A6; text-align: right; }
    .chat-bot { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px 8px 8px 0px; margin-bottom: 10px; border-left: 3px solid #D4AF37; }
    .blur-text { filter: blur(5px); opacity: 0.6; pointer-events: none; }
    .muted { color: #94A3B8; font-size: 0.85em; }
    .vip-title { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VIP KEYS (50 Claves generadas para Venta) ---
VIP_KEYS = [
    "a1b2c3d4-e5f6-4789-a012-3456789abcde",
    "98765432-10fe-dcba-9876-543210fedcba",
    "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    "f1e2d3c4-b5a6-7890-1234-56789abcdef0",
    "11223344-5566-7788-9900-aabbccddeeff",
    "5f4e3d2c-1b0a-9f8e-7d6c-5b4a3e2d1c0b",
    "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d",
    "cdef1234-5678-90ab-cdef-1234567890ab",
    "4d3c2b1a-0f9e-8d7c-6b5a-4e3d2c1b0a9f",
    "aa11bb22-cc33-dd44-ee55-ff6600778899",
    "00112233-4455-6677-8899-aabbccddeeff",
    "f0e1d2c3-b4a5-6789-0123-456789abcdef",
    "12345678-9abc-def0-1234-56789abcdef0",
    "fedcba98-7654-3210-fedc-ba9876543210",
    "a0b1c2d3-e4f5-6789-a0b1-c2d3e4f56789",
    "9f8e7d6c-5b4a-3e21-0f1e-2d3c4b5a6789",
    "1a2b3c4d-1a2b-3c4d-1a2b-3c4d1a2b3c4d",
    "5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b",
    "d4c3b2a1-0f9e-8d7c-6b5a-4e3d2c1b0a9f",
    "11223344-1122-3344-1122-334411223344",
    "aabbccdd-eeff-0011-2233-445566778899",
    "09876543-21fedcba-0987-654321fedcba",
    "123abc45-6def-7890-123a-bc456def7890",
    "456def78-9012-3abc-456d-ef7890123abc",
    "7890123a-bc45-6def-7890-123abc456def",
    "def01234-5678-9abc-def0-123456789abc",
    "abc456de-f789-0123-abc4-56def7890123",
    "01234567-89ab-cdef-0123-456789abcdef",
    "89abcdef-0123-4567-89ab-cdef01234567",
    "cdef0123-4567-89ab-cdef-0123456789ab",
    "ef012345-6789-abcd-ef01-23456789abcd",
    "23456789-abcd-ef01-2345-6789abcdef01",
    "6789abcd-ef01-2345-6789-abcdef012345",
    "abcdef01-2345-6789-abcd-ef0123456789",
    "3456789a-bcde-f012-3456-789abcdef012",
    "789abcdef-0123-4567-89ab-cdef01234567",
    "bcdef012-3456-789a-bcde-f0123456789a",
    "f0123456-789a-bcde-f012-3456789abcde",
    "01234567-89ab-cdef-0123-456789abcdef",
    "456789ab-cdef-0123-4567-89abcdef0123",
    "89abcdef-0123-4567-89ab-cdef01234567",
    "cdef0123-4567-89ab-cdef-0123456789ab",
    "01234567-89ab-cdef-0123-456789abcdef",
    "456789ab-cdef-0123-4567-89abcdef0123",
    "89abcdef-0123-4567-89ab-cdef01234567",
    "cdef0123-4567-89ab-cdef-0123456789ab",
    "ef012345-6789-abcd-ef01-23456789abcd",
    "23456789-abcd-ef01-2345-6789abcdef01",
    "6789abcd-ef01-2345-6789-abcdef012345",
    "abcdef01-2345-6789-abcd-ef0123456789"
]

# --- GEMINI API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

def llamar_gemini(prompt, system_instruction):
    if not api_key:
        return "⚠️ ERROR CRÍTICO: Falta la API Key en los 'Secrets'."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    data = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nENTRADA DE LA USUARIA:\n{prompt}"}]}],
        "safetySettings": safety_settings
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            try:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                return "⚠️ Error al parsear la respuesta."
        else:
            return f"⚠️ Error ({response.status_code}) de la API."
    except Exception as e:
        return f"⚠️ Error de Conexión o Tiempo de espera agotado: {str(e)}"

# --- INICIO DE SESIÓN Y MEMORIA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'perfil_el' not in st.session_state:
    st.session_state.perfil_el = {"nombre": "", "edad": 30, "apego": "No sé", "historia": "No sé", "tiempo_relacion": ""}
if 'consent' not in st.session_state:
    st.session_state.consent = False
if 'mensajes_consultorio' not in st.session_state:
    st.session_state.mensajes_consultorio = [] # Memoria para el chat interactivo

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 60px;'>🌊</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Vínculo Nítido</h3>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.info("🔐 Acceso VIP")
        clave = st.text_input("Ingresa tu Clave VIP:", type="password")
        if st.button("INGRESAR"):
            if clave and clave.strip() in VIP_KEYS:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Clave inválida. Verifica tu correo o adquiere un pase.")
    else:
        st.success("✨ Bienvenida, Soberana.")
        with st.expander("⚙️ Perfil del Vínculo", expanded=True):
            with st.form("perfil"):
                p_nombre = st.text_input("Nombre:", value=st.session_state.perfil_el["nombre"])
                p_edad = st.number_input("Edad:", value=st.session_state.perfil_el["edad"], min_value=15, max_value=90)
                p_apego = st.selectbox("Apego:", ["No sé", "Evitativo", "Ansioso", "Seguro"], index=0)
                p_hist = st.selectbox("Historia:", ["No sé", "Padres Divorciados", "Padre Ausente", "Violencia", "Narcisismo"], index=0)
                p_tiempo = st.text_input("Tiempo de relación:", value=st.session_state.perfil_el.get("tiempo_relacion",""))
                
                if st.form_submit_button("💾 Guardar Parámetros"):
                    st.session_state.perfil_el = {
                        "nombre": p_nombre, "edad": p_edad, "apego": p_apego, "historia": p_hist, "tiempo_relacion": p_tiempo
                    }
                    st.toast("Parámetros clínicos actualizados")
        
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()

# --- PANTALLA PRINCIPAL ---
st.title("Vínculo Nítido")
st.markdown("<p class='muted'>Traducción de comportamiento apoyada en neurociencia.</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🧬 Test Apego", "👁️ Verdad Oculta", "🔥 Laboratorio VIP", "🛋️ Consultorio Soberano"])

# --- TAB 1: TEST GRATIS ---
with tab1:
    st.header("Descubre su Patrón Cerebral")
    r1 = st.radio("Ante la intimidad, él:", ["Se aleja (Miedo / Sobrecarga)", "Se pone intenso (Ansiedad)", "Estable"])
    r2 = st.radio("Ante conflictos, él:", ["Huye / Silencio", "Explota / Culpa", "Dialoga"])
    if st.button("VER DIAGNÓSTICO"):
        st.divider()
        if "aleja" in r1 or "Huye" in r2:
            st.error("❄️ **APEGO EVITATIVO**")
            st.write("Su cerebro asocia la cercanía emocional con pérdida de libertad. El contacto activa respuestas de huida.")
        elif "intenso" in r1 or "Explota" in r2:
            st.warning("🔥 **APEGO ANSIOSO**")
            st.write("Su intensidad nace del miedo al abandono. Hiperactividad en la amígdala cerebral.")
        else:
            st.success("✅ **APEGO SEGURO**")

# --- TAB 2: GANCHO GRATIS ---
with tab2:
    st.subheader("¿Mensaje confuso?")
    consent = st.checkbox("Acepto que este análisis es informativo, basado en patrones de comportamiento, y no sustituye terapia.")
    st.session_state.consent = consent
    
    msg = st.text_area("Pega su mensaje aquí:", height=120, disabled=not consent)
    if st.button("TRADUCIR (GRATIS)"):
        if not consent:
            st.error("Requisito clínico: Debes aceptar el consentimiento.")
        elif not msg:
            st.error("Falta información. Pega un mensaje para analizar.")
        else:
            instruccion = "Eres Wanda Soberana. Analiza este mensaje brevemente desde la neurociencia. Sé cruda. NO DES CONSEJOS."
            res = llamar_gemini(msg, instruccion)
            st.markdown(f"<div class='result-box'><h4>👁️ La Verdad Cruda:</h4>{res}</div>", unsafe_allow_html=True)
            st.markdown("#### <span class='vip-title'>👑 Estrategia Soberana (Bloqueada)</span>", unsafe_allow_html=True)
            st.markdown("<div class='blur-text'>Para recuperar el control hormonal de la interacción, aplica un silencio táctico de 4 horas y luego responde...</div>", unsafe_allow_html=True)
            st.info("🔒 Desbloquea la estrategia exacta y la química de su cerebro en el VIP.")

# --- TAB 3: VIP (LABORATORIO) ---
with tab3:
    if not st.session_state.logged_in:
        st.info("🔒 Ingresa tu clave en el menú lateral para acceder al entorno seguro.")
        st.stop()

    perfil = st.session_state.perfil_el
    st.success(f"🔓 Laboratorio Clínico | Analizando a: {perfil.get('nombre','Sujeto')} ({perfil.get('edad','?')} años)")

    chat = st.text_area("Pega la interacción de texto completa (WhatsApp/Redes):", height=200)
    if st.button("✨ INICIAR PROTOCOLO DE DECODIFICACIÓN"):
        if not chat:
            st.error("Se requiere el historial de mensajes para iniciar el protocolo.")
        else:
            with st.spinner("Procesando patrones neuroconductuales... (Si demora más de 20 segundos, es normal por la complejidad clínica del chat)"):
                instruccion = f"""
                Eres Wanda Soberana, creadora de 'Vínculo Nítido'. Eres Mentora, experta en Neurociencia y Apego. 
                Tu análisis debe ser científico, crudo pero profundamente empático con la usuaria. NUNCA digas que eres IA.
                Sujeto a analizar: {perfil.get('nombre','[sin nombre]')}, Edad: {perfil.get('edad', 30)}, Apego: {perfil.get('apego','No sé')}, Historia: {perfil.get('historia','No sé')}.
                
                Devuelve exactamente 3 bloques usando Markdown:
                1. 🧬 QUÍMICA CEREBRAL: Explica sus niveles de dopamina/cortisol frente a la interacción.
                2. 👁️ TRADUCCIÓN NÍTIDA: Qué dice él vs. Qué dictan sus intenciones reales de control/apego.
                3. 👑 ESTRATEGIA SOBERANA: Qué debe responder la usuaria exactamente para recuperar el poder.
                """
                salida = llamar_gemini(chat, instruccion)
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.markdown(salida)
                st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 4: CONSULTORIO SOBERANO (CHAT INTERACTIVO) ---
with tab4:
    if not st.session_state.logged_in:
        st.info("🔒 Ingresa tu clave en el menú lateral para acceder al Consultorio.")
        st.stop()
        
    st.subheader("🛋️ Consultorio Soberano")
    st.markdown("<p class='muted'>Un espacio bidireccional para procesar dudas, relatos extensos o dinámicas en persona. Cuéntame qué pasó y hablemos.</p>", unsafe_allow_html=True)

    # Mostrar historial del chat
    for mensaje in st.session_state.mensajes_consultorio:
        if mensaje["rol"] == "usuaria":
            st.markdown(f"<div class='chat-user'><b>Tú:</b><br>{mensaje['texto']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'><b>👑 Wanda:</b><br>{mensaje['texto']}</div>", unsafe_allow_html=True)

    # Input para conversar
    nueva_consulta = st.text_area("Escribe aquí tu relato, duda o respuesta:", height=100, key="input_consultorio")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Enviar / Consultar"):
            if nueva_consulta:
                # Guardar mensaje de la usuaria
                st.session_state.mensajes_consultorio.append({"rol": "usuaria", "texto": nueva_consulta})
                
                # Construir el contexto (memoria) para la IA
                historial_str = ""
                for msg in st.session_state.mensajes_consultorio[-5:]: # Recuerda los últimos 5 mensajes
                    prefijo = "Usuaria: " if msg["rol"] == "usuaria" else "Wanda: "
                    historial_str += f"{prefijo}{msg['texto']}\n"

                with st.spinner("Procesando tu relato... (Puede demorar unos segundos)"):
                    instruccion_consultorio = f"""
                    Eres Wanda Soberana. Estás en una sesión de mentoría 1 a 1 (Consultorio Soberano).
                    La usuaria te está contando situaciones de su vida, su relación con {st.session_state.perfil_el['nombre']} (Apego: {st.session_state.perfil_el['apego']}) o dudas sobre su valor y proyectos.
                    Tono: Eres una mentora cruda, validas profundamente sus emociones, le das claridad clínica sobre lo que está viviendo y la empoderas. Dialogas de tú a tú, no como un reporte.
                    Si ella te cuenta sobre su proyecto o negocio, aliéntala a confiar en su visión por encima de las opiniones de hombres evitativos.
                    
                    HISTORIAL DE LA CHARLA RECIENTE:
                    {historial_str}
                    
                    Responde al último mensaje de la usuaria continuando la conversación de forma natural y terapéutica.
                    """
                    
                    respuesta_wanda = llamar_gemini(nueva_consulta, instruccion_consultorio)
                    st.session_state.mensajes_consultorio.append({"rol": "wanda", "texto": respuesta_wanda})
                    st.rerun() # Recarga la pantalla para mostrar el nuevo mensaje
    with col2:
        if st.button("🧹 Limpiar Charla"):
            st.session_state.mensajes_consultorio = []
            st.rerun()

st.markdown("---")
st.markdown("<div class='muted'>Vínculo Nítido © 2026 | Metodología Soberana</div>", unsafe_allow_html=True)
