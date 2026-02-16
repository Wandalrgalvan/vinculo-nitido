import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

# --- BARRA LATERAL (CLAVE VIP) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=100)
    st.header("Zona VIP")
    clave_ingresada = st.text_input("🔑 Ingresá tu Clave de Acceso", type="password")
    
    # Buscamos la API KEY escondida en los secretos
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("⚠️ Falta configurar la API Key en los Secretos.")
        api_key = ""

# --- TÍTULO PRINCIPAL ---
st.title("💎 Vínculo Nítido")
st.subheader("Traductor de Mensajes Confusos a Verdad Soberana")

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🕵️‍♀️ Test Gratuito", "💬 Analizar Chat (VIP)", "🍷 Analizar Cita (VIP)"])

# --- PESTAÑA 1: TEST GRATUITO ---
with tab1:
    st.info("Descubrí qué perfil tiene el hombre con el que tratás.")
    
    perfil = st.radio("¿Cuál es su comportamiento principal?", 
                      ["Se aleja cuando hay intimidad (Miedo)", 
                       "Promete y no cumple (Inmadurez)", 
                       "Aparece y desaparece (Intermitencia)",
                       "Te hace sentir culpable (Manipulación)"])
    
    if st.button("Ver Diagnóstico Rápido"):
        if "aleja" in perfil:
            st.warning("🚨 Perfil Detectado: CAPITÁN DE CRISTAL. Su distancia no es desinterés, es pánico a sentir.")
        elif "Promete" in perfil:
            st.warning("🎈 Perfil Detectado: PETER PAN. Busca una madre, no una pareja.")
        elif "Aparece" in perfil:
            st.warning("👻 Perfil Detectado: EL FANTASMA. Solo vuelve para verificar que seguís disponible.")
        else:
            st.error("🐍 Perfil Detectado: NARCISISTA ENCUBIERTO. Cuidado, tu autoestima está en juego.")
        
        st.success("💡 ¿Querés saber qué esconden sus chats? Pasate a la pestaña VIP.")

# --- LÓGICA DE INTELIGENCIA ARTIFICIAL ---
def consultar_ia(prompt):
    if not api_key:
        return "Error: No hay API Key configurada."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- PESTAÑA 2: ANALIZAR CHAT ---
with tab2:
    st.write("Copiá la conversación y obtené la traducción real.")
    chat_texto = st.text_area("Pegá el chat aquí:", height=200)
    
    if st.button("✨ Analizar Verdad"):
        if clave_ingresada == "soberana2026": # LA CONTRASEÑA VIP
            if chat_texto:
                with st.spinner("La IA está leyendo entre líneas..."):
                    prompt = f"""
                    Actúa como una experta en psicología vincular. 
                    Analiza este chat de WhatsApp: "{chat_texto}".
                    1. ¿Qué patrón muestra él?
                    2. ¿Qué siente ella (la usuaria) y por qué?
                    3. Traducción de Nitidez: ¿Qué quiso decir realmente?
                    4. Consejo Soberano: ¿Qué debe hacer ella? (Acción concreta).
                    """
                    resultado = consultar_ia(prompt)
                    st.markdown(resultado)
            else:
                st.warning("Pegá un chat primero.")
        else:
            st.error("⛔ Acceso Denegado. Clave incorrecta.")

# --- PESTAÑA 3: ANALIZAR CITA ---
with tab3:
    st.write("Contame qué pasó en la cita.")
    relato = st.text_area("Escribí los detalles aquí:", height=150)
    
    if st.button("🔮 Diagnosticar Encuentro"):
        if clave_ingresada == "soberana2026":
            if relato:
                with st.spinner("Analizando micro-gestos y conductas..."):
                    prompt = f"""
                    Analiza esta cita: "{relato}".
                    Dime si hay 'Red Flags' (banderas rojas) o 'Green Flags'.
                    ¿Vale la pena una segunda cita? Sé brutalmente honesta.
                    """
                    resultado = consultar_ia(prompt)
                    st.markdown(resultado)
            else:
                st.warning("Escribí algo sobre la cita.")
        else:
            st.error("⛔ Acceso Denegado. Clave incorrecta.")
