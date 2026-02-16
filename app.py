import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=100)
    st.header("Zona VIP")
    clave_ingresada = st.text_input("🔑 Ingresá tu Clave de Acceso", type="password")
    
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("⚠️ Falta configurar la API Key en los Secretos.")
        api_key = ""

# --- FUNCIÓN DE CONEXIÓN DIRECTA (SIN INTERMEDIARIOS) ---
def consultar_ia_directa(prompt):
    if not api_key:
        return "Error: No hay API Key."
    
    # URL directa a la API de Google (Modelo 1.5 Flash)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            # Si salió bien, extraemos el texto
            resultado = response.json()
            return resultado['candidates'][0]['content']['parts'][0]['text']
        else:
            # Si salió mal, mostramos el error crudo de Google para saber qué pasa
            return f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ PRINCIPAL ---
st.title("💎 Vínculo Nítido")
st.subheader("Traductor de Mensajes Confusos a Verdad Soberana")

tab1, tab2 = st.tabs(["🕵️‍♀️ Test Rápido", "💬 Analizar Chat (VIP)"])

with tab1:
    st.info("Diagnóstico Express")
    perfil = st.radio("Conducta principal:", ["Se aleja (Miedo)", "Promete y no cumple (Inmaduro)", "Intermitente (Fantasma)"])
    if st.button("Ver Resultado"):
        st.warning(f"Posible perfil detectado para: {perfil}. Pasate al VIP para más detalle.")

with tab2:
    st.write("Pegá la conversación para analizarla con IA Real.")
    chat_texto = st.text_area("Chat:", height=200)
    
    if st.button("✨ Analizar Verdad"):
        if clave_ingresada == "soberana2026":
            if chat_texto:
                with st.spinner("Conectando directo con el cerebro de Google..."):
                    prompt = f"Actúa como psicóloga experta. Analiza este chat: '{chat_texto}'. Dame: 1. Patrón oculto. 2. Qué siente ella. 3. Traducción real. 4. Consejo directo."
                    resultado = consultar_ia_directa(prompt)
                    st.markdown(resultado)
            else:
                st.warning("Escribí algo.")
        else:
            st.error("⛔ Clave incorrecta.")
