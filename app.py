import streamlit as st
import requests
from datetime import datetime
import json
import mercadopago 

# --- CONFIG VISUAL Y PSICOLOGÍA DEL COLOR ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Roboto:wght@400;500&display=swap');
    
    /* --- FONDO PRINCIPAL Y BARRA LATERAL (Forzamos Modo Oscuro) --- */
    .stApp, [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important; 
        color: #F8FAFC !important; 
        font-family: 'Roboto', sans-serif; 
    }
    
    /* Forzar que los textos sueltos no se pongan negros */
    p, span, div, label { color: #F8FAFC !important; }
    
    h1, h2, h3, h4, h5, h6 { font-family: 'Montserrat', sans-serif; color: #5EEAD4 !important; font-weight: 600; }
    .stRadio label p { color: #FFFFFF !important; font-size: 1.05em !important; font-family: 'Roboto', sans-serif !important; }
    .muted { color: #94A3B8 !important; font-size: 0.95em; }
    
    /* --- CAJAS DE INSTRUCCIONES UX --- */
    .instruction-box { 
        background: rgba(20, 184, 166, 0.15) !important; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 4px solid #14B8A6; 
        margin-bottom: 20px; 
        font-size: 0.95em; 
        color: #FFFFFF !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #14B8A6 0%, #0D9488 100%) !important;
        color: #FFFFFF !important; font-weight: bold; border-radius: 8px; border: none; width: 100%; padding: 12px; transition: all 0.3s ease;
    }
    .stButton>button:hover { filter: brightness(1.1); color: #FFFFFF !important; }
    
    /* FIX DE TEXTOS LARGOS EN MENÚS DESPLEGABLES Y COLORES */
    div[data-baseweb="select"] > div:first-child { height: auto !important; min-height: 38px !important; }
    div[data-baseweb="select"] span { white-space: normal !important; word-wrap: break-word !important; overflow: visible !important; text-overflow: clip !important; display: block !important; line-height: 1.3 !important; }
    
    /* FIX: Color de fondo y texto de las opciones desplegables */
    ul[role="listbox"] { background-color: #1E293B !important; }
    ul[role="listbox"] li { 
        white-space: normal !important; 
        word-wrap: break-word !important; 
        height: auto !important; 
        min-height: 40px !important; 
        padding-top: 8px !important; 
        padding-bottom: 8px !important; 
        line-height: 1.3 !important; 
        color: #F8FAFC !important; /* Fuerza el texto blanco */
    }
    /* Efecto al pasar el mouse por las opciones */
    ul[role="listbox"] li:hover { background-color: #334155 !important; }

    /* --- EL FIX DE LAS CAJAS DE TEXTO (Para que se vea bien lo que se escribe) --- */
    /* Apuntamos específicamente a los inputs reales */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #0F172A !important; 
        color: #F8FAFC !important; /* Texto blanco brillante */
        -webkit-text-fill-color: #F8FAFC !important; /* Fix específico para iOS/Safari */
        font-size: 16px !important; /* Evita el auto-zoom en iPhone y mejora legibilidad */
    }
    
    /* Fondo del contenedor de las cajas de texto y selects */
    .stTextInput>div>div, .stTextArea>div>div, .stNumberInput>div>div, div[data-baseweb="select"]>div {
        background-color: #1E293B !important; 
        border: 1px solid #334155 !important; 
        border-radius: 6px;
    }
    
    .result-box { background: rgba(15, 23, 42, 0.6) !important; padding: 25px; border-left: 4px solid #5EEAD4; border-radius: 8px; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .chat-user { background: rgba(20, 184, 166, 0.1) !important; padding: 15px; border-radius: 8px 8px 0px 8px; margin-bottom: 10px; border-right: 3px solid #14B8A6; text-align: right; color: #FFFFFF !important; }
    .chat-bot { background: rgba(255, 255, 255, 0.05) !important; padding: 15px; border-radius: 8px 8px 8px 0px; margin-bottom: 10px; border-left: 3px solid #D4AF37; color: #FFFFFF !important; }
    .blur-text { filter: blur(5px); opacity: 0.6; pointer-events: none; }
    .vip-title { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- VIP KEYS (Originales + 100 Nuevas) ---
VIP_KEYS = [
    # --- Claves Originales ---
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
    "6789abcd-ef01-2345-6789-abcdef012345", "abcdef01-2345-6789-abcd-ef0123456789",
    # --- 100 Claves Nuevas ---
    "e4d909c2-901a-4286-a579-24285e6db8f1", "b3815e4f-21f4-4a82-965a-06387a329c2d", "c9a518d6-7248-43b9-8f0a-115f242c92e8", "7d4b6559-994c-4e8c-b9b5-683a45c79802", "8a1e537d-2b4f-4d69-a831-7b98d2543e1c",
    "5f6294a1-8d3e-4512-b11c-92b45398d7a1", "2c4819d5-7e9b-4682-938f-a1856d392e4b", "f13a86c9-1254-4d89-b052-7e8c459b13d2", "9b4d58a2-3f1c-4e76-8a5b-1c394d2876f5", "6e159a4b-827c-4193-b328-5a7c493218e6",
    "d2837f51-49b6-4328-91c5-8e7d413b96a2", "1a7b69c4-5d3e-4812-a729-b65c3418e9d5", "8c593a2e-1b4d-4769-9831-f2d47b5936c8", "4f18d5b9-7a2c-4e81-b593-c82e6d3197a4", "b64a13d8-952c-471e-8a62-d9b15c4837e2",
    "3e7c95a1-2d48-4693-b184-e5d79c3218f6", "9a2b85c3-1d4e-4732-a9b1-f6c834d925e7", "c51d8b94-7e2a-4168-93f5-a4b27d1958c6", "f84a2d19-3b5c-4e71-8c62-e15d3948b7a2", "2b9c7a41-8d5e-4319-b684-c5a17e9283d6",
    "a18d5c39-2b4f-4761-98a2-d6b359c47e18", "6c39b1a4-7d2e-4859-a5c8-e24d17b936f5", "d72e9a15-4b8c-4316-95f2-a8c14d39b7e6", "1f48a5b9-2c7d-4198-b365-c9e28d4157a3", "e9b25c48-1a7d-4639-8f41-d3a69b285c71",
    "8a5c3d19-4b2e-4716-98f5-e6c1a4d92b37", "4b1a8d5c-9e2f-4371-a6b5-c7d92e184f36", "c9d28a15-7b4e-4193-8f5c-a1b639d482e7", "f51a8c39-2d4b-4761-9c82-e3d15b497a62", "2d7b9a15-8c4e-4319-b5f6-c1a84d392e7b",
    "b8c45a19-3d7e-4162-9a5b-d2c81e394f76", "7e1a9b45-2d8c-4319-8f56-e4c13d29b7a8", "a4d91b5c-8e2f-4731-9c68-d1a52e394b76", "6b2c8a15-9d4e-4173-8f5a-e3d17c492b85", "d1a85c39-4b2e-4716-9f82-c5b61e49d7a3",
    "1c5a9b48-7d2e-4319-8b65-e4d13c298a7f", "e2b85a19-3c7d-4164-9f8a-d1c52e394b76", "9d4a1b5c-8e2f-4731-a6b5-c3d92e184f76", "5a1b8c39-4d2e-4716-9f85-e6c1a4d92b37", "c7d29a15-8b4e-4193-a5c8-e2d14b39a7f6",
    "f1a8c5d9-2b4e-4761-9c82-d3a65b497e18", "3d7b9a15-8c4e-4319-b5f6-c1a84d392e7b", "8b5c4a19-3d7e-4162-9a5b-d2c81e394f76", "4e1a9b5c-2d8c-4319-8f56-e4c13d29b7a8", "a2d91b5c-8e2f-4731-9c68-d1a52e394b76",
    "6c2b8a15-9d4e-4173-8f5a-e3d17c492b85", "d3a85c39-4b2e-4716-9f82-c5b61e49d7a3", "1e5a9b48-7d2e-4319-8b65-e4d13c298a7f", "e4b85a19-3c7d-4164-9f8a-d1c52e394b76", "9f4a1b5c-8e2f-4731-a6b5-c3d92e184f76",
    "5c1b8a39-4d2e-4716-9f85-e6c1a4d92b37", "c9d29a15-8b4e-4193-a5c8-e2d14b39a7f6", "f3a8c5d9-2b4e-4761-9c82-d3a65b497e18", "3f7b9a15-8c4e-4319-b5f6-c1a84d392e7b", "8d5c4a19-3d7e-4162-9a5b-d2c81e394f76",
    "4a1a9b5c-2d8c-4319-8f56-e4c13d29b7a8", "a4d91b5c-8e2f-4731-9c68-d1a52e394b76", "6e2b8a15-9d4e-4173-8f5a-e3d17c492b85", "d5a85c39-4b2e-4716-9f82-c5b61e49d7a3", "1a5a9b48-7d2e-4319-8b65-e4d13c298a7f",
    "e6b85a19-3c7d-4164-9f8a-d1c52e394b76", "9a4a1b5c-8e2f-4731-a6b5-c3d92e184f76", "5e1b8a39-4d2e-4716-9f85-e6c1a4d92b37", "cb d29a15-8b4e-4193-a5c8-e2d14b39a7f6", "f5a8c5d9-2b4e-4761-9c82-d3a65b497e18",
    "3a7b9a15-8c4e-4319-b5f6-c1a84d392e7b", "8f5c4a19-3d7e-4162-9a5b-d2c81e394f76", "4c1a9b5c-2d8c-4319-8f56-e4c13d29b7a8", "a6d91b5c-8e2f-4731-9c68-d1a52e394b76", "6a2b8a15-9d4e-4173-8f5a-e3d17c492b85",
    "d7a85c39-4b2e-4716-9f82-c5b61e49d7a3", "1c5a9b48-7d2e-4319-8b65-e4d13c298a7f", "e8b85a19-3c7d-4164-9f8a-d1c52e394b76", "9c4a1b5c-8e2f-4731-a6b5-c3d92e184f76", "5a1b8a39-4d2e-4716-9f85-e6c1a4d92b37",
    "cd d29a15-8b4e-4193-a5c8-e2d14b39a7f6", "f7a8c5d9-2b4e-4761-9c82-d3a65b497e18", "3c7b9a15-8c4e-4319-b5f6-c1a84d392e7b", "8a5c4a19-3d7e-4162-9a5b-d2c81e394f76", "4e1a9b5c-2d8c-4319-8f56-e4c13d29b7a8",
    "a8d91b5c-8e2f-4731-9c68-d1a52e394b76", "6c2b8a15-9d4e-4173-8f5a-e3d17c492b85", "d9a85c39-4b2e-4716-9f82-c5b61e49d7a3", "1e5a9b48-7d2e-4319-8b65-e4d13c298a7f", "eab85a19-3c7d-4164-9f8a-d1c52e394b76",
    "9e4a1b5c-8e2f-4731-a6b5-c3d92e184f76", "5c1b8a39-4d2e-4716-9f85-e6c1a4d92b37", "cf d29a15-8b4e-4193-a5c8-e2d14b39a7f6", "f9a8c5d9-2b4e-4761-9c82-d3a65b497e18", "3e7b9a15-8c4e-4319-b5f6-c1a84d392e7b",
    "8c5c4a19-3d7e-4162-9a5b-d2c81e394f76", "4a1a9b5c-2d8c-4319-8f56-e4c13d29b7a8", "aad91b5c-8e2f-4731-9c68-d1a52e394b76", "6e2b8a15-9d4e-4173-8f5a-e3d17c492b85", "dba85c39-4b2e-4716-9f82-c5b61e49d7a3",
    "1a5a9b48-7d2e-4319-8b65-e4d13c298a7f", "ecb85a19-3c7d-4164-9f8a-d1c52e394b76", "9a4a1b5c-8e2f-4731-a6b5-c3d92e184f76", "5e1b8a39-4d2e-4716-9f85-e6c1a4d92b37", "c1d29a15-8b4e-4193-a5c8-e2d14b39a7f6"
]
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
        # UX TEXT: INGRESO VIP
        st.markdown("<div class='instruction-box'><b>👋 Bienvenida:</b> Si ya tienes tu clave, ingrésala abajo. Si aún no tienes pase, elige una opción de pago para desbloquear la metodología completa.</div>", unsafe_allow_html=True)
        
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
        
        # --- BOTÓN GUMROAD ---
        st.markdown("""
        <a href="TU_LINK_DE_GUMROAD_AQUI" target="_blank" style="text-decoration: none; display: block; width: 100%; box-sizing: border-box;">
            <div style="background-color: #0F172A; border: 1px solid #14B8A6; color: white; padding: 12px; border-radius: 6px; text-align: center; transition: 0.3s; margin-bottom: 10px; word-wrap: break-word;">
                <span style="font-weight: bold; font-size: 1.05em; color: #5EEAD4;">Obtener Pase VIP</span><br>
                <span style="font-size: 0.75em; color: #94A3B8;">🌍 Pago con Tarjeta (Entrega Inmediata)</span>
            </div>
        </a>
        """, unsafe_allow_html=True)
        
       # --- BOTÓN MERCADO PAGO DINÁMICO ---
        try:
            sdk = mercadopago.SDK(st.secrets["MP_ACCESS_TOKEN"])
            preference_data = {
                "items": [
                    {
                        "title": "Pase VIP - Vínculo Nítido",
                        "quantity": 1,
                        "unit_price": 100.0,
                        "currency_id": "ARS"
                    }
                ],
                "binary_mode": True,
                "purpose": "wallet_purchase" 
            }
            preference_response = sdk.preference().create(preference_data)
            
            if "response" in preference_response and "init_point" in preference_response["response"]:
                link_oficial_mp = preference_response["response"]["init_point"]
                st.markdown(f"""
                <a href="{link_oficial_mp}" target="_blank" style="text-decoration: none; display: block; width: 100%; box-sizing: border-box;">
                    <div style="background-color: transparent; border: 1px dashed #475569; color: #CBD5E1; padding: 10px; border-radius: 6px; text-align: center; transition: 0.3s; word-wrap: break-word;">
                        <span style="font-weight: bold; font-size: 0.9em;">🇦🇷 Opción Argentina ($5.900 ARS)</span><br>
                        <span style="font-size: 0.75em;">Pagar con Mercado Pago</span>
                    </div>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Error de Mercado Pago: {preference_response}")
                
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.markdown(f"""
            <a href="{link_oficial_mp}" target="_blank" style="text-decoration: none; display: block; width: 100%; box-sizing: border-box;">
                <div style="background-color: transparent; border: 1px dashed #475569; color: #CBD5E1; padding: 10px; border-radius: 6px; text-align: center; transition: 0.3s; word-wrap: break-word;">
                    <span style="font-weight: bold; font-size: 0.9em;">🇦🇷 Opción Argentina ($5.900 ARS)</span><br>
                    <span style="font-size: 0.75em;">Pagar con Mercado Pago</span>
                </div>
            </a>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown("<p style='text-align: center; font-size: 0.75em; color: #EF4444;'>Conectando pasarela local...</p>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; font-size: 0.75em; color: #64748B; margin-top: 10px;'>🔒 Tu clave VIP será enviada automáticamente a tu correo tras el pago.</p>", unsafe_allow_html=True)
    else:
        st.success("👩🏻‍💼 Bienvenida, Soberana.")
        
        # UX TEXT: INSTRUCCIÓN PARA COMPLETAR EL PERFIL
        st.markdown("<div class='instruction-box'><b>🚨 Paso Indispensable:</b> Completa el perfil de tu vínculo. Nuestro sistema requiere este contexto clínico para calibrar la decodificación.</div>", unsafe_allow_html=True)

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
    
    st.markdown("<div class='instruction-box'><b>¿Para qué sirve?</b> Este test gratuito identifica su patrón de comportamiento primario. Saber esto te permitirá entender por qué reacciona de cierta manera ante la cercanía.</div>", unsafe_allow_html=True)
    
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
    
    st.markdown("<div class='instruction-box'><b>¿Cómo usarlo?</b> Pega ese mensaje suelto que te dejó con dudas. El sistema aislará las palabras y traducirá la intención real oculta tras ellas.</div>", unsafe_allow_html=True)
    
    consent = st.checkbox("Acepto que este análisis es informativo, basado en patrones de comportamiento, y no sustituye terapia.")
    st.session_state.consent = consent
    
    msg = st.text_area("Pega su mensaje aquí:", height=120, disabled=not consent)
    if st.button("TRADUCIR (GRATIS)"):
        if not consent:
            st.error("Requisito clínico: Debes aceptar el consentimiento.")
        elif not msg:
            st.error("Falta información. Pega un mensaje para analizar.")
        else:
            # --- NUEVO PROMPT SIMPLE TAB 2 ---
            instruccion = """
            Eres Wanda Soberana, mentora experta en relaciones. 
            Traduce la intención real y oculta de este mensaje. 
            Menciona la neurociencia (dopamina, cortisol, apego) pero explícalo con palabras SÚPER SIMPLES, coloquiales y fáciles de entender para una mujer que no tiene estudios científicos. 
            Sé cruda, directa y reveladora. Habla de tú a tú. 
            REGLA DE ORO: NO uses términos médicos complejos (prohibido decir 'corteza prefrontal', 'hipotálamo', etc.). 
            NO des consejos, solo expón la verdad de cómo él está manipulando la situación o buscando placer fácil.
            """
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
        st.error("⚠️ **ACCIÓN REQUERIDA:** Despliega el 'Perfil del Vínculo' en el menú de la izquierda y guarda sus datos antes de iniciar. El Laboratorio necesita esta información base.")
        nombre_mostrar = "Sujeto"
        
    st.markdown("<div class='instruction-box'><b>Protocolo Avanzado:</b> Pega aquí el historial completo de la conversación (puedes copiar y pegar directo de WhatsApp). La metodología cruzará estos textos con el perfil psicológico que cargaste para entregarte su estado químico y tu estrategia de respuesta.</div>", unsafe_allow_html=True)

    st.success(f"🔓 Laboratorio Clínico | Analizando a: {nombre_mostrar} ({perfil.get('edad', 30)} años) | {perfil.get('tipo_relacion', '')}")

    chat = st.text_area("Pega la interacción de texto completa (WhatsApp/Redes):", height=200)
    if st.button("✨ INICIAR PROTOCOLO DE DECODIFICACIÓN"):
        if not chat:
            st.error("Se requiere el historial de mensajes para iniciar el protocolo.")
        else:
            with st.spinner("Procesando patrones neuroconductuales... (Si demora más de 20 segundos, es normal por la complejidad de tu interacción)"):
                # --- NUEVO PROMPT SIMPLE TAB 3 (LAB VIP) ---
                instruccion = f"""
                Eres Wanda Soberana, creadora de 'Vínculo Nítido'. Eres Mentora, experta en relaciones y comportamiento humano.
                Tu análisis debe ser crudo, directo, revelador, pero profundamente empático con la usuaria. NUNCA digas que eres IA.
                Sujeto a analizar: {nombre_mostrar}, Edad: {perfil.get('edad', 30)}, Tipo de Vínculo: {perfil.get('tipo_relacion', 'No sé')}, Apego: {perfil.get('apego','No sé')}.
                
                REGLA DE ORO: Escribe de forma SÚPER SIMPLE, coloquial y fácil de entender. Habla como una amiga sabia y directa. ESTÁ ESTRICTAMENTE PROHIBIDO usar términos médicos, académicos o psicológicos complejos (nada de 'hipotálamo', 'corteza', 'sistema límbico', 'gaslighting', 'override', etc.). Si hablas de química, usa solo "dopamina" (adicción/placer rápido) o "cortisol" (estrés/ansiedad) y explícalo en lenguaje de calle.

                Devuelve exactamente 3 bloques usando Markdown:
                
                ### 1. 🧬 LA QUÍMICA DEL MOMENTO
                Explica brevemente (máximo 2 párrafos cortos) qué está pasando en la cabeza de él y de ella. Ejemplo: "Él te busca para un shot rápido de dopamina (placer sin esfuerzo), mientras a ti te sube el cortisol (estrés) por la incertidumbre."
                
                ### 2. 👁️ LA VERDAD CRUDA (Traducción)
                Toma 2 o 3 frases clave de lo que él dijo y traduce qué significan realmente en su idioma de manipulación o evasión. Desnuda sus excusas.
                
                ### 3. 👑 TU MOVIMIENTO SOBERANO
                Dile exactamente cómo recuperar el poder. Dale una (y solo una) frase literal, corta y fría que debe copiar y pegar para responderle, o indícale si debe clavar el visto.
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
    
    st.markdown("<div class='instruction-box'><b>Tu Espacio Seguro:</b> Aquí no analizamos mensajes, aquí hablamos de ti. Cuéntame la situación con tus propias palabras, haz catarsis o pide claridad. Te escucharé y responderé como tu mentora personal.</div>", unsafe_allow_html=True)
    
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
                    # --- NUEVO PROMPT RESTRINGIDO TAB 4 (CONSULTORIO) ---
                    instruccion_consultorio = f"""
                    Eres Wanda Soberana. Estás en una sesión de mentoría 1 a 1 (Consultorio Soberano).
                    La usuaria te está contando situaciones de su vida, su relación con {nombre_consultorio} (Tipo de Vínculo: {st.session_state.perfil_el.get('tipo_relacion', 'No sé')}, Apego: {st.session_state.perfil_el.get('apego', 'No sé')}) o dudas sobre su valor y proyectos.
                    
                    Tono: Eres una mentora cruda, validas profundamente sus emociones, le das claridad clínica sobre lo que está viviendo y la empoderas. Dialogas de tú a tú.
                    
                    REGLA DE ORO DE FORMATO (¡ESTRICTO!): 
                    1. Tu respuesta debe ser CORTA, ÁGIL y DIRECTA, simulando un chat real.
                    2. MÁXIMO 3 párrafos cortos. ¡Prohibido escribir testamentos!
                    3. Ve directo al hueso del problema. No des vueltas.
                    4. Termina SIEMPRE con UNA sola pregunta poderosa y corta que la haga reflexionar y continuar la charla.
                    
                    HISTORIAL DE LA CHARLA RECIENTE:
                    {historial_str}
                    
                    Responde al último mensaje de la usuaria aplicando estrictamente estas reglas de longitud.
                    """
                    respuesta_wanda = llamar_gemini(nueva_consulta, instruccion_consultorio)
                    st.session_state.mensajes_consultorio.append({"rol": "wanda", "texto": respuesta_wanda})
                    st.rerun()
    with col2:
        if st.button("🧹 Limpiar Charla"):
            st.session_state.mensajes_consultorio = []
            st.rerun()

st.markdown("---")

# --- NUEVO BLOQUE: ESCUDO LEGAL Y PRIVACIDAD ---
with st.expander("⚖️ Términos, Privacidad y Aviso Legal"):
    st.markdown("""
    **1. Naturaleza del Servicio:** Vínculo Nítido es una herramienta educativa y de análisis basada en patrones de comportamiento. NO es un diagnóstico médico ni psicológico, y NO reemplaza la terapia profesional con un especialista en salud mental.  
    **2. Privacidad Absoluta:** Tus chats y relatos son tuyos. No almacenamos tus conversaciones en bases de datos para lectura humana. Los textos se envían de forma cifrada al motor de análisis y se descartan inmediatamente tras generar la respuesta.  
    **3. Política de Reembolso:** Al tratarse de un producto digital de consumo y entrega inmediata (Pase VIP), no se realizan reembolsos una vez procesado el pago y enviada la clave de acceso.
    """, unsafe_allow_html=True)

st.markdown("<div class='muted'>Vínculo Nítido © 2026 | Metodología Soberana</div>", unsafe_allow_html=True)
