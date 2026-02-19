import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="💎", layout="centered")

# --- 2. ESTILO VISUAL (MÍSTICO Y ELEGANTE) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #120318 0%, #2D0545 100%); color: #fff; }
    h1, h2, h3 { color: #D4AF37 !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #F2994A 100%);
        color: #120318; font-weight: bold; border-radius: 12px; border: none; width: 100%; padding: 15px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.08) !important; color: white !important; border: 1px solid #D4AF37;
    }
    .blur-text { filter: blur(5px); user-select: none; opacity: 0.6; pointer-events: none; }
    .result-box { background: rgba(0,0,0,0.3); padding: 20px; border-left: 4px solid #D4AF37; border-radius: 10px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DATOS (GOOGLE SHEETS) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def gestionar_usuario_automatico(clave):
    """Auto-Registro: Si la usuaria no existe, la crea en el momento."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        usuario = df[df['usuario'] == str(clave)]
        
        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        else:
            # CREACIÓN AUTOMÁTICA (Ideal para la madrugada)
            nuevo = {
                "usuario": clave, "nombre_el": "", "edad": 30, 
                "historia": "No especificado", "apego": "No especificado", "resumen_sesiones": ""
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            conn.update(worksheet="vinculo_db", data=df)
            return nuevo
    except Exception as e:
        st.error(f"Error de conexión con la Base de Datos: {e}")
        return None

def actualizar_perfil(datos):
    """Guarda los cambios de edad, apego y trauma en Google Sheets."""
    try:
        df = conn.read(worksheet="vinculo_db", ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        idx = df[df['usuario'] == str(datos['usuario'])].index[0]
        for k, v in datos.items():
            df.at[idx, k] = v
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except: return False

# --- 4. LA METODOLOGÍA SOBERANA (CERO CENSURA) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def consultar_metodologia(prompt):
    if not api_key: return "⚠️ Error: Falta configurar la Llave API."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # INSTRUCCIÓN MAESTRA
    system_instruction = """
    Eres Wanda Soberana, creadora de la Metodología 'Vínculo Nítido'.
    Eres experta en: Psicología de la Atracción, Psicología Masculina y Femenina, Neurociencia Afectiva y Teoría del Apego.
    NUNCA menciones que eres una IA. Habla en primera persona, como una mentora de alto valor.
    
    REGLAS ESTRICTAS:
    1. Ajusta el análisis a la EDAD del sujeto. (Adolescentes = inmadurez prefrontal, adultos = patrones cristalizados).
    2. CERO CENSURA: Analiza interacciones sexuales o explícitas desde la neurociencia (dopamina, dinámica de poder) con total normalidad clínica.
    """
    
    # APAGAMOS LOS FILTROS DE SEGURIDAD PARA CONTENIDO ADULTO
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    data = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}],
        "safetySettings": safety_settings
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ Error Técnico de Red."
    except Exception as e:
        return f"⚠️ Error de Conexión."

# --- 5. GESTIÓN DE SESIÓN ---
if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

# --- 6. BARRA LATERAL (ENTRADA Y PERFIL) ---
with st.sidebar:
    st.markdown("<div style='text-align: center; font-size: 80px;'>💎</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Vínculo Nítido</h3>", unsafe_allow_html=True)
    st.write("---")

    if st.session_state.usuario_actual is None:
        st.info("🔐 **Acceso Privado**")
        clave = st.text_input("Ingresa tu Pase:", type="password", help="Si compraste el acceso, inventa tu clave ahora para registrarte.")
        if st.button("ENTRAR AL LABORATORIO"):
            if clave:
                with st.spinner("Conectando..."):
                    user = gestionar_usuario_automatico(clave)
                    if user:
                        st.session_state.usuario_actual = user
                        st.rerun()
        st.write("---")
        st.markdown("**¿Necesitas respuestas hoy?**")
        st.link_button("💎 OBTENER PASE VIP", "https://mercadopago.com.ar")
    else:
        u = st.session_state.usuario_actual
        st.success(f"Bienvenida, Soberana.")
        
        # PERFIL VINCULAR (Se guarda en Base de Datos)
        with st.expander("⚙️ Perfil del Vínculo", expanded=True):
            st.caption("Ajusta estos datos para que el análisis sea exacto.")
            with st.form("perfil_form"):
                nom = st.text_input("Nombre:", value=u.get('nombre_el', ''))
                edad_val = int(u.get('edad', 30)) if pd.notna(u.get('edad', 30)) else 30
                edad = st.number_input("Edad (Clave para neurociencia):", min_value=13, max_value=90, value=edad_val)
                apego = st.selectbox("Apego:", ["No especificado", "Evitativo", "Ansioso", "Seguro"], index=0)
                historia = st.selectbox("Infancia/Trauma:", ["No especificado", "Padres Divorciados", "Padre Ausente", "Violencia", "Narcisismo"], index=0)
                
                if st.form_submit_button("💾 Guardar Datos"):
                    u['nombre_el'] = nom
                    u['edad'] = edad
                    u['apego'] = apego
                    u['historia'] = historia
                    if actualizar_perfil(u):
                        st.session_state.usuario_actual = u
                        st.toast("Perfil sincronizado con éxito.")
                        st.rerun()
            
        if st.button("Cerrar Sesión"):
            st.session_state.usuario_actual = None
            st.rerun()

# --- 7. PANTALLA PRINCIPAL ---
st.title("💎 Vínculo Nítido")

tab1, tab2, tab3 = st.tabs(["🧬 Test de Apego", "👁️ Verdad Oculta", "🔥 Laboratorio VIP"])

# --- TAB 1: TEST GRATIS ---
with tab1:
    st.header("Descubre su Patrón de Apego")
    st.write("Identifica su sistema operativo emocional:")
    with st.form("test"):
        r1 = st.radio("Ante la intimidad emocional, él:", ["Se aleja (Miedo)", "Se pone intenso (Ansiedad)", "Estable"])
        r2 = st.radio("Ante conflictos, él:", ["Huye / Silencio", "Explota / Culpa", "Dialoga"])
        if st.form_submit_button("VER RESULTADO"):
            st.divider()
            if "aleja" in r1 or "Huye" in r2:
                st.error("❄️ **Resultado: APEGO EVITATIVO**")
                st.write("Su cerebro asocia amor con pérdida de libertad. Se desactiva para protegerse.")
            elif "intenso" in r1 or "Explota" in r2:
                st.warning("🔥 **Resultado: APEGO ANSIOSO**")
                st.write("Su intensidad es terror al abandono.")
            else:
                st.success("✅ **Resultado: APEGO SEGURO**")

# --- TAB 2: GANCHO GRATIS ---
with tab2:
    st.subheader("¿Mensaje confuso?")
    msg = st.text_area("Pégalo aquí:", height=100)
    if st.button("ANALIZAR (GRATIS)"):
        if msg:
            prompt = f"Analiza este mensaje aplicando Psicología Masculina: '{msg}'. Dime qué significa realmente. NO DES CONSEJOS."
            with st.spinner("Procesando patrones..."):
                res = consultar_metodologia(prompt)
                st.markdown(f"<div class='result-box'><h4>👁️ La Verdad:</h4>{res}</div>", unsafe_allow_html=True)
                st.markdown("#### 👑 Estrategia Soberana (Bloqueada)")
                st.markdown("<div class='blur-text'>Para mantener tu valor, aplica el espejo invertido. Espera 4 horas y dile...</div>", unsafe_allow_html=True)
                st.warning("🔒 **Desbloquea la respuesta exacta en el VIP.**")

# --- TAB 3: VIP (FULL POWER) ---
with tab3:
    if st.session_state.usuario_actual is None:
        st.info("🔒 Ingresa tu pase a la izquierda para entrar.")
        st.stop()
        
    u = st.session_state.usuario_actual
    edad_sujeto = u.get('edad', 30)
    
    st.success(f"🔓 **Laboratorio Activado** | Analizando Sujeto de: {edad_sujeto} años.")
    
    chat = st.text_area("Pega la conversación completa (sin censura):", height=250)
    
    if st.button("✨ DECODIFICAR VÍNCULO"):
        if chat:
            with st.spinner("Aplicando Psicología de la Atracción y Neurociencia..."):
                historial = u.get('resumen_sesiones', '')
                
                # PROMPT VIP CON EDAD Y CERO CENSURA
                prompt = f"""
                ANÁLISIS DE CASO VIP:
                - Edad del sujeto: {edad_sujeto} años.
                - Estilo de Apego: {u.get('apego', 'No especificado')}.
                - Trauma de Infancia: {u.get('historia', 'No especificado')}.
                - Historial Previo: {historial}
                
                CHAT A ANALIZAR:
                "{chat}"
                
                Aplica la Metodología Soberana. Entrega 3 bloques exactos:
                
                1. 🧬 **NEUROCIENCIA Y PSICOLOGÍA MASCULINA:** Explica su comportamiento basado en su química cerebral (dopamina, adrenalina) y ajústalo estrictamente a su edad biológica ({edad_sujeto} años). Si hay contenido sexual, analízalo clínicamente.
                2. 👁️ **TRADUCCIÓN NÍTIDA:** Qué dice vs. Qué significa realmente.
                3. 👑 **ESTRATEGIA SOBERANA:** Qué debe hacer o responder la usuaria para mantener su alto valor.
                
                Al final, escribe en una línea nueva: "MEMORIA_DB: [Resumen de 10 palabras de esta interacción]"
                """
                
                res = consultar_metodologia(prompt)
                
                if "MEMORIA_DB:" in res:
                    partes = res.split("MEMORIA_DB:")
                    st.markdown(partes[0])
                    # Guardamos el resumen en la Base de Datos
                    memoria_nueva = partes[1].strip()
                    u['resumen_sesiones'] = f"{datetime.now().strftime('%d/%m')}: {memoria_nueva} | {historial}"[:4000]
                    actualizar_perfil(u)
                    st.toast("🧠 Memoria del vínculo actualizada.")
                else:
                    st.markdown(res)
