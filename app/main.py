import streamlit as st
import sys
import os

# --- 1. CONFIGURACIÓN DEL PATH ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from src.models.inference import model_service
except ImportError:
    st.error("⚠️ No se encuentra el backend. Ejecuta desde la raíz.")
    st.stop()

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Retention AI | HR Analytics",
    page_icon="🧠",
    layout="wide"
)

# --- 3. TÍTULO ---
st.title("🧠 Retention AI: Predictor de Fuga de Talento")
st.markdown("""
Esta herramienta evalúa el riesgo de abandono basándose en factores demográficos y laborales.
Rellena el formulario a continuación:
""")
st.markdown("---")

# --- 4. FORMULARIO CENTRADO (SIN SIDEBAR) ---

# Usamos st.expander para agrupar y st.columns para aprovechar el ancho

# GRUPO A: DATOS PERSONALES
with st.expander("👤 1. Datos Personales y Educación", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("Edad", 18, 65, 30)
        marital = st.selectbox("Estado Civil", ["Single", "Married", "Divorced"])
    with col2:
        distance = st.slider("Distancia a Casa (km)", 1, 30, 5)
        education = st.select_slider("Nivel Educativo (1-5)", options=[1, 2, 3, 4, 5], value=3)
    with col3:
        edu_field = st.selectbox("Campo Educativo", 
            ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"])

# GRUPO B: DATOS LABORALES
with st.expander("💼 2. Datos Laborales", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        dept = st.selectbox("Departamento", ["Sales", "Research & Development", "Human Resources"])
        role = st.selectbox("Puesto (Job Role)", 
            ['Sales Executive', 'Research Scientist', 'Laboratory Technician', 
             'Manufacturing Director', 'Healthcare Representative', 'Manager', 
             'Sales Representative', 'Research Director', 'Human Resources'])
    with col2:
        level = st.slider("Job Level (1-5)", 1, 5, 2)
        travel = st.selectbox("Viajes de Negocio", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
    with col3:
        overtime = st.radio("¿Hace Horas Extra?", ["Yes", "No"], horizontal=True)

# GRUPO C: SATISFACCIÓN Y COMPENSACIÓN
with st.expander("❤️ 3. Satisfacción y Compensación", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        income = st.number_input("Salario Mensual ($)", min_value=1000, max_value=20000, value=5000, step=500)
        stock = st.select_slider("Nivel de Stock Options (0-3)", options=[0, 1, 2, 3], value=0)
    with col2:
        job_sat = st.slider("Satisfacción Trabajo (1-4)", 1, 4, 3)
        env_sat = st.slider("Satisfacción Ambiente (1-4)", 1, 4, 3)
    with col3:
        rel_sat = st.slider("Satisfacción Relaciones (1-4)", 1, 4, 3)
        involvement = st.slider("Involucración (1-4)", 1, 4, 3)
        wlb = st.slider("Work Life Balance (1-4)", 1, 4, 3)

# GRUPO D: ANTIGÜEDAD
with st.expander("⏳ 4. Antigüedad e Historial", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        years_at_co = st.number_input("Años en la Empresa", 0, 40, 5)
        companies = st.number_input("Empresas Anteriores", 0, 10, 1)
    with col2:
        years_role = st.number_input("Años en el Rol Actual", 0, 20, 2)
        training = st.slider("Formaciones año pasado", 0, 6, 2)
    with col3:
        years_manager = st.number_input("Años con el Mismo Jefe", 0, 20, 2)
    with col4:
        years_promo = st.number_input("Años desde última Promoción", 0, 20, 1)

# Preparación de datos (Feature Engineering simple)
total_satisfaction = env_sat + job_sat + rel_sat + involvement

input_data = {
    'Age': age, 'DistanceFromHome': distance, 'MonthlyIncome': income,
    'NumCompaniesWorked': companies, 'TrainingTimesLastYear': training,
    'YearsAtCompany': years_at_co, 'YearsSinceLastPromotion': years_promo,
    'YearsWithCurrManager': years_manager, 'EnvironmentSatisfaction': env_sat,
    'JobInvolvement': involvement, 'JobLevel': level, 'JobSatisfaction': job_sat,
    'RelationshipSatisfaction': rel_sat, 'WorkLifeBalance': wlb, 'Education': education,
    'BusinessTravel': travel, 'Department': dept, 'EducationField': edu_field,
    'JobRole': role, 'MaritalStatus': marital, 'OverTime': overtime,
    'StockOptionLevel': stock, 'TotalSatisfaction': total_satisfaction
}

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. ZONA DE PREDICCIÓN Y THRESHOLD ---

# Creamos dos columnas: Izquierda para el control, Derecha vacía (o para info)
c_control, c_info = st.columns([1, 1])

with c_control:
    st.subheader("⚙️ Configuración del Análisis")
    
    # Slider del Threshold
    threshold = st.slider(
        "Umbral de Riesgo (Threshold)", 
        0.0, 1.0, 0.50, 0.05,
        help="Si la probabilidad supera este valor, se marcará como Riesgo Alto."
    )
    
    # Botón de cálculo
    predict_btn = st.button("Calcular Riesgo", type="primary", use_container_width=True)


# --- 6. VISUALIZACIÓN DE RESULTADOS ---
st.markdown("---")

if predict_btn:
    with st.spinner('Analizando patrones con el modelo IA...'):
        try:
            # 1. Llamada al Modelo
            result = model_service.predict(input_data)
            prob = result['probability'] # Probabilidad pura (float)
            
            # 2. Aplicar el Threshold del Slider
            is_churn = prob >= threshold
            
            # 3. Mostrar Resultados
            col_res1, col_res2 = st.columns([1, 2])
            
            with col_res1:
                # Métrica Grande
                st.metric(
                    label="Probabilidad de Fuga Estimada", 
                    value=f"{prob:.1%}",
                    delta=f"Umbral: {threshold:.0%}",
                    delta_color="off"
                )
            
            with col_res2:
                # Caja de Estado (Colores nativos de Streamlit)
                if is_churn:
                    st.error(f"🚨 **ALERTA: RIESGO ALTO DE ABANDONO**")
                    st.markdown(f"La probabilidad ({prob:.1%}) supera el umbral configurado ({threshold:.1%}).")
                    st.warning("👉 **Acción:** Agendar reunión de retención y revisar condiciones salariales.")
                else:
                    st.success(f"✅ **ESTADO: EMPLEADO ESTABLE**")
                    st.markdown(f"La probabilidad ({prob:.1%}) está por debajo del umbral de riesgo ({threshold:.1%}).")
                    st.info("👍 **Acción:** Mantener plan de desarrollo actual.")
                    
        except Exception as e:
            st.error(f"Ocurrió un error en la predicción: {e}")