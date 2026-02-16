import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
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

# --- FUNCIÓN INTELIGENTE: BUSCAR MODELO DISPONIBLE ---
def obtener_modelo_valido(api_key):
    """Pregunta a Google qué modelos están habilitados para esta llave."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            # Buscamos el primer modelo que sirva para generar texto
            for modelo in datos.get('models', []):
                if 'generateContent' in modelo.get('supportedGenerationMethods', []):
                    # Preferimos modelos "pro" o "flash" si hay varios
                    if 'gemini' in modelo['name']:
                        return modelo['name']
            return "models/gemini-pro" # Fallback por defecto
        else:
            return None
    except:
        return None

# --- FUNCIÓN DE CONSULTA ---
def consultar_ia_auto(prompt):
    if not api_key:
        return "Error: No hay API Key."

    # PASO 1: Detectar modelo automáticamente
    modelo_a_usar = obtener_modelo_valido(api_key)
    
    if not modelo_a_usar:
        return "Error: Tu llave no tiene acceso a ningún modelo. Revisá tu cuenta de Google."

    # PASO 2: Usar ese modelo
    url = f"https://generativelanguage.googleapis.com/v1beta/{modelo_a_usar}:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error ({modelo_a_usar}): {response.text}"
            
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ ---
st.title("💎 Vínculo Nítido")
st.success("Sistema conectado. Modo Auto-Detección activado.")

tab1, tab2 = st.tabs(["🕵️‍♀️ Test Rápido", "💬 Analizar Chat (VIP)"])

with tab1:
    st.write("Diagnóstico Express")
    perfil = st.radio("Conducta:", ["Se aleja", "Promete y no cumple", "Fantasma"])
    if st.button("Ver Resultado"):
        st.warning(f"Posible perfil detectado: {perfil}.")

with tab2:
    st.write("Pegá la conversación:")
    chat_texto = st.text_area("Chat:", height=200)
    
    if st.button("✨ Analizar Verdad"):
        if clave_ingresada == "soberana2026":
            if chat_texto:
                with st.spinner("Buscando el mejor modelo de IA disponible..."):
                    prompt = f"Actúa como psicóloga experta. Analiza: '{chat_texto}'."
                    resultado = consultar_ia_auto(prompt)
                    st.markdown(resultado)
            else:
                st.warning("Escribí algo.")
        else:
            st.error("⛔ Clave incorrecta.")
