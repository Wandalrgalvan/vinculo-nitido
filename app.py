import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- 2. ESTILO VISUAL MÍSTICO Y ELEGANTE ---
st.markdown("""
    <style>
    /* Fondo Degradado Místico */
    .stApp {
        background: rgb(45,0,70);
        background: linear-gradient(160deg, rgba(45,0,70,1) 0%, rgba(20,0,40,1) 50%, rgba(0,0,20,1) 100%);
        color: #FFFFFF;
    }
    
    /* Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #1A0525;
    }
    
    /* Centrar elementos de la barra lateral */
    [data-testid="stSidebar"] > div:first-child {
        text-align: center;
    }

    /* Botones Dorados (CTA) */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDC830 100%);
        color: #000000;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        padding: 12px 24px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.6);
    }

    /* Inputs (Campos de texto más limpios) */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #F0F2F6 !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* Alertas y Títulos */
    h1 { color: #D4AF37 !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); }
    h2, h3 { color: #E6E6FA !important; }
    .stSuccess { background-color: rgba(0, 255, 0, 0.1) !important; color: white !important; }
    .stWarning { background-color: rgba(255, 255, 0, 0.1) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONEXIÓN A BASE DE DATOS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos_usuario(clave):
    """Busca si la usuaria ya existe en la hoja de cálculo."""
    try:
        # Leemos la hoja (asegurate que tu hoja se llame 'vinculo_db')
        df = conn.read(worksheet="vinculo_db", usecols=list(range(6)), ttl=0)
        # Convertimos la columna usuario a string para evitar errores
        df['usuario'] = df['usuario'].astype(str)
        usuario = df[df['usuario'] == str(clave)]
        
        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        return None
    except Exception as e:
        # Si falla (ej: hoja vacía), retornamos None sin romper la app
        return None

def guardar_perfil_nuevo(datos):
    """Guarda o actualiza el perfil."""
    try:
        df = conn.read(worksheet="vinculo_db", usecols=list(range(6)), ttl=0)
        df['usuario'] = df['usuario'].astype(str)
        
        if str(datos['usuario']) in df['usuario'].values:
            idx = df[df['usuario'] == str(datos['usuario'])].index[0]
            for key, value in datos.items():
                df.at[idx, key] = value
        else:
            nuevo_df = pd.DataFrame([datos])
            df = pd.concat([df, nuevo_df], ignore_index=True)
            
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- 4. MOTOR INTELIGENCIA ARTIFICIAL ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def consultar_ia(prompt):
    if not api_key: return "Error: Falta configurar la API Key."
    
    # URL directa para evitar problemas de librería
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error IA: {response.text}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- 5. BARRA LATERAL (LOGIN Y VENTAS) ---
with st.sidebar:
    # Imagen de silueta (URL estable de Wikimedia)
    st.markdown("""
        <center>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Woman_silhouette_standing.svg/418px-Woman_silhouette_standing.svg.png" width="120" style="filter: invert(1); margin-bottom: 10px;">
            <h2 style='color: #D4AF37; margin:0; font-size: 24px;'>Zona Soberana</h2>
        </center>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # SECCIÓN 1: LOGIN
    st.markdown("### 🔐 Acceso Clientas")
    clave_usuario = st.text_input("Ingresá tu Clave VIP:", type="password", placeholder="Ej: MARIA_01")
    
    usuario_data = None
    datos_cargados = False
    
    if clave_usuario:
        with st.spinner("Buscando tu expediente..."):
            usuario_data = cargar_datos_usuario(clave_usuario)
            if usuario_data:
                st.success(f"Bienvenida de nuevo.")
                datos_cargados = True
            else:
                st.info("Clave nueva detectada. Completá el perfil abajo para activarla.")

    # SECCIÓN 2: PERFIL DEL VÍNCULO (Solo si hay clave)
    if clave_usuario:
        st.markdown("### 📁 Expediente del Él")
        st.caption("Estos datos afinan la puntería de la IA.")
        
        # Valores por defecto (VACÍOS para no influir)
        val_nombre = usuario_data['nombre_el'] if usuario_data else ""
        val_edad = int(usuario_data['edad']) if usuario_data and pd.notna(usuario_data['edad']) else 0
        val_historia = usuario_data['historia'] if usuario_data else "Seleccionar..."
        val_apego = usuario_data['apego'] if usuario_data else "Seleccionar..."
        
        with st.form("perfil_form"):
            nombre_el = st.text_input("Nombre de él:", value=val_nombre, placeholder="Ej: Juan")
            edad_el = st.number_input("Edad:", min_value=15, max_value=80, value=val_edad if val_edad > 0 else 30)
            
            # Opciones separadas como pediste
            historia_familiar = st.selectbox("Historia / Trauma:", 
                                             ["Seleccionar...", 
                                              "Ninguno aparente",
                                              "Padres Divorciados Conflictivos",
                                              "Padre Ausente / Abandono",
                                              "Madre Narcisista / Sobreprotectora",
                                              "Entorno de Violencia",
                                              "Historia de Adicciones",
                                              "Duelos no resueltos"],
                                             index=0 if val_historia == "Seleccionar..." else None)
            
            apego_detectado = st.selectbox("Estilo de Apego (si sabés):", 
                                           ["Seleccionar...", "Evitativo (Se aleja)", "Ansioso (Persigue)", "Seguro", "Desorganizado (Caótico)"],
                                           index=0 if val_apego == "Seleccionar..." else None)
            
            if st.form_submit_button("💾 Guardar / Actualizar"):
                datos_nuevos = {
                    "usuario": clave_usuario,
                    "nombre_el": nombre_el,
                    "edad": edad_el,
                    "historia": historia_familiar,
                    "apego": apego_detectado,
                    "resumen_sesiones": usuario_data['resumen_sesiones'] if usuario_data else ""
                }
                guardar_perfil_nuevo(datos_nuevos)
                st.toast("¡Expediente actualizado con éxito!")
                st.rerun()

    # SECCIÓN 3: VENTA (Si no hay clave o para renovar)
    st.write("---")
    st.markdown("### ¿Aún no sos VIP?")
    st.write("Desbloqueá el análisis profundo y la consejera 24/7.")
    # ACÁ VA TU LINK DE MERCADOPAGO REAL
    st.link_button("💎 Comprar Pase VIP", "https://link_de_mercadopago_aqui.com")

# --- 6. INTERFAZ PRINCIPAL ---
st.title("💎 Vínculo Nítido")
st.markdown("### *Decodificando la mente masculina con ciencia*")
st.write("") 

# TABS: La primera es GRATIS, las otras son VIP
tab1, tab2, tab3 = st.tabs(["🕵️‍♀️ Test Gratuito", "🔬 Analizar Chat (VIP)", "👑 Consejera (VIP)"])

# --- PESTAÑA 1: GRATIS (El Gancho) ---
with tab1:
    st.write("### Diagnóstico Rápido de Conducta")
    st.write("Descubrí qué patrón oculto está operando hoy. (No requiere clave).")
    
    conducta = st.radio("¿Qué hizo él últimamente?", 
                      ["Se aleja cuando hay intimidad emocional", 
                       "Te llena de mensajes y luego desaparece días", 
                       "Solo escribe de madrugada o para sexo",
                       "Te hace sentir culpable de sus errores"])
    
    if st.button("Ver Diagnóstico Preliminar"):
        st.divider()
        if "aleja" in conducta:
            st.error("🚨 **Patrón Detectado: APEGO EVITATIVO.**")
            st.write("Su cerebro percibe tu amor como una amenaza a su libertad. No es que no te quiera, es que tiene miedo.")
        elif "llena" in conducta:
            st.error("🎰 **Patrón Detectado: REFUERZO INTERMITENTE.**")
            st.write("Es la técnica más adictiva que existe (como las máquinas tragamonedas). Te da migajas para mantenerte enganchada.")
        elif "madrugada" in conducta:
            st.error("🦊 **Patrón Detectado: ESTRATEGIA DE CORTO PLAZO.**")
            st.write("Biológicamente, está buscando acceso reproductivo a bajo costo de inversión. Cuidado.")
        else:
            st.error("🐍 **Patrón Detectado: GASLIGHTING / MANIPULACIÓN.**")
            st.write("Está distorsionando tu realidad para que dudes de tu propia cordura. Es peligroso.")
            
        # EL GANCHO DE VENTA
        st.info("💡 **¿Querés saber si miente? ¿Querés saber qué contestarle para recuperar tu poder?**")
        st.markdown("👉 **Ingresá tu Clave VIP en el menú** o comprá tu pase para analizar sus chats reales.")

# --- PESTAÑA 2: VIP (Bloqueada sin clave) ---
with tab2:
    if not clave_usuario or not datos_cargados:
        st.warning("🔒 **Contenido Bloqueado.**")
        st.write("Para usar el Laboratorio de Análisis, ingresá tu Clave VIP en la barra lateral.")
        st.stop()
    
    st.success(f"🔓 **Modo VIP Activado.** Analizando a: {nombre_el} ({edad_el} años).")
    
    chat_texto = st.text_area("Pegá la conversación completa:", height=200, placeholder="Él: Hola perdida...\nYo: ...")
    
    if st.button("✨ DECODIFICAR MENTE MASCULINA"):
        if chat_texto and nombre_el:
            with st.spinner("La IA está cruzando datos psicológicos..."):
                historial = usuario_data.get('resumen_sesiones', '')
                
                prompt = f"""
                Actúa como 'Wanda Soberana' (Psicóloga Evolutiva).
                
                PERFIL DEL SUJETO:
                - Nombre: {nombre_el}
                - Edad: {edad_el}
                - Trauma/Historia: {historia_familiar}
                - Apego: {apego_detectado}
                - Historial previo: {historial}
                
                CHAT A ANALIZAR: "{chat_texto}"
                
                Dame un análisis crudo y directo en 4 pasos:
                1. Diagnóstico Nervioso (Dopamina/Cortisol).
                2. Estrategia Reproductiva (¿Qué busca?).
                3. Traducción Real (¿Qué significan sus palabras?).
                4. Consejo Soberano (Acción concreta).
                
                AL FINAL, escribe: "RESUMEN_DB: [Una frase resumen de lo que pasó hoy para guardar en memoria]".
                """
                resultado = consultar_ia(prompt)
                
                # Separar el resumen para guardar
                if "RESUMEN_DB:" in resultado:
                    partes = resultado.split("RESUMEN_DB:")
                    texto_visible = partes[0]
                    resumen_nuevo = partes[1].strip()
                    
                    # Guardar en base de datos
                    nuevo_historial = f"{datetime.now().strftime('%d/%m')}: {resumen_nuevo} | " + historial[:500]
                    guardar_perfil_nuevo({
                        "usuario": clave_usuario, 
                        "nombre_el": nombre_el, "edad": edad_el, "historia": historia_familiar, 
                        "apego": apego_detectado, "resumen_sesiones": nuevo_historial
                    })
                else:
                    texto_visible = resultado
                
                st.markdown(texto_visible)
        else:
            st.warning("Faltan datos. Asegurate de completar el expediente de él en la barra lateral.")

# --- PESTAÑA 3: CONSEJERA (Bloqueada sin clave) ---
with tab3:
    if not clave_usuario or not datos_cargados:
        st.warning("🔒 **Consejera Privada Bloqueada.**")
        st.write("Necesitás un pase VIP para hablar con la mentora.")
        st.stop()
        
    st.write("¿Qué sentís hoy? Desahogate sin filtro.")
    consulta = st.text_area("Tu mensaje:", height=150)
    
    if st.button("💡 PEDIR ESTRATEGIA"):
        if consulta:
            with st.spinner("Conectando con tu Mentora..."):
                prompt = f"""
                Sos una Mentora de Alto Valor.
                La usuaria ({clave_usuario}) está lidiando con {nombre_el} ({historia_familiar}).
                Ella dice: "{consulta}".
                
                Dame un consejo empoderador, estratégico y digno.
                """
                st.markdown(consultar_ia(prompt))
