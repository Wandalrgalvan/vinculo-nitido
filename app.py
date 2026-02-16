import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- ESTILO VISUAL MÍSTICO (CSS MEJORADO) ---
st.markdown("""
    <style>
    /* 1. Fondo Degradado Místico (Violeta Mágico) 
       Ya no es negro oscuro, es un degradado vibrante pero elegante */
    .stApp {
        background: rgb(45,0,70);
        background: linear-gradient(160deg, rgba(45,0,70,1) 0%, rgba(20,0,40,1) 50%, rgba(0,0,20,1) 100%);
        color: #FFFFFF;
    }

    /* 2. Barra Lateral CENTRADA y con estilo */
    section[data-testid="stSidebar"] {
        background-color: #1A0525; /* Violeta muy oscuro */
        text-align: center;
    }
    
    /* Truco para centrar la imagen y los títulos en la barra */
    section[data-testid="stSidebar"] .block-container {
        text-align: center;
        align-items: center;
    }
    
    section[data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        border-radius: 50%;
        border: 3px solid #D4AF37; /* Borde dorado */
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.5); /* Resplandor */
    }

    /* 3. Botones Dorados de Alto Valor */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDC830 100%);
        color: #000000;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        font-size: 16px;
        padding: 12px 24px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.6);
    }

    /* 4. CAJAS DE TEXTO (Ahora GRIS CLARO para leer mejor) */
    .stTextArea>div>div>textarea {
        background-color: #F5F5F5; /* Gris muy clarito, casi blanco */
        color: #000000; /* Letra negra */
        border: 2px solid #D4AF37;
        border-radius: 12px;
        font-family: sans-serif;
    }
    
    /* Inputs de contraseña */
    .stTextInput>div>div>input {
        background-color: #F5F5F5;
        color: black;
        border-radius: 10px;
    }

    /* 5. Títulos y Textos */
    h1 {
        text-align: center;
        color: #D4AF37 !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        font-size: 3rem !important;
    }
    h3 {
        text-align: center;
        color: #E6E6FA !important; /* Lavanda */
        font-style: italic;
    }
    p, li {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    # Imagen de silueta mística
    st.image("https://cdn.pixabay.com/photo/2019/04/06/00/39/woman-4106373_1280.jpg", width=160) 
    
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>Zona Soberana</h2>", unsafe_allow_html=True)
    st.write("---")
    st.write("Tu espacio de claridad, ciencia y poder.")
    
    st.write("")
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

st.write("") 

# AHORA SON 3 PESTAÑAS
tab1, tab2, tab3 = st.tabs(["🧠 Perfil Rápido", "🔬 Analizar Chat (VIP)", "👑 Consejera Real"])

# --- PESTAÑA 1: PERFIL ---
with tab1:
    st.info("Diagnóstico preliminar de conducta:")
    perfil = st.radio("¿Qué patrón repite él hoy?", 
                      ["Se aleja ante la intimidad (Apego Evitativo)", 
                       "Bombardea de amor y luego se va (Refuerzo Intermitente)", 
                       "Solo aparece de noche/sexting (Estrategia Corto Plazo)",
                       "Te culpa de sus reacciones (Gaslighting)"])
    
    st.write("")
    if st.button("Ver Diagnóstico"):
        st.success(f"Patrón detectado: **{perfil}**.")
        st.markdown("⚠️ **Alerta:** Este comportamiento altera tu química cerebral (Cortisol/Dopamina). Pasate a la pestaña VIP para romper el ciclo.")

# --- PESTAÑA 2: ANALIZAR CHAT ---
with tab2:
    st.write("Pegá la conversación. Vamos a aplicar neurociencia afectiva.")
    chat_texto = st.text_area("Chat de WhatsApp:", height=200, placeholder="Pega aquí el texto... (Tus datos son privados)")
    
    st.write("")
    if st.button("✨ DECODIFICAR MENTE MASCULINA"):
        if clave_ingresada == "soberana2026":
            if chat_texto:
                with st.spinner("Analizando niveles de dopamina, jerarquía y apego..."):
                    
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
                    - Traduce lo que dice a lo que realmente significa.
                    
                    4. 👑 **ESTRATEGIA SOBERANA:**
                    - Consejo de Alto Valor.
                    - Cómo responder (o callar) para recuperar el marco de poder.
                    """
                    
                    resultado = consultar_ia_auto(prompt)
                    st.markdown(resultado)
            else:
                st.warning("El chat está vacío.")
        else:
            st.error("⛔ Clave incorrecta.")

# --- PESTAÑA 3: CONSEJERA REAL (NUEVA) ---
with tab3:
    st.write("¿Qué te pasa por la mente? Desahogate o pedí un consejo puntual.")
    consulta = st.text_area("Escribí acá tu situación o cómo te sentís:", height=150, placeholder="Ej: Me siento ansiosa porque no escribe, quiero escribirle...")
    
    if st.button("💡 PEDIR CONSEJO SOBERANO"):
        if clave_ingresada == "soberana2026":
            if consulta:
                with st.spinner("Conectando con tu mejor versión..."):
                    prompt = f"""
                    Actúa como una Consejera de Alto Valor y Mentora de Vida.
                    La usuaria te cuenta esto: "{consulta}".
                    
                    No la juzgues. Valida sus emociones pero sacúdela con la verdad.
                    Dale una estrategia de dignidad.
                    Recuérdale quién es ella.
                    Tono: Amoroso pero firme. Como una hermana mayor sabia.
                    """
                    resultado = consultar_ia_auto(prompt)
                    st.markdown(resultado)
            else:
                st.warning("Escribí algo para aconsejarte.")
        else:
            st.error("⛔ Clave incorrecta.")
