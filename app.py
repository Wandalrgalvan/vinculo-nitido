import streamlit as st
import requests
import json

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🧬", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 10px; font-weight: bold; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica', sans-serif; }
    .stTextArea>div>div>textarea { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://img.freepik.com/fotos-premium/retrato-moda-mujer-hermosa-reina-corona-oro-diosa-griega-ia-generativa_438099-12372.jpg", width=200) 
    st.header("Zona Soberana")
    st.write("Análisis con Neurociencia y Psicología Aplicada.")
    clave_ingresada = st.text_input("🔑 Tu Clave VIP", type="password")
    
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("⚠️ Falta API Key")
        api_key = ""

# --- MOTOR DE INTELIGENCIA (AUTO-DETECT) ---
def obtener_modelo_valido(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            for modelo in datos.get('models', []):
                if 'generateContent' in modelo.get('supportedGenerationMethods', []):
                    if 'gemini' in modelo['name']:
                        return modelo['name']
            return "models/gemini-pro"
        else:
            return None
    except:
        return None

def consultar_ia_auto(prompt):
    if not api_key: return "Error: No hay API Key."
    modelo = obtener_modelo_valido(api_key)
    if not modelo: return "Error de conexión con Google."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/{modelo}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- INTERFAZ ---
st.title("🧬 Vínculo Nítido")
st.markdown("### *Decodificando la mente masculina con ciencia*")

tab1, tab2 = st.tabs(["🧠 Perfil Rápido", "🔬 Analizar Chat (VIP)"])

with tab1:
    st.info("Diagnóstico preliminar de conducta:")
    perfil = st.radio("¿Qué patrón repite él?", 
                      ["Se aleja ante la intimidad (Apego Evitativo)", 
                       "Bombardea de amor y luego se va (Refuerzo Intermitente)", 
                       "Solo aparece de noche/sexting (Estrategia Reproductiva a Corto Plazo)",
                       "Te culpa de sus reacciones (Manipulación/Gaslighting)"])
    
    if st.button("Ver Diagnóstico"):
        st.write(f"Has detectado: **{perfil}**. Pasate al VIP para entender la neurociencia detrás de esto.")

with tab2:
    st.write("Pegá la conversación. La IA buscará patrones subconscientes.")
    chat_texto = st.text_area("Chat de WhatsApp:", height=250)
    
    if st.button("✨ ESCHUCHAR LA VERDAD CIENTÍFICA"):
        if clave_ingresada == "soberana2026":
            if chat_texto:
                with st.spinner("Analizando niveles de dopamina, apego y jerarquía..."):
                    
                    # --- AQUÍ ESTÁ EL PROMPT CIENTÍFICO ---
                    prompt = f"""
                    Actúa como 'Wanda Soberana': una experta en Neurociencia Afectiva, Psicología Evolutiva, Teoría del Apego y Comportamiento Masculino.
                    Tu tono debe ser directo, empoderador y crudo (de mujer a mujer), pero tus argumentos deben tener base científica sólida.
                    
                    ANALIZA ESTE CHAT: "{chat_texto}"
                    
                    Estructura tu respuesta en estos 4 bloques exactos:

                    1. 🧬 **DIAGNÓSTICO DEL SISTEMA NERVIOSO Y APEGO:**
                    - Identifica el Estilo de Apego de él (¿Es Evitativo Despectivo? ¿Ansioso?).
                    - ¿Qué está pasando en el cerebro de ELLA? (¿Él está usando "Refuerzo Intermitente" para generarle adicción a la dopamina? ¿Hay breadcrumbing?).
                    
                    2. 🦁 **PSICOLOGÍA EVOLUTIVA (La verdad biológica):**
                    - ¿Qué estrategia reproductiva está usando él? (¿Inversión a largo plazo o acceso sexual a bajo costo?).
                    - Analiza la "Inversión de Esfuerzo": ¿Él caza o solo espera recibir?
                    
                    3. 👁️ **TRADUCCIÓN NÍTIDA (Sin anestesia):**
                    - Traduce sus palabras bonitas a la realidad de sus actos.
                    - "Él dice X, pero su comportamiento grita Y".
                    
                    4. 👑 **ESTRATEGIA SOBERANA (Acción):**
                    - Un consejo basado en la dignidad y el "Alto Valor".
                    - ¿Cómo romper el ciclo de adicción química?
                    - Qué responder (o qué callar) para recuperar el poder.
                    
                    Sé breve, contundente y no uses jerga médica aburrida, explicá los conceptos complejos de forma simple y reveladora.
                    """
                    
                    resultado = consultar_ia_auto(prompt)
                    st.markdown(resultado)
            else:
                st.warning("El chat está vacío.")
        else:
            st.error("⛔ Clave incorrecta.")
