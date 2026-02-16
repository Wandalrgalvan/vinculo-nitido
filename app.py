import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- ESTILO VISUAL MÍSTICO (CSS) ---
st.markdown("""
    <style>
    /* 1. Fondo Degradado Místico (Violeta Profundo a Negro) */
    .stApp {
        background: rgb(20,0,30);
        background: linear-gradient(180deg, rgba(20,0,30,1) 0%, rgba(10,0,20,1) 100%);
        color: #E6E6FA; /* Color Lavanda claro para el texto (muy legible) */
    }

    /* 2. Centrar la Barra Lateral */
    [data-testid="stSidebar"] {
        text-align: center;
        background-color: #11001C; /* Fondo oscuro para la barra */
    }
    
    /* Ajuste para que las imágenes de la barra lateral se centren */
    [data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%; /* La hace redonda */
        border: 2px solid #D4AF37; /* Borde dorado */
    }

    /* 3. Botones Dorados */
    .stButton>button {
        background: linear-gradient(to right, #D4AF37, #C5A028);
        color: black;
        border: none;
        border-radius: 20px;
        font-weight: bold;
        padding: 10px 24px;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4); /* Brillo dorado */
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: #333;
    }

    /* 4. Cajas de Texto (Inputs) */
    .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.1); /* Transparente sutil */
        color: white;
        border: 1px solid #D4AF37;
        border-radius: 10px;
    }
    
    /* 5. Títulos */
    h1 {
        text-align: center;
        color: #D4AF37 !important; /* Dorado */
        font-family: 'Helvetica', sans-serif;
        text-shadow: 2px 2px 4px #000000;
    }
    h3 {
        text-align: center;
        color: #B0C4DE !important;
        font-weight: 300;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    # Imagen de silueta con flores y mariposas
    st.image("https://img.freepik.com/fotos-premium/silueta-mujer-mariposas-flores-cabeza-fondo-negro-ia-generativa_585735-3004.jpg", width=180) 
    
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>Zona Soberana</h2>", unsafe_allow_html=True)
    st.write("---") # Línea divisoria
    st.write("Tu espacio de claridad y poder.")
    
    st.write("") # Espacio
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

# --- INTERFAZ PRINCIPAL ---
st.title("💎 Vínculo Nítido")
st.markdown("### *Decodificando la mente masculina con ciencia*")

st.write("") # Espacio para airear

tab1, tab2 = st.tabs(["🧠 Perfil Rápido", "🔬 Analizar Chat (VIP)"])

with tab1:
    st.info("Diagnóstico preliminar de conducta:")
    perfil = st.radio("¿Qué patrón repite él hoy?", 
                      ["Se aleja ante la intimidad (Apego Evitativo)", 
                       "Bombardea de amor y luego se va (Refuerzo Intermitente)", 
                       "Solo aparece de noche/sexting (Estrategia de Corto Plazo)",
                       "Te culpa de sus reacciones (Gaslighting)"])
    
    st.write("")
    if st.button("Ver Diagnóstico"):
        st.success(f"Patrón detectado: **{perfil}**.")
        st.write("Pasate a la pestaña VIP para entender qué neuroquímicos está activando en tu cerebro.")

with tab2:
    st.write("Pegá la conversación. Vamos a aplicar neurociencia afectiva.")
    chat_texto = st.text_area("Chat de WhatsApp:", height=250, placeholder="Pega aquí el texto...")
    
    st.write("")
    if st.button("✨ DECODIFICAR MENTE MASCULINA"):
        if clave_ingresada == "soberana2026":
            if chat_texto:
                with st.spinner("Analizando niveles de dopamina, jerarquía y apego..."):
                    
                    # --- PROMPT CIENTÍFICO ---
                    prompt = f"""
                    Actúa como 'Wanda Soberana': experta en Neurociencia Afectiva, Psicología Evolutiva y Comportamiento Masculino.
                    Tono: Directo, empoderador, de mujer a mujer, pero con base científica sólida.
                    
                    ANALIZA ESTE CHAT: "{chat_texto}"
                    
                    Estructura tu respuesta en estos 4 bloques exactos (Usa negritas y emojis):

                    1. 🧬 **DIAGNÓSTICO DEL SISTEMA NERVIOSO:**
                    - Estilo de Apego detectado en él.
                    - ¿Qué circuito está activando en ELLA? (¿Ansiedad/Cortisol? ¿Adicción a la Dopamina?).
                    
                    2. 🦁 **PSICOLOGÍA EVOLUTIVA (La verdad biológica):**
                    - ¿Estrategia reproductiva de él? (Corto plazo vs Largo plazo).
                    - Nivel de Inversión: ¿Es cazador o recolector oportunista?
                    
                    3. 👁️ **TRADUCCIÓN NÍTIDA:**
                    - Traduce lo que dice a lo que realmente significa sus actos.
                    
                    4. 👑 **ESTRATEGIA SOBERANA:**
                    - Consejo de Alto Valor.
                    - Cómo responder para recuperar el marco de poder y dejar de perseguir.
                    """
                    
                    resultado = consultar_ia_auto(prompt)
                    st.markdown(resultado)
            else:
                st.warning("El chat está vacío.")
        else:
            st.error("⛔ Clave incorrecta.")
