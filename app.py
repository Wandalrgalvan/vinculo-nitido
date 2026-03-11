import streamlit as st
import requests
from datetime import datetime
import json

# --- CONFIG VISUAL Y PSICOLOGÍA DEL COLOR ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Roboto:wght@400;500&display=swap');
    .stApp { background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; font-family: 'Roboto', sans-serif; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Montserrat', sans-serif; color: #5EEAD4 !important; font-weight: 600; }
    .stRadio label p { color: #FFFFFF !important; font-size: 1.05em !important; font-family: 'Roboto', sans-serif !important; }
    .muted { color: #E2E8F0; font-size: 0.95em; }
    .stButton>button {
        background: linear-gradient(90deg, #14B8A6 0%, #0D9488 100%);
        color: #FFFFFF; font-weight: bold; border-radius: 8px; border: none; width: 100%; padding: 12px; transition: all 0.3s ease;
    }
    .stButton>button:hover { filter: brightness(1.1); }
    
    /* FIX DEFINITIVO: Cajas de texto y Selectores adaptados para celular */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important; color: white !important; border: 1px solid #334155; border-radius: 6px;
    }
    
    /* Arregla el texto seleccionado DENTRO de la cajita principal */
    div[data-baseweb="select"] > div, div[data-baseweb="select"] span {
        white-space: normal !important;
        word-wrap: break-word !important;
        text-overflow: clip !important;
    }
    
    /* Arregla el texto en la LISTA DESPLEGABLE (la capa flotante) */
    div[data-baseweb="popover"] li {
        white-space: normal !important;
        word-wrap: break-word !important;
        height: auto !important;
        min-height: 40px !important;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }
    
    .result-box { background: rgba(15, 23, 42, 0.6); padding: 25px; border-left: 4px solid #5EEAD4; border-radius: 8px; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .chat-user { background: rgba(20, 184, 166, 0.1); padding: 15px; border-radius: 8px 8px 0px 8px; margin-bottom: 10px; border-right: 3px solid #14B8A6; text-align: right; }
    .chat-bot { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px 8px 8px 0px; margin-bottom: 10px; border-left: 3px solid #D4AF37; }
    .blur-text { filter: blur(5px); opacity: 0.6; pointer-events: none; }
    .vip-title { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VIP KEYS ---
VIP_KEYS = [
    "a1b2c3d4-e5f6-4789-a012-3456789abcde", "98765432-10fe-dcba-9876-543210fedcba",
    "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d", "f1e2d3c4-b5a6-7890-1234-56789abcdef0",
    "11223344-5566-7788-9900-aabbccddeeff", "5f4e3d2c-1b0a-9f8e-7d6c-5b4a3e2d1c0b",
    "7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d", "cdef1234-5678-90ab-cdef-1234567890ab",
    "4d3c2b1a-0f9e-8d7c-6b5a-4e3d2c1b0a9f", "aa11bb22-cc33-dd44-ee55-ff6600778899",
    "00112233-4455-6677-8899-aabbccddeeff", "f0e1d2c3-b4a5-6789-0123-456789abcdef",
    "12345678-9abc-def0-1234-56789abcdef0", "fedcba98-7654-3210-fedc-ba9876543210",
    "a0b1c2d3-e4f5-6789-a0b1-c2d3e4f56789", "9f8e7d6c-5b4a-3e21-0f1e-2d3c4b5a6789",
    "1a2b3c4d-1a2b-3c4d-1a2b-3c4d1a2b3c4d", "5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b",
    "d4c3b2a1-0f9e-8d7c-6b5a-4e3d2c1b0a9f", "11223344-1122-3344-1122-334411223344",
    "aabbccdd-eeff-0011-2233-445566778899", "09876543-21fedcba-0987-654321fedcba",
    "123abc45-6def-7890-123a-bc456def7890", "456def78-9012-3abc-456d-ef7890123abc",
    "7890123a-bc45-6def-7890-123abc456def", "def01234-5678-9abc-def0-123456789abc",
    "abc456de-f789-0123-abc4-56def7890123", "01234567-89ab-cdef-0123-456789abcdef",
    "89abcdef-0123-4567-89ab-cdef01234567", "cdef0123-4567-89ab-cdef-0123456789ab",
    "ef012345-6789-abcd-ef01-23456789abcd", "23456789-abcd-ef01-2345-6789abcdef01",
    "6789abcd-ef01-2345-6789-abcdef012345", "abcdef01-2345-6789-abcd-ef0123456789",
    "3456789a-bcde-f012-3456-789abcdef012", "789abcdef-0123-4567-89ab-cdef01234567",
    "bcdef012-3456-789a-bcde-f0123456789a", "f0123456-789a-bcde-f012-3456789abcde",
    "01234567-89ab-cdef-0123-456789abcdef", "456789ab-cdef-0123-4567-89abcdef0123",
    "89abcdef-0123-4567-89ab-cdef01234567", "cdef0123-4567-89ab-cdef-0123456789ab",
    "01234567-89ab-cdef-0123-456789abcdef", "456789ab-cdef-0123-4567-89abcdef0123",
    "89abcdef-0123-4567-89ab-cdef01234567", "cdef0123-4567-89ab-cdef-0123456789ab",
    "ef012345-6789-abcd-ef01-23456789abcd", "23456789-abcd-ef01-2345-6789abcdef01",
    "6789abcd-ef01-2345-6789-abcdef012345", "abcdef01-2345-6789-abcd-ef0123456789"
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
    st.session_state.perfil_el = {"nombre": "", "edad": 30, "tipo_relacion": "No sé", "apego": "No sé", "historia": "No sé", "tiempo_relacion": ""}
if 'consent' not in st.session_state:
    st.session_state.consent = False
if 'mensajes_consultorio' not in st.session_state:
    st.session_state.mensajes_consultorio = []

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 60px;'>👑</div>", unsafe_allow_html=True)
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
        
        st.write("---")
        st.markdown("<h4 style='text-align: center; color: #5EEAD4;'>💎 Adquirir Pase VIP</h4>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("<h4 style='text-align: center; color: #5EEAD4; margin-bottom: 5px;'>🔓 Decodifica su mente</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.85em; color: #94A3B8; margin-bottom: 20px;'>Accede al Laboratorio VIP y al Consultorio Soberano para traducir sus verdaderas intenciones.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <a href="TU_LINK_DE_GUMROAD_AQUI" target="_blank" style="text-decoration: none; display: block; width: 100%; box-sizing: border-box;">
            <div style="background-color: #0F172A; border: 1px solid #14B8A6; color: white; padding: 12px; border-radius: 6px; text-align: center; transition: 0.3s; margin-bottom: 10px; word-wrap: break-word;">
                <span style="font-weight: bold; font-size: 1.05em; color: #5EEAD4;">Obtener Pase VIP</span><br>
                <span style="font-size: 0.75em; color: #94A3B8;">🌍 Pago con Tarjeta (Entrega Inmediata)</span>
            </div>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <a href="TU_LINK_DE_MERCADO_PAGO_AQUI" target="_blank" style="text-decoration: none; display: block; width: 100%; box-sizing: border-box;">
            <div style="background-color: transparent; border: 1px dashed #475569; color: #CBD5E1; padding: 10px; border-radius: 6px; text-align: center; transition: 0.3s; word-wrap: break-word;">
                <span style="font-weight: bold; font-size: 0.9em;">🇦🇷 Opción Argentina</span><br>
                <span style="font-size: 0.75em;">Pagar en Pesos (Mercado Pago)</span>
            </div>
        </a>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; font-size: 0.75em; color: #64748B; margin-top: 10px;'>Si usas Mercado Pago, envíame el comprobante por Instagram para habilitar tu clave.</p>", unsafe_allow_html=True)
    else:
        st.success("👩🏻‍💼 Bienvenida, Soberana.")
        with st.expander("👩🏻‍💼 Perfil del Vínculo", expanded=True):
            with st.form("perfil"):
                p_nombre = st.text_input("Nombre:", value=st.session_state.perfil_el.get("nombre", ""))
                p_edad = st.number_input("Edad:", value=st.session_state.perfil_el.get("edad", 30), min_value=15, max_value=90)
                
                lista_tipos = ["No sé", "Casados", "Novios", "Amantes", "Casi algo", "Ex pareja", "Contacto Cero"]
                tipo_actual = st.session_state.perfil_el.get("tipo_relacion", "No sé")
                idx_tipo = lista_tipos.index(tipo_actual) if tipo_actual in lista_tipos else 0
                p_tipo = st.selectbox("Tipo de Vínculo:", lista_tipos, index=idx_tipo)
                
                lista_apegos = ["No sé", "Evitativo", "Ansioso", "Seguro"]
                apego_actual = st.session_state.perfil_el.get("apego", "No sé")
                idx_apego = lista_apegos.index(apego_actual) if apego_actual in lista_apegos else 0
                p_apego = st.selectbox("Apego:", lista_apegos, index=idx_apego)
                
                lista_hist = ["No sé", "Padres Divorciados", "Padre Ausente", "Violencia", "Narcisismo"]
                hist_actual = st.session_state.perfil_el.get("historia", "No sé")
                idx_hist = lista_hist.index(hist_actual) if hist_actual in lista_hist else 0
                p_hist = st.selectbox("Historia de Crianza:", lista_hist, index=idx_hist)
                
                p_tiempo = st.text_input("Tiempo de relación:", value=st.session_state.perfil_el.get("tiempo_relacion",""))
                
                if st.form_submit_button("💾 Guardar Parámetros"):
                    st.session_state.perfil_el = {
                        "nombre": p_nombre, "edad": p_edad, "tipo_relacion": p_tipo, "apego": p_apego, "historia": p_hist, "tiempo_relacion": p_tiempo
                    }
                    st.rerun() 
        
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()

# --- PANTALLA PRINCIPAL ---
st.title("Vínculo Nítido")
st.markdown("<h3 style='color: #F8FAFC !important; font-size: 1.2em; margin-top: -15px;'>🧠 Decodifica la mente de tu pareja (o casi algo)</h3>", unsafe_allow_html=True)
st.markdown("<p class='muted'>Traducción de comportamiento en el amor, apoyada en neurociencia.</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🧬 Test Apego", "👁️ Verdad Oculta", "🔥 Laboratorio VIP", "🛋️ Consultorio Soberano"])

# --- TAB 1: TEST GRATIS ---
with tab1:
    st.header("Descubre su Patrón Cerebral")
    st.markdown("<p class='muted'>Responde estas 3 preguntas para identificar su estilo de apego.</p>", unsafe_allow_html=True)

    r1 = st.radio("1. Ante la intimidad y la cercanía emocional, él:", 
        ["Se siente cómodo y confía", 
         "Necesita cercanía constante y teme que lo dejes", 
         "Se agobia, pone barreras o se aleja", 
         "Es caótico: te busca intensamente y luego huye"])
    
    r2 = st.radio("2. Durante un conflicto o discusión, él suele:", 
        ["Dialogar para buscar una solución juntos", 
         "Reclamar, explotar o culpar por miedo a perderte", 
         "Castigar con el hielo (silencio) o minimizar el problema", 
         "Tener reacciones impredecibles y explosivas"])
         
    r3 = st.radio("3. Respecto a la independencia y el espacio personal:", 
        ["Respeta tu espacio y disfruta el suyo sin inseguridad", 
         "Entra en pánico o sobrepiensa si tardas en responder", 
         "Exige extrema autosuficiencia y resiente tus demandas", 
         "Desconfía profundamente de ti, pero le aterra estar solo"])

    if st.button("VER DIAGNÓSTICO"):
        st.divider()
        evitativo_opts = [
            "Se agobia, pone barreras o se aleja",
            "Castigar con el hielo (silencio) o minimizar el problema",
            "Exige extrema autosuficiencia y resiente tus demandas"
        ]
        ansioso_opts = [
            "Necesita cercanía constante y teme que lo dejes",
            "Reclamar, explotar o culpar por miedo a perderte",
            "Entra en pánico o sobrepiensa si tardas en responder"
        ]
        desorganizado_opts = [
            "Es caótico: te busca intensamente y luego huye",
            "Tener reacciones impredecibles y explosivas",
            "Desconfía profundamente de ti, pero le aterra estar solo"
        ]
        seguro_opts = [
            "Se siente cómodo y confía",
            "Dialogar para buscar una solución juntos",
            "Respeta tu espacio y disfruta el suyo sin inseguridad"
        ]

        respuestas = [r1, r2, r3]
        evitativo = sum([1 for r in respuestas if r in evitativo_opts])
        ansioso = sum([1 for r in respuestas if r in ansioso_opts])
        desorganizado = sum([1 for r in respuestas if r in desorganizado_opts])
        seguro = sum([1 for r in respuestas if r in seguro_opts])
        
        scores = {"Evitativo": evitativo, "Ansioso-Ambivalente": ansioso, "Desorganizado": desorganizado, "Seguro": seguro}
        max_apego = max(scores, key=scores.get)
        
        if max_apego == "Evitativo":
            st.error("❄️ **APEGO EVITATIVO**")
            st.write("Rechaza la intimidad emocional y muestra una autosuficiencia extrema. Su cerebro asocia la cercanía con pérdida de libertad. El contacto profundo activa sus respuestas de huida o distanciamiento.")
        elif max_apego == "Ansioso-Ambivalente":
            st.warning("🔥 **APEGO ANSIOSO-AMBIVALENTE**")
            st.write("Siente una fuerte necesidad de cercanía y preocupación constante por el rechazo. Su intensidad y conductas demandantes nacen del miedo al abandono y una hiperactividad en la amígdala cerebral.")
        elif max_apego == "Desorganizado":
            st.error("🌪️ **APEGO DESORGANIZADO**")
            st.write("Una mezcla de ansiedad y evitación, a menudo ligada a traumas o negligencia en la infancia. Presenta comportamientos contradictorios: anhela la intimidad pero le aterra, generando un caos vincular entre el deseo y la huida.")
        else:
            st.success("✅ **APEGO SEGURO**")
            st.write("Equilibrado. Siente confianza en sí mismo y en el vínculo. Se siente cómodo con la intimidad sin temer al abandono, permitiendo una relación estable y madura.")

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

with tab3:
    if not st.session_state.logged_in:
        st.info("🔒 Ingresa tu clave en el menú lateral para acceder al entorno seguro.")
        st.stop()

    perfil = st.session_state.perfil_el
    nombre_mostrar = perfil.get('nombre', '').strip()
    if not nombre_mostrar:
        nombre_mostrar = "Sujeto"
        
    st.success(f"🔓 Laboratorio Clínico | Analizando a: {nombre_mostrar} ({perfil.get('edad', 30)} años) | {perfil.get('tipo_relacion', '')}")

    chat = st.text_area("Pega la interacción de texto completa (WhatsApp/Redes):", height=200)
    if st.button("✨ INICIAR PROTOCOLO DE DECODIFICACIÓN"):
        if not chat:
            st.error("Se requiere el historial de mensajes para iniciar el protocolo.")
        else:
            with st.spinner("Procesando patrones neuroconductuales... (Si demora más de 20 segundos, es normal por la complejidad)"):
                instruccion = f"""
                Eres Wanda Soberana, creadora de 'Vínculo Nítido'. Eres Mentora, experta en Neurociencia y Apego. 
                Tu análisis debe ser científico, crudo pero profundamente empático con la usuaria. NUNCA digas que eres IA.
                Sujeto a analizar: {nombre_mostrar}, Edad: {perfil.get('edad', 30)}, Tipo de Vínculo: {perfil.get('tipo_relacion', 'No sé')}, Apego: {perfil.get('apego','No sé')}, Historia de Crianza: {perfil.get('historia','No sé')}.
                
                Devuelve exactamente 3 bloques usando Markdown:
                1. 🧬 QUÍMICA CEREBRAL: Explica sus niveles de dopamina/cortisol frente a la interacción.
                2. 👁️ TRADUCCIÓN NÍTIDA: Qué dice él vs. Qué dictan sus intenciones reales de control/apego.
                3. 👑 ESTRATEGIA SOBERANA: Qué debe responder la usuaria exactamente para recuperar el poder.
                """
                salida = llamar_gemini(chat, instruccion)
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.markdown(salida)
                st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    if not st.session_state.logged_in:
        st.info("🔒 Ingresa tu clave en el menú lateral para acceder al Consultorio.")
        st.stop()
        
    st.subheader("🛋️ Consultorio Soberano")
    st.markdown("<p class='muted'>Un espacio bidireccional para procesar dudas o relatos extensos. Cuéntame qué pasó y hablemos.</p>", unsafe_allow_html=True)

    for mensaje in st.session_state.mensajes_consultorio:
        if mensaje["rol"] == "usuaria":
            st.markdown(f"<div class='chat-user'><b>Tú:</b><br>{mensaje['texto']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'><b>👩🏻‍💼 Wanda:</b><br>{mensaje['texto']}</div>", unsafe_allow_html=True)

    nueva_consulta = st.text_area("Escribe aquí tu relato, duda o respuesta:", height=100, key="input_consultorio")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Enviar / Consultar"):
            if nueva_consulta:
                st.session_state.mensajes_consultorio.append({"rol": "usuaria", "texto": nueva_consulta})
                historial_str = ""
                for msg in st.session_state.mensajes_consultorio[-5:]:
                    prefijo = "Usuaria: " if msg["rol"] == "usuaria" else "Wanda: "
                    historial_str += f"{prefijo}{msg['texto']}\n"

                with st.spinner("Procesando tu relato..."):
                    nombre_consultorio = st.session_state.perfil_el.get('nombre', '').strip() or "el sujeto"
                    instruccion_consultorio = f"""
                    Eres Wanda Soberana. Estás en una sesión de mentoría 1 a 1 (Consultorio Soberano).
                    La usuaria te está contando situaciones de su vida, su relación con {nombre_consultorio} (Tipo de Vínculo: {st.session_state.perfil_el.get('tipo_relacion', 'No sé')}, Apego: {st.session_state.perfil_el.get('apego', 'No sé')}) o dudas sobre su valor y proyectos.
                    Tono: Eres una mentora cruda, validas profundamente sus emociones, le das claridad clínica sobre lo que está viviendo y la empoderas. Dialogas de tú a tú, no como un reporte.
                    
                    HISTORIAL DE LA CHARLA RECIENTE:
                    {historial_str}
                    
                    Responde al último mensaje de la usuaria continuando la conversación de forma natural y terapéutica.
                    """
                    respuesta_wanda = llamar_gemini(nueva_consulta, instruccion_consultorio)
                    st.session_state.mensajes_consultorio.append({"rol": "wanda", "texto": respuesta_wanda})
                    st.rerun()
    with col2:
        if st.button("🧹 Limpiar Charla"):
            st.session_state.mensajes_consultorio = []
            st.rerun()

st.markdown("---")
st.markdown("<div class='muted'>Vínculo Nítido © 2026 | Metodología Soberana</div>", unsafe_allow_html=True)
