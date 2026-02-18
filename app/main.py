import streamlit as st
import sys
import os
import pandas as pd
import altair as alt

# --- 1. CONFIGURACIÓN DEL PATH ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from src.models.inference import model_service
except ImportError:
    st.error("⚠️ Backend not found. Please run from root.")
    st.stop()

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Retention AI",
    page_icon="🧠",
    layout="wide"
)

# --- 3. GESTIÓN DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

def navigate_to(page):
    st.session_state['page'] = page

# --- 4. CSS GENERAL ---
st.markdown("""
<style>
    /* Fondo general */
    .stApp { background-color: #f8f9fa; }
    
    /* Ocultar flecha del Delta */
    [data-testid="stMetricDelta"] svg { display: none; }
    [data-testid="stMetricDelta"] > div { margin-left: 0 !important; }

    /* Estilo base para botones pequeños de navegación */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# PÁGINA 1: HOME (TARJETAS CLICKABLES CON ESTILO AVANZADO)
# ==============================================================================
if st.session_state['page'] == 'home':
    
    st.markdown("""
    <style>
        /* CSS MÁGICO PARA LAS TARJETAS */
        div.stButton > button {
            height: 240px;
            width: 100%;
            background-color: white !important;
            color: #4b5563 !important;      /* Color base (descripción): Gris medio */
            border: 1px solid #e5e7eb !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
            
            /* TRUCO: Display block permite usar ::first-line */
            display: block !important; 
            white-space: pre-wrap !important; /* Respeta los saltos de línea */
            
            font-size: 1rem !important;      /* Tamaño letra pequeña */
            padding-top: 0px !important;    /* Ajuste para centrar visualmente */
            
            transition: all 0.2s ease-in-out;
        }

        /* ESTILO PARA EL TÍTULO Y EMOJI (La primera línea) */
        div.stButton > button p::first-line {
            font-size: 1.8rem !important;    /* TÍTULO GRANDE */
            font-weight: 900 !important;     /* NEGRITA FUERTE */
            color: #1f2937 !important;       /* Color casi negro */
            line-height: 2.5 !important;     /* Separación con el texto de abajo */
        }
        
        /* HOVER: Elevación */
        div.stButton > button:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px rgba(0,0,0,0.1) !important;
            border-color: #005bea !important;
            
            /* Mantenemos colores fijos para que no se ponga rojo/azul */
            background-color: white !important;
            color: #4b5563 !important;
        }
        /* Hover también mantiene el título negro */
        div.stButton > button:hover p::first-line {
            color: #1f2937 !important;
        }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #111827; margin-bottom: 40px;'>🧬 Retention AI</h1>", unsafe_allow_html=True)
    
    col_spacer_l, col_manual, col_batch, col_spacer_r = st.columns([1, 4, 4, 1])
    
    with col_manual:
        # Ponemos Emoji y Título en la MISMA LÍNEA para que el CSS ::first-line los coja a los dos
        txt_manual = "👤 INDIVIDUAL ANALYSIS\nAnalyze a single employee profile manually.\nBest for 1-on-1 reviews."
        if st.button(txt_manual, use_container_width=True):
            navigate_to('manual')
            st.rerun()

    with col_batch:
        txt_batch = "📂 BATCH ANALYSIS\nUpload a CSV/Excel file.\nProcess hundreds of employees at once."
        if st.button(txt_batch, use_container_width=True):
            navigate_to('batch')
            st.rerun()


# ==============================================================================
# PÁGINA 2: MANUAL ANALYSIS
# ==============================================================================
elif st.session_state['page'] == 'manual':
    if st.button("← Back to Home"):
        navigate_to('home')
        st.rerun()

    st.title("👤 Individual Employee Analysis")
    st.markdown("""
    This tool evaluates churn risk based on demographic and labor factors.
    Fill out the form below:
    """)
    st.markdown("---")

    # --- FORMULARIO ---
    with st.expander("👤 1. Personal Data & Education", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider("Age", 18, 65, 30)
            marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        with col2:
            distance = st.slider("Distance from Home (km)", 1, 30, 5)
            education = st.select_slider("Education Level (1-5)", options=[1, 2, 3, 4, 5], value=3)
        with col3:
            edu_field = st.selectbox("Education Field", 
                ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"])

    with st.expander("💼 2. Job Details", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            dept = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
            role = st.selectbox("Job Role", 
                ['Sales Executive', 'Research Scientist', 'Laboratory Technician', 
                 'Manufacturing Director', 'Healthcare Representative', 'Manager', 
                 'Sales Representative', 'Research Director', 'Human Resources'])
        with col2:
            level = st.slider("Job Level (1-5)", 1, 5, 2)
            travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
        with col3:
            overtime = st.radio("OverTime?", ["Yes", "No"], horizontal=True)

    with st.expander("❤️ 3. Satisfaction & Compensation", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            income = st.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000, step=500)
            stock = st.select_slider("Stock Options Level (0-3)", options=[0, 1, 2, 3], value=0)
        with col2:
            job_sat = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
            env_sat = st.slider("Environment Satisfaction (1-4)", 1, 4, 3)
        with col3:
            rel_sat = st.slider("Relationship Satisfaction (1-4)", 1, 4, 3)
            involvement = st.slider("Job Involvement (1-4)", 1, 4, 3)
            wlb = st.slider("Work Life Balance (1-4)", 1, 4, 3)

    with st.expander("⏳ 4. Tenure & History", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            years_at_co = st.number_input("Years at Company", 0, 40, 5)
            companies = st.number_input("Num Companies Worked", 0, 10, 1)
        with col2:
            years_role = st.number_input("Years in Current Role", 0, 20, 2)
            training = st.slider("Training Times Last Year", 0, 6, 2)
        with col3:
            years_manager = st.number_input("Years with Curr Manager", 0, 20, 2)
        with col4:
            years_promo = st.number_input("Years Since Last Promo", 0, 20, 1)

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

    # --- PREDICCIÓN ---
    c_control, c_info = st.columns([1, 1])

    with c_control:
        st.subheader("⚙️ Analysis Configuration")
        threshold = st.slider("Risk Threshold", 0.0, 1.0, 0.50, 0.05)
        predict_btn = st.button("Calculate Risk", type="primary", use_container_width=True)

    st.markdown("---")

    if predict_btn:
        with st.spinner('Analyzing patterns with AI model...'):
            try:
                result = model_service.predict(input_data)
                prob = result['probability']
                is_churn = prob >= threshold
                
                col_res1, col_res2 = st.columns([1, 2])
                
                with col_res1:
                    st.metric("Estimated Churn Probability", f"{prob:.1%}", delta=f"Threshold: {threshold:.0%}", delta_color="off")
                
                with col_res2:
                    if is_churn:
                        st.error(f"🚨 **ALERT: HIGH CHURN RISK**")
                        st.markdown(f"Probability ({prob:.1%}) exceeds the configured threshold ({threshold:.1%}).")
                        st.warning("👉 **Action:** Schedule retention meeting.")
                    else:
                        st.success(f"✅ **STATUS: STABLE EMPLOYEE**")
                        st.markdown(f"Probability ({prob:.1%}) is below the risk threshold ({threshold:.1%}).")
                        st.info("👍 **Action:** Maintain current development plan.")
                        
            except Exception as e:
                st.error(f"Prediction Error: {e}")
                
            # --- XAI ---
            st.markdown("---")
            st.subheader("🔍 Why this result?")
            st.write("Factors influencing this specific decision:")

            df_imp = model_service.get_feature_importance()
            
            if not df_imp.empty:
                def clean_names(name):
                    name = name.replace('num__', '').replace('cat__', '').replace('remainder__', '')
                    translations = {
                        'TotalSatisfaction': 'Total Sat.', 'StockOptionLevel': 'Stock Options',
                        'OverTime_Yes': 'OverTime (Yes)', 'OverTime_No': 'OverTime (No)',
                        'MonthlyIncome': 'Salary', 'Age': 'Age', 'YearsAtCompany': 'Years at Company',
                        'YearsWithCurrManager': 'Years w/ Manager', 'DistanceFromHome': 'Distance',
                        'EnvironmentSatisfaction': 'Env. Sat.', 'JobSatisfaction': 'Job Sat.',
                        'WorkLifeBalance': 'Work Life Balance', 'JobInvolvement': 'Job Involvement',
                        'NumCompaniesWorked': 'Num Companies', 'Log_MonthlyIncome': 'Log Salary',
                        'BusinessTravel_Travel_Frequently': 'Travel Freq.', 'JobRole_Laboratory Technician': 'Lab Tech',
                        'StockOptionLevel_0': 'No Stocks', 'BusinessTravel_Non-Travel': 'Non-Travel',
                        'YearsSinceLastPromotion': 'Years Since Promo'
                    }
                    return translations.get(name, name)

                df_imp['Variable'] = df_imp['Variable'].apply(clean_names)
                df_imp['Tipo'] = df_imp['Peso'].apply(lambda x: 'Increases Risk 🚨' if x > 0 else 'Protects (Retains) 🛡️')
                df_imp['Color'] = df_imp['Peso'].apply(lambda x: '#ff4b4b' if x > 0 else '#22c55e')
                
                # REINTRODUCIMOS LA ORDENACIÓN POR MAGNITUD ABSOLUTA
                df_imp['AbsPeso'] = df_imp['Peso'].abs()
                df_imp = df_imp.sort_values(by='AbsPeso', ascending=False)

                top_5 = df_imp.head(5)
                orden_visual = top_5["Variable"].to_list()
                
                base = alt.Chart(top_5).encode(
                    x=alt.X('Peso', title='Impact on Prediction'),
                    y=alt.Y('Variable', sort=orden_visual, title=None),
                    color=alt.Color('Tipo', scale=alt.Scale(domain=['Increases Risk 🚨', 'Protects (Retains) 🛡️'], range=['#ff4b4b', '#22c55e']), legend=alt.Legend(title="Effect", orient="bottom")),
                    tooltip=[alt.Tooltip('Variable', title='Factor'), alt.Tooltip('Peso', format='.2f', title='Weight')]
                )
                
                chart = base.mark_bar()
                st.altair_chart(chart, use_container_width=True)

                with st.expander("View all factors (Full Detail)"):
                    rest_df = df_imp.iloc[5:]
                    if not rest_df.empty:
                        orden_visual_2 = rest_df["Variable"].to_list()
                        base_rest = alt.Chart(rest_df).encode(
                            x=alt.X('Peso', title='Impact on Prediction'),
                            y=alt.Y('Variable', sort=orden_visual_2, title=None),
                            color=alt.Color('Tipo', scale=alt.Scale(domain=['Increases Risk 🚨', 'Protects (Retains) 🛡️'], range=['#ff4b4b', '#22c55e']), legend=None),
                            tooltip=[alt.Tooltip('Variable', title='Factor'), alt.Tooltip('Peso', format='.2f', title='Weight')]
                        )
                        chart_rest = base_rest.mark_bar()
                        st.altair_chart(chart_rest, use_container_width=True)
                    else:
                        st.write("No more relevant variables.")
            else:
                st.warning("⚠️ Could not extract feature importance.")

# ==============================================================================
# PÁGINA 3: BATCH ANALYSIS
# ==============================================================================
elif st.session_state['page'] == 'batch':
    if st.button("← Back to Home"):
        navigate_to('home')
        st.rerun()

    st.title("📂 Batch Employee Analysis")
    st.markdown("""
    Upload a **CSV** or **Excel** file containing employee data. 
    The AI will predict churn risk for the entire list instantly.
    """)
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Drop your file here", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.write(f"**Loaded {len(df)} employees.** Preview:")
            st.dataframe(df.head(3))
            
            batch_threshold = st.slider("Risk Filter Threshold", 0.0, 1.0, 0.50, 0.05)
            
            if st.button("Run Batch Prediction", type="primary"):
                with st.spinner("Processing all rows..."):
                    
                    sat_cols = ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction', 'JobInvolvement']
                    if all(col in df.columns for col in sat_cols) and 'TotalSatisfaction' not in df.columns:
                        df['TotalSatisfaction'] = df[sat_cols].sum(axis=1)
                    
                    results_df = model_service.predict_batch(df)
                    high_risk_df = results_df[results_df['Churn_Probability'] >= batch_threshold].sort_values(by='Churn_Probability', ascending=False)
                    
                    st.markdown("---")
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        st.metric("Total Employees", len(results_df))
                    with col_m2:
                        st.metric("High Risk Detected", len(high_risk_df), delta="Action Needed", delta_color="inverse")
                    
                    st.subheader("🔥 Top At-Risk Employees")
                    
                    if not high_risk_df.empty:
                        cols_possible = ['EmployeeNumber', 'Department', 'JobRole', 'Age', 'MonthlyIncome']
                        cols_to_show = ['Churn_Probability'] + [c for c in df.columns if c in cols_possible]
                        
                        st.dataframe(high_risk_df[cols_to_show].style.background_gradient(subset=['Churn_Probability'], cmap='Reds'), use_container_width=True)
                        
                        csv = high_risk_df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download High Risk Report (CSV)", csv, 'high_risk_employees.csv', 'text/csv')
                    else:
                        st.success("Great news! No employees exceeded the risk threshold.")
                        
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.warning("Ensure your file columns match the training data format.")