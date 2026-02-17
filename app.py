import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
import json
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Vínculo Nítido", page_icon="🦋", layout="centered")

# --- ESTILO VISUAL MÍSTICO ---
st.markdown("""
    <style>
    /* Fondo Degradado */
    .stApp {
        background: rgb(45,0,70);
        background: linear-gradient(160deg, rgba(45,0,70,1) 0%, rgba(20,0,40,1) 50%, rgba(0,0,20,1) 100%);
        color: #FFFFFF;
    }
    
    /* Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #1A0525;
    }

    /* Botones Dorados */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDC830 100%);
        color: #000000;
        border: none;
        border-radius: 25px;
        font-weight: bold;
        padding: 12px 24px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(212, 175, 55, 0.6);
    }

    /* Inputs (Gris Claro) */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        border-radius: 10px !important;
    }
    
    /* Títulos */
    h1 { color: #D4AF37 !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); }
    h3 { color: #E6E6FA !important; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A BASE DE DATOS (Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def cargar_datos_usuario(clave):
    """Busca si la usuaria ya existe en la hoja de cálculo."""
    try:
        df = conn.read(worksheet="vinculo_db", usecols=list(range(6)), ttl=0)
        usuario = df[df['usuario'] == clave]
        if not usuario.empty:
            return usuario.iloc[0].to_dict()
        return None
    except Exception as e:
        return None

def guardar_perfil_nuevo(datos):
    """Guarda un perfil nuevo o actualiza uno existente."""
    try:
        df = conn.read(worksheet="vinculo_db", usecols=list(range(6)), ttl=0)
        
        # Si ya existe, lo actualizamos
        if datos['usuario'] in df['usuario'].values:
            idx = df[df['usuario'] == datos['usuario']].index[0]
            for key, value in datos.items():
                df.at[idx, key] = value
        else:
            # Si es nuevo, lo agregamos
            nuevo_df = pd.DataFrame([datos])
            df = pd.concat([df, nuevo_df], ignore_index=True)
            
        conn.update(worksheet="vinculo_db", data=df)
        return True
    except Exception as e:
        st.error(f"Error guardando datos: {e}")
        return False

# --- MOTOR IA ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = ""

def obtener_modelo_valido(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            for modelo in datos.get('models', []):
                if 'generateContent' in modelo.get('supportedGenerationMethods', []):
                    if 'gemini' in modelo['name']: return modelo['name']
            return "models/gemini-pro"
        return None
    except: return None

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
        else: return f"Error: {response.text}"
    except Exception as e: return f"Error: {str(e)}"

# --- BARRA LATERAL: LOGIN Y PERFIL ---
with st.sidebar:
    st.markdown("""
        <center>
            <img src="https://images.unsplash.com/photo-1614726365723-49caaa563b7b?q=80&w=300&auto=format&fit=crop" width="150" style="border-radius: 50%; border: 3px solid #D4AF37; margin-bottom: 15px;">
            <h2 style='color: #D4AF37; margin-top:0;'>Zona Soberana</h2>
        </center>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 1. LOGIN
    clave_usuario = st.text_input("🔑 Tu Clave de Acceso:", type="password", help="Si no tenés una, inventá una para empezar.")
    
    usuario_data = None
    if clave_usuario:
        usuario_data = cargar_datos_usuario(clave_usuario)
        if usuario_data:
            st.success(f"Hola de nuevo, Soberana.")
        else:
            st.info("Clave nueva. Creando perfil...")

    # 2. DATOS DEL VÍNCULO (Se llenan solos si ya existen)
    st.markdown("### 📁 Expediente del Él")
    
    val_nombre = usuario_data['nombre_el'] if usuario_data else "Julio"
    # Convertir edad a int manejando posibles errores de conversión
    try:
        val_edad = int(usuario_data['edad']) if usuario_data and pd.notna(usuario_data['edad']) else 35
    except:
        val_edad = 35

    val_historia = usuario_data['historia'] if usuario_data else "No sé / Normal"
    val_orden = usuario_data['apego'] if usuario_data else "No sé" # Usamos la columna 'apego' para orden nacimiento por ahora
    
    with st.form("perfil_form"):
        nombre_el = st.text_input("Nombre:", value=val_nombre)
        edad_el = st.number_input("Edad:", min_value=15, max_value=90, value=val_edad)
        historia_familiar = st.selectbox("Historia Familiar / Trauma:", 
                                         ["No sé / Normal", "Padres Divorciados Conflictivos", "Padre Ausente", "Violencia / Adicciones"],
                                         index=["No sé / Normal", "Padres Divorciados Conflictivos", "Padre Ausente", "Violencia / Adicciones"].index(val_historia) if val_historia in ["No sé / Normal", "Padres Divorciados Conflictivos", "Padre Ausente", "Violencia / Adicciones"] else 0)
        orden_nacimiento = st.selectbox("Orden Nacimiento:", ["No sé", "Mayor (Responsable)", "Medio (Mediador)", "Menor (Mimado)"],
                                        index=["No sé", "Mayor (Responsable)", "Medio (Mediador)", "Menor (Mimado)"].index(val_orden) if val_orden in ["No sé", "Mayor (Responsable)", "Medio (Mediador)", "Menor (Mimado)"] else 0)
        
        if st.form_submit_button("💾 Guardar Expediente"):
            if clave_usuario:
                datos_nuevos = {
                    "usuario": clave_usuario,
                    "nombre_el": nombre_el,
                    "edad": edad_el,
                    "historia": historia_familiar,
                    "apego": orden_nacimiento, # Guardamos orden en columna apego para simplificar
                    "resumen_sesiones": usuario_data['resumen_sesiones'] if usuario_data else ""
                }
                if guardar_perfil_nuevo(datos_nuevos):
                    st.success("¡Datos guardados!")
                    st.rerun()
            else:
                st.error("Ingresá una clave primero.")

# --- INTERFAZ PRINCIPAL ---
st.title("💎 Vínculo Nítido")
st.markdown("### *Decodificando la mente masculina con ciencia*")
st.write("") 

if not clave_usuario:
    st.warning("👈 Por favor, ingresá tu Clave en la barra lateral para activar la IA.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🧠 Perfil Rápido", "🔬 Analizar Chat (VIP)", "👑 Consejera Real"])

# --- PESTAÑA 1 ---
with tab1:
    st.write(f"Sujeto: **{nombre_el} ({edad_el} años)** | Contexto: **{historia_familiar}**")
    perfil = st.radio("Conducta de hoy:", ["Se aleja (Evitativo)", "Bombardea (Intermitente)", "Solo sexual (Corto Plazo)", "Manipulación (Gaslighting)"])
    if st.button("Ver Diagnóstico"):
        st.success(f"Patrón: **{perfil}**.")
        st.info("La IA está lista para analizar el chat considerando su historial.")

# --- PESTAÑA 2 ---
with tab2:
    chat_texto = st.text_area("Chat de WhatsApp:", height=200, placeholder="Pegá aquí...")
    if st.button("✨ DECODIFICAR"):
        if chat_texto:
            with st.spinner(f"Analizando a {nombre_el} ({edad_el} años)..."):
                
                # Buscamos historial previo si existe
                historial_previo = usuario_data.get('resumen_sesiones', '') if usuario_data else ""
                
                prompt = f"""
                Actúa como 'Wanda Soberana' (Psicóloga Evolutiva y Experta en Relaciones).
                
                SUJETO: {nombre_el}, {edad_el} años.
                HISTORIA: {historia_familiar}, {orden_nacimiento}.
                HISTORIAL PREVIO: {historial_previo}
                
                CHAT A ANALIZAR: "{chat_texto}"
                
                Analiza en 4 puntos (Diagnóstico Nervioso, Estrategia Reproductiva, Traducción Real, Consejo Soberano).
                IMPORTANTE: Al final, dame un 'RESUMEN_PARA_DB' de 1 linea sobre este análisis para guardar en su historial.
                """
                resultado = consultar_ia_auto(prompt)
                
                # Separamos el resumen para guardar (truco de IA)
                partes = resultado.split("RESUMEN_PARA_DB")
                analisis_visible = partes[0]
                
                st.markdown(analisis_visible)
                
                # Guardado automático de memoria
                if len(partes) > 1:
                    nuevo_resumen = f"{datetime.now().strftime('%d/%m')}: {partes[1].strip()} | " + historial_previo[:500]
                    guardar_perfil_nuevo({
                        "usuario": clave_usuario, "nombre_el": nombre_el, "edad": edad_el,
                        "historia": historia_familiar, "apego": orden_nacimiento,
                        "resumen_sesiones": nuevo_resumen
                    })
                    st.toast("🧠 Memoria del vínculo actualizada.")

# --- PESTAÑA 3 ---
with tab3:
    consulta = st.text_area("Desahogate:", height=150)
    if st.button("💡 PEDIR ESTRATEGIA"):
        if consulta:
            with st.spinner("Pensando..."):
                prompt = f"""
                Mentora de Alto Valor.
                Usuaria lidiando con {nombre_el} ({edad_el}, {historia_familiar}).
                Ella dice: "{consulta}".
                Consejo duro pero amoroso.
                """
                resultado = consultar_ia_auto(prompt)
                st.markdown(resultado)
