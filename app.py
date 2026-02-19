import streamlit as st
import requests
from datetime import datetime
import uuid
import json

# --- CONFIG VISUAL ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #120318 0%, #2D0545 100%); color: #fff; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #F2994A 100%);
        color: #120318; font-weight: bold; border-radius: 12px; border: none; width: 100%; padding: 12px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.08) !important; color: white !important; border: 1px solid #D4AF37;
    }
    .result-box { background: rgba(0,0,0,0.35); padding: 20px; border-left: 4px solid #D4AF37; border-radius: 10px; margin-top: 15px; }
    .blur-text { filter: blur(5px); opacity: 0.6; pointer-events: none; }
    .muted { color: #ddd; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- VIP KEYS (20 ejemplos) ---
VIP_KEYS = [
    # Reemplaza/añade aquí claves reales que generes (UUIDs)
    "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "9b2f5a21-3cbb-4b7f-8a1f-3c5f2d9b4f11",
    "a4e1f5d2-1b2c-4c3d-8f9a-0b1c2d3e4f55",
    "8f7e6d5c-4b3a-2910-9f8e-7d6c5b4a3e22",
    "c3b2a190-8f7e-6d5c-4b3a-29108f7e6d11",
    "f1e2d3c4-b5a6-7890-1234-56789abcdef0",
    "11111111-2222-3333-4444-555555555555",
    "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "123e4567-e89b-12d3-a456-426614174000",
    "9f8e7d6c-5b4a-3e22-c3b2-a1908f7e6d55",
    "0f1e2d3c-4b5a-6c7d-8e9f-0a1b2c3d4e66",
    "abcdefab-cdef-abcd-efab-cdefabcdef12",
    "abcd1234-ef56-7890-abcd-ef1234567890",
    "feedface-0000-1111-2222-333344445555",
    "beefbeef-1234-5678-9abc-def012345678",
    "77777777-8888-9999-aaaa-bbbbbbbbbbbb",
    "deadbeef-dead-beef-dead-beefdeadbeef",
    "cafebab0-cafe-babe-cafe-bab0cafebabe",
    "facefeed-face-feed-face-feedfacefeed",
    "01234567-89ab-cdef-0123-456789abcdef"
]

# --- GEMINI API KEY ---
api_key = st.secrets.get("GEMINI_API_KEY", "")

def consultar_soberana(prompt, edad_sujeto):
    if not api_key:
        return "⚠️ ERROR CRÍTICO: Falta la API Key en los 'Secrets'. Agrega GEMINI_API_KEY en Streamlit Secrets."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    system_instruction = f"""
    Eres Wanda Soberana, creadora de la Metodología 'Vínculo Nítido'.
    Eres experta en: Psicología de la Atracción, Psicología Masculina, Neurociencia y Apego.
    TU OBJETIVO: Analizar vínculos. NUNCA menciones que eres una IA.
    EDAD DEL SUJETO: {edad_sujeto} años (Ajusta el análisis a su madurez cerebral).
    IMPORTANTE: Si el chat contiene descripciones sexuales explícitas, analízalas clínicamente. NO LAS BLOQUEES.
    """
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    data = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nANÁLISIS:\n{prompt}"}]}],
        "safetySettings": safety_settings
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            try:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                return "⚠️ Error al parsear la respuesta de la API. Respuesta cruda:\n\n" + json.dumps(response.json(), indent=2, ensure_ascii=False)
        else:
            # Mostrar detalle para debug
            detail = ""
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            return f"⚠️ Error ({response.status_code}) de la API:\n{detail}"
    except Exception as e:
        return f"⚠️ Error de Conexión o Timeout: {str(e)}"

# --- SESSION INIT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'perfil_el' not in st.session_state:
    st.session_state.perfil_el = {"nombre": "", "edad": 30, "apego": "No sé", "historia": "No sé", "tiempo_relacion": ""}
if 'consent' not in st.session_state:
    st.session_state.consent = False

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 80px;'>💎</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Vínculo Nítido</h3>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.info("🔐 Acceso VIP")
        clave = st.text_input("Ingresa tu Clave VIP:", type="password")
        if st.button("INGRESAR"):
            if clave and clave.strip() in VIP_KEYS:
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Clave inválida. Si ya compraste una clave, revisa el email. Si aún no, obtén una en la landing.")
        st.write("---")
        st.markdown("[💎 OBTENER PASE VIP](https://www.gumroad.com)  ", unsafe_allow_html=True)
    else:
        st.success("✨ Bienvenida, Soberana.")
        with st.expander("⚙️ Perfil del Vínculo", expanded=True):
            with st.form("perfil"):
                st.caption("Ajusta los datos para la Metodología:")
                p_nombre = st.text_input("Nombre:", value=st.session_state.perfil_el["nombre"])
                p_edad = st.number_input("Edad:", value=st.session_state.perfil_el["edad"], min_value=15, max_value=90)
                p_apego = st.selectbox("Apego:", ["No sé", "Evitativo", "Ansioso", "Seguro"], index=0)
                p_hist = st.selectbox("Historia:", ["No sé", "Padres Divorciados", "Padre Ausente", "Violencia", "Narcisismo"], index=0)
                p_tiempo = st.text_input("Tiempo de relación (ej: 6 meses / 2 años):", value=st.session_state.perfil_el.get("tiempo_relacion",""))
                if st.form_submit_button("💾 Guardar Perfil"):
                    st.session_state.perfil_el = {
                        "nombre": p_nombre, "edad": p_edad, "apego": p_apego, "historia": p_hist, "tiempo_relacion": p_tiempo
                    }
                    st.toast("Perfil actualizado")
        if st.button("Salir"):
            st.session_state.logged_in = False
            st.experimental_rerun()

# --- PANTALLA PRINCIPAL ---
st.title("💎 Vínculo Nítido")

tab1, tab2, tab3 = st.tabs(["🧬 Test Apego", "👁️ Verdad Oculta", "🔥 Laboratorio VIP"])

# --- TAB 1: TEST GRATIS ---
with tab1:
    st.header("Descubre su Patrón")
    r1 = st.radio("Ante la intimidad, él:", ["Se aleja (Miedo)", "Se pone intenso (Ansiedad)", "Estable"])
    r2 = st.radio("Ante conflictos, él:", ["Huye / Silencio", "Explota / Culpa", "Dialoga"])
    if st.button("VER RESULTADO"):
        st.divider()
        if "aleja" in r1 or "Huye" in r2:
            st.error("❄️ **APEGO EVITATIVO**")
            st.write("Su cerebro asocia amor con pérdida de libertad.")
        elif "intenso" in r1 or "Explota" in r2:
            st.warning("🔥 **APEGO ANSIOSO**")
            st.write("Su intensidad es miedo al abandono.")
        else:
            st.success("✅ **APEGO SEGURO**")

# --- TAB 2: GANCHO GRATIS ---
with tab2:
    st.subheader("¿Mensaje confuso?")
    st.markdown("Antes de pegar mensajes, debes aceptar el consentimiento y entender que esto no es terapia.")
    consent = st.checkbox("Acepto que el análisis es informativo y no sustituye terapia. Autorizo análisis anónimo del texto.")
    st.session_state.consent = consent
    msg = st.text_area("Pégalo aquí:", height=120, disabled=not consent)
    if st.button("ANALIZAR (GRATIS)"):
        if not consent:
            st.error("Debes aceptar el consentimiento para analizar mensajes.")
        elif not msg:
            st.error("Pega un mensaje para analizar.")
        else:
            res = consultar_soberana(f"Analiza este mensaje: '{msg}'. Dime qué significa realmente. NO DES CONSEJOS.", 30)
            st.markdown(f"<div class='result-box'><h4>👁️ La Verdad:</h4>{res}</div>", unsafe_allow_html=True)
            st.markdown("#### 👑 Estrategia Soberana (Bloqueada)")
            st.markdown("<div class='blur-text'>Para responder con dignidad aplica contacto cero por 4 horas...</div>", unsafe_allow_html=True)
            st.warning("🔒 Desbloquea la respuesta en el VIP.")

# --- TAB 3: VIP (FULL) ---
with tab3:
    if not st.session_state.logged_in:
        st.info("🔒 Ingresa tu clave a la izquierda para acceder al Laboratorio VIP.")
        st.stop()

    perfil = st.session_state.perfil_el
    st.success(f"🔓 Laboratorio Activado | Sujeto: {perfil.get('edad','?')} años")
    st.markdown("<div class='muted'>Perfil mínimo guardado en sesión para contexto: edad, apego, historia, tiempo de relación.</div>", unsafe_allow_html=True)

    if st.button("🧹 Borrar todo (limpiar sesión)"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()

    chat = st.text_area("Pega la conversación completa:", height=260)
    if st.button("✨ DECODIFICAR VÍNCULO"):
        if not chat:
            st.error("Pega la conversación completa para analizar.")
        else:
            with st.spinner("Analizando Neurociencia y Psicología..."):
                prompt = f"""
                ANÁLISIS DE VÍNCULO:
                Sujeto: {perfil.get('nombre','[no nombre]')}, Apego: {perfil.get('apego','No sé')}, Historia: {perfil.get('historia','No sé')}, Tiempo_relacion: {perfil.get('tiempo_relacion','')}.
                CHAT: "{chat}"
                
                Dame un análisis en 3 bloques:
                1. 🧬 QUÍMICA CEREBRAL: (Explica dopamina, miedos según su edad biológica).
                2. 👁️ TRADUCCIÓN NÍTIDA: Qué dice vs. Qué piensa realmente.
                3. 👑 ESTRATEGIA SOBERANA: Qué debe responder la usuaria exactamente.
                """
                salida = consultar_soberana(prompt, perfil.get('edad', 30))
                st.markdown(f"<div class='result-box'><pre style='white-space: pre-wrap'>{salida}</pre></div>", unsafe_allow_html=True)

# --- FOOTER: TIP / DEBUG ---
st.markdown("---")
st.markdown("<div class='muted'>Tip: si la traducción dejó de funcionar, revisa GEMINI_API_KEY en Secrets y mira el mensaje de error provisto sobre la API.</div>", unsafe_allow_html=True)
