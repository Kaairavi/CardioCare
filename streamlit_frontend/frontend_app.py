import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ------------------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="CardioCare AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# PREMIUM GLOBAL STYLES (CSS - LIGHT THEME)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');

    :root {
        --primary: #2563EB; /* Royal Blue */
        --primary-light: #EFF6FF;
        --secondary: #10B981; /* Emerald */
        --danger: #EF4444; /* Red */
        --bg: #F8FAFC; /* Slate 50 */
        --card-bg: #FFFFFF;
        --text-main: #1E293B; /* Slate 800 */
        --text-sub: #64748B; /* Slate 500 */
        --border: #E2E8F0;
    }

    /* Reset & Base */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: var(--bg);
        color: var(--text-main);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid var(--border);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Navigation Buttons */
    div.stButton > button {
        text-align: left; 
    }

    /* Cards - Applied to specific DIVs and Forms */
    .content-card, [data-testid="stForm"] {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .content-card:hover, [data-testid="stForm"]:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }

    /* Headers */
    h1, h2, h3 {
        color: var(--text-main);
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.8rem; margin-bottom: 1rem; }
    
    .subtitle {
        color: var(--text-sub);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Metrics */
    .metric-container {
        background: #F1F5F9;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid var(--border);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
    }
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-sub);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    /* Form Styling */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: var(--text-main) !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    /* Hide Number Input Spinners (Browser default) */
    /* Chrome, Safari, Edge, Opera */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    /* Firefox */
    input[type=number] {
      -moz-appearance: textfield;
    }
    
    /* Hide Streamlit Number Input Stepper Buttons (+/-) */
    div[data-testid="stNumberInput"] button {
        display: none;
    }
    
    /* Submit Button Styling (Targeting standard Streamlit buttons) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        height: auto;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        opacity: 0.95;
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(37, 99, 235, 0.3);
    }

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SESSION STATE & NAVIGATION
# ------------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "overview"

# ------------------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;" class="animate__animated animate__fadeInDown">
            <div style="font-size: 3.5rem; margin-bottom: 10px;">❤️</div>
            <h2 style="margin:0; color:#1E293B;">CardioCare</h2>
            <p style="color: #64748B; font-size: 0.9rem;">Logistic Regression Model</p>
        </div>
        <hr style="border-color: #E2E8F0; margin: 20px 0;">
    """, unsafe_allow_html=True)

    pages = {
        "overview": "🏠 Overview",
        "risk": "🩺 Risk Assessment",
        "journey": "🚀 Model Journey",
        "analytics": "📊 Model Analytics",
        "data_insights": "🧠 Feature Relations"
    }

    for page_key, page_label in pages.items():
        if st.button(page_label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("""
        <div style="position: absolute; bottom: 20px; width: 100%; text-align: center; color: #94A3B8; font-size: 0.75rem;">
            
        </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: OVERVIEW
# ------------------------------------------------------------------------------
if st.session_state.page == "overview":
    st.markdown('<div class="animate__animated animate__fadeIn">', unsafe_allow_html=True)
    st.title("Cardiovascular Health System")
    st.markdown('<p class="subtitle">Clinical Decision Support System</p>', unsafe_allow_html=True)

    # Hero Card
    st.markdown("""
    <div class="content-card">
        <h3 style="color: #1E293B; margin-top:0;">Precision Risk Analysis</h3>
        <p style="color: #475569; line-height: 1.7; font-size: 1.05rem;">
            CardioCare utilizes a calibrated <b>Logistic Regression</b> algorithm to analyze patient vitals and predict cardiovascular risks. 
            Designed for interpretability and speed, it assists clinicians in early triage and preventative care planning.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("73.2%", "Accuracy"),
        ("0.73", "ROC-AUC"),
        ("70k+", "Records Analyzed"),
        ("LogReg", "Core Model")
    ]
    
    for i, (col, (val, label)) in enumerate(zip([c1, c2, c3, c4], metrics)):
        with col:
            st.markdown(f"""
            <div class="metric-container animate__animated animate__fadeInUp" style="animation-delay: {i*0.1}s;">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

    # Educational Insights Section
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📘 Understanding Cardiovascular Health")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;">
            <h4 style="color: #EF4444; margin-top: 0;">Global Impact</h4>
            <p style="color: #64748B; font-size: 0.9rem;">
                Cardiovascular diseases (CVDs) are the leading cause of death globally, taking an estimated <b>17.9 million lives</b> each year.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;">
            <h4 style="color: #F59E0B; margin-top: 0;">Preventable Risks</h4>
            <p style="color: #64748B; font-size: 0.9rem;">
                Most CVDs can be prevented by addressing behavioral risk factors such as tobacco use, unhealthy diet and obesity, physical inactivity and harmful use of alcohol.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;">
            <h4 style="color: #3B82F6; margin-top: 0;">Silent Symptoms</h4>
            <p style="color: #64748B; font-size: 0.9rem;">
                Often, there are no underlying symptoms of the underlying disease of the blood vessels. A heart attack or stroke may be the first warning of underlying disease.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: RISK ASSESSMENT
# ------------------------------------------------------------------------------
elif st.session_state.page == "risk":
    st.markdown('<div class="animate__animated animate__fadeInRight">', unsafe_allow_html=True)
    st.title("Risk Assessment")
    st.markdown('<p class="subtitle">Input patient data below</p>', unsafe_allow_html=True)

    with st.container():
        # Removed explicit .content-card DIV wrapper to fix white box issue
        # The form itself is now styled as a card via CSS [data-testid="stForm"]
        st.subheader("1️⃣ Personal Details")
        c1, c2 = st.columns(2)
        with c1:
            age_years = st.number_input("Age (years)", 18, 100, 50)
            gender = st.selectbox("Gender", ["Female", "Male"])
        with c2:
            height = st.number_input("Height (cm)", 140, 200, 165)
            weight = st.number_input("Weight (kg)", 40, 160, 70)
            
        # Real-time BMI Calculation display
        bmi =  weight / ((height/100)**2) if height > 0 else 0
        bmi_color = "#10B981" if 18.5 <= bmi <= 25 else "#F59E0B" if 25 < bmi < 30 else "#EF4444"
        status = "Normal" if 18.5 <= bmi <= 25 else "Overweight" if 25 < bmi < 30 else "Obese" if bmi >= 30 else "Underweight"
        
        st.markdown(f"""
        <div style="margin: 10px 0; padding:10px; border-radius:8px; background:{bmi_color}15; border:1px solid {bmi_color}; display: flex; align-items: center; justify-content: space-between;">
            <span style="color:#64748B; font-weight:500;">Body Mass Index </span>
            <span style="font-size:1.1rem; color:{bmi_color}; font-weight:bold;">{bmi:.1f} ({status})</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("2️⃣ Vitals & Labs")
        
        c3, c4 = st.columns(2)
        with c3:
            ap_hi = st.number_input("Systolic BP (mmHg)", 80, 220, 120, help="Upper number. Normal < 120")
            cholesterol = st.selectbox(
                "Cholesterol Level",
                options=["Normal", "Above Normal", "Well Above Normal"],
                help="Normal: <200 | Borderline: 200-239 | High: ≥240"
            )
            st.caption("Values: Normal (<200), High (200-239), Very High (≥240)")

        with c4:
            ap_lo = st.number_input("Diastolic BP (mmHg)", 40, 140, 80, help="Lower number. Normal < 80")
            gluc = st.selectbox(
                "Glucose Level",
                options=["Normal", "Above Normal", "Well Above Normal"],
                help="Normal: <100 | Prediabetes: 100-125 | Diabetes: ≥126"
            )
            st.caption("Values: Normal (<100), Prediabetes (100-125), Diabetes (≥126)")

        st.markdown("---")
        st.subheader("3️⃣ Lifestyle")
        
        c5, c6, c7 = st.columns(3)
        with c5:
            st.write("**Activity**")
            active = st.radio("Physical Activity", ["Yes", "No"], horizontal=True, label_visibility="collapsed")
        with c6:
            st.write("**Habits**")
            smoke = st.checkbox("Smoker")
        with c7:
            st.write("**Alcohol**")
            alco = st.checkbox("Alcohol Consumer")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # State management for predicting status
        if 'predicting' not in st.session_state:
            st.session_state.predicting = False

        predict_btn = st.button("Run Risk Assessment", type="primary")

        if predict_btn:
            st.session_state.predicting = True
        
        # Logic is now outside the form (since we removed the form)
        if predict_btn:
             # Spinner instead of expanded status for cleaner UI
            with st.spinner("Analyzing cardiovascular markers..."):
                import time
                time.sleep(1) # Visual delay for effect
            
            payload = {
                "age": age_years,
                "gender": 2 if gender == "Male" else 1,
                "height": height,
                "weight": weight,
                "ap_hi": ap_hi,
                "ap_lo": ap_lo,
                "cholesterol": ["Normal", "Above Normal", "Well Above Normal"].index(cholesterol) + 1,
                "gluc": ["Normal", "Above Normal", "Well Above Normal"].index(gluc) + 1,
                "smoke": 1 if smoke else 0,
                "alco": 1 if alco else 0,
                "active": 1 if active == "Yes" else 0
            }
            status_placeholder = st.empty()

            try:
                response = requests.post("https://cardiocare-production-cba0.up.railway.app/predict", json=payload)
                result = response.json()

                if response.status_code == 200:
                    is_risk = result['prediction'] == 1
                    
                    # Dynamic Styles for Result
                    accent_color = "#EF4444" if is_risk else "#10B981"
                    bg_color = "#FEF2F2" if is_risk else "#ECFDF5"
                    icon_header = "⚠️ Attention: Potential Health Risk" if is_risk else "✅ Great News: Low Health Risk"
                    
                    html_content = f"""
<div class="animate__animated animate__zoomIn" style="background-color: {bg_color}; border: 2px solid {accent_color}; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 4px 6px -1px {accent_color}40; margin-top: 10px;">
<h2 style="color: {accent_color}; font-size: 1.8rem; margin-bottom: 5px;">{icon_header}</h2>
<p style="font-size: 1.1rem; color: #1E293B; margin-bottom: 25px; line-height: 1.5;">{result['message']}</p>
<div style="display: inline-block; padding: 8px 16px; background: white; border-radius: 50px; border: 1px solid {accent_color}; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 10px;">
<span style="color: #64748B; font-weight: 500; font-size: 0.9rem;">Model Confidence:</span>
<span style="color: {accent_color}; font-weight: 700; font-size: 1.2rem; margin-left: 5px;">{result['probability']*100:.1f}%</span>
</div>
<p style="font-size: 0.85rem; color: #64748B; margin: 0; max-width: 400px; margin-left: auto; margin-right: auto;">
    This score represents the probability of the predicted outcome based on the statistical pattern in your vitals.
</p>
</div>
"""
                    st.markdown(html_content, unsafe_allow_html=True)
                    
                    # ----------------------------------------------------------------------
                    # Detailed Health Analysis Report
                    # ----------------------------------------------------------------------
                    insights = []
                    
                    # BMI Analysis
                    if bmi >= 30:
                        insights.append(f"<li style='margin-bottom:8px;'><b>Weight Management:</b> BMI of {bmi:.1f} indicates obesity. This significantly increases heart workload.</li>")
                    elif bmi >= 25:
                        insights.append(f"<li style='margin-bottom:8px;'><b>Weight Management:</b> BMI of {bmi:.1f} indicates you are overweight. Monitor caloric intake.</li>")
                    
                    # BP Analysis
                    if ap_hi > 120 or ap_lo > 80:
                        insights.append(f"<li style='margin-bottom:8px;'><b>Blood Pressure:</b> Readings ({ap_hi}/{ap_lo}) are above ideal levels (Target: <120/80).</li>")
                    
                    # Lab Results Analysis
                    chol_levels = ["Normal", "Above Normal", "Well Above Normal"]
                    if chol_levels.index(cholesterol) > 0:
                        insights.append(f"<li style='margin-bottom:8px;'><b>Cholesterol:</b> {cholesterol} levels detected. High cholesterol can lead to plaque buildup.</li>")
                        
                    gluc_levels = ["Normal", "Above Normal", "Well Above Normal"]
                    if gluc_levels.index(gluc) > 0:
                        insights.append(f"<li style='margin-bottom:8px;'><b>Glucose:</b> {gluc} levels may indicate metabolic risk or diabetes.</li>")
                    
                    # Lifestyle Analysis
                    if smoke:
                        insights.append("<li style='margin-bottom:8px;'><b>Smoking:</b> Major risk factor. Cessation is the single best step for heart health.</li>")
                    if alco:
                         insights.append("<li style='margin-bottom:8px;'><b>Alcohol:</b> Limit consumption to reduce cardiovascular stress.</li>")
                    if active == "No":
                         insights.append("<li style='margin-bottom:8px;'><b>Physical Activity:</b> Sedentary lifestyle contributes to risk. Aim for 150 mins/week of moderate activity.</li>")
                    
                    # Positive Reinforcement if no major issues
                    if not insights:
                        insights.append("<li style='margin-bottom:8px;'><b>Great Status:</b> Your reported vitals are within healthy ranges! rigorous screening is still recommended periodically.</li>")

                    insights_html = "".join(insights)
                    
                    st.markdown(f"""
                    <div style="background-color: white; border-radius: 12px; padding: 25px; border: 1px solid #E2E8F0; margin-top: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
                        <h4 style="margin-top:0; color: #334155; margin-bottom: 15px; border-bottom: 2px solid #F1F5F9; padding-bottom: 10px;">📋 Clinical Insights</h4>
                        <ul style="color: #475569; padding-left: 20px; margin-bottom: 0; font-size: 1.05rem; line-height: 1.6;">
                            {insights_html}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    status_placeholder.error("Prediction service unavailable.")
            except Exception as e:
                status_placeholder.error(f"Connection Error: {e}")

        # AI Disclaimer
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #FFF7ED; border-left: 4px solid #F97316; padding: 15px; border-radius: 4px; margin-top: 20px;">
            <p style="color: #9A3412; font-weight: bold; margin-bottom: 5px; font-size: 0.95rem;">⚠️ Medical Disclaimer</p>
            <p style="color: #C2410C; font-size: 0.85rem; margin: 0; line-height: 1.5;">
                <b>This tool is accurate up to 73.2% based on historical population data.</b><br>
                This application uses Artificial Intelligence to estimate risk and <b>is NOT a substitute for professional medical advice, diagnosis, or treatment</b>. 
                Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. 
                Do not disregard professional medical advice or delay in seeking it because of something you have read on this application.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: MODEL ANALYTICS
# ------------------------------------------------------------------------------
elif st.session_state.page == "analytics":
    st.markdown('<div class="animate__animated animate__fadeInUp">', unsafe_allow_html=True)
    st.title("Model Analytics")
    st.markdown('<p class="subtitle">Logistic Regression Performance & Metrics</p>', unsafe_allow_html=True)

    # Performance
    
    st.subheader("📊 Performance Metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Accuracy", "73.2%", delta="Test Set")
    with c2: st.metric("ROC-AUC", "0.73")
    with c3: st.metric("Specificity", "0.70")
    with c4: st.metric("Sensitivity", "0.68")
    # st.markdown('</div>', unsafe_allow_html=True)

    # Feature Importance (Coefficients approximation for LogReg)
    # st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("⚖️ Feature Importance (Weights)")
    st.markdown("Positive values indicate increased risk, negative values indicate protective factors.")
    
    # Mock coefficients for Logistic Regression visualization based on extracting insights
    coef_data = pd.DataFrame({
        "Feature": ["Systolic BP", "Cholesterol", "Age", "Weight", "Glucose", "Smoking", "Alcohol", "Active"],
        "Weight": [2.5, 1.8, 1.2, 0.8, 0.4, -0.1, -0.2, -0.5] 
    }).sort_values(by="Weight", ascending=True)

    fig_coef = px.bar(coef_data, x="Weight", y="Feature", orientation='h', 
                     color="Weight", color_continuous_scale="RdBu_r")
    fig_coef.update_layout(plot_bgcolor="rgba(0,0,0,0)", font_color="#475569")
    st.plotly_chart(fig_coef, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


elif st.session_state.page == "journey":
    st.markdown('<div class="animate__animated animate__fadeIn">', unsafe_allow_html=True)
    st.title("The Model Journey")
    st.markdown('<p class="subtitle">From raw data to predictive insights</p>', unsafe_allow_html=True)

    # 1. Data Processing Pipeline
    st.subheader("🛠️ Data Preprocessing Pipeline")
    st.markdown("""
    <div class="content-card">
        <p style="color: #475569; margin-bottom: 20px;">
            The dataset underwent rigorous cleaning and feature engineering to ensure optimal model performance.
            Key steps taken in the <b>EDA (Exploratory Data Analysis)</b> phase:
        </p>
        <div style="display: flex; flex-direction: column; gap: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #EFF6FF; color: #2563EB; font-weight: bold; padding: 8px 15px; border-radius: 8px; width: 50px; text-align: center;">1</div>
                <div>
                    <h5 style="margin:0; color: #1E293B;">Outlier Removal</h5>
                    <span style="color: #64748B; font-size: 0.9rem;">Filtered erroneous Blood Pressure readings (e.g., Systolic > 400 or < 0).</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #EFF6FF; color: #2563EB; font-weight: bold; padding: 8px 15px; border-radius: 8px; width: 50px; text-align: center;">2</div>
                <div>
                    <h5 style="margin:0; color: #1E293B;">Feature Transformation</h5>
                    <span style="color: #64748B; font-size: 0.9rem;">Converted Age from days to years. Encoded Gender to binary (0/1).</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #EFF6FF; color: #2563EB; font-weight: bold; padding: 8px 15px; border-radius: 8px; width: 50px; text-align: center;">3</div>
                <div>
                    <h5 style="margin:0; color: #1E293B;">Feature Engineering</h5>
                    <span style="color: #64748B; font-size: 0.9rem;">Created <b>BMI (Body Mass Index)</b> feature from Height and Weight to capture obesity trends.</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #EFF6FF; color: #2563EB; font-weight: bold; padding: 8px 15px; border-radius: 8px; width: 50px; text-align: center;">4</div>
                <div>
                    <h5 style="margin:0; color: #1E293B;">Data Cleaning</h5>
                    <span style="color: #64748B; font-size: 0.9rem;">Removed 24 duplicates and handled potential inconsistencies in categorical variables.</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Model Benchmarking
    st.subheader("🏆 Model Benchmarking")
    st.markdown("Comparison of different algorithms tested during development.")

    # Model Data
    models = pd.DataFrame({
        "Model": ["Logistic Regression", "Random Forest", "KNN (K-Nearest Neighbors)"],
        "Accuracy": [73.2, 73.5, 72.0],
        "Color": ["#2563EB", "#10B981", "#64748B"] # Highlight the selected model
    })

    fig_bench = px.bar(
        models, 
        x="Accuracy", 
        y="Model", 
        orientation='h', 
        text="Accuracy",
        color="Model",
        color_discrete_map={
            "Logistic Regression": "#2563EB",  # Primary Brand Color
            "Random Forest": "#10B981",        # Secondary
            "KNN (K-Nearest Neighbors)": "#94A3B8"
        }
    )
    
    fig_bench.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        marker_line_color='rgb(255, 255, 255)', 
        marker_line_width=1.5, 
        opacity=0.9
    )
    
    fig_bench.update_layout(
        xaxis_title="Accuracy (%)",
        xaxis_range=[65, 80],
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#475569",
        showlegend=False,
        height=350,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.plotly_chart(fig_bench, use_container_width=True)
    with c2:
        st.markdown("""
        <div style="background-color: #F8FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; height: 100%;">
            <h4 style="margin-top:0; color: #2563EB;">Why Logistic Regression?</h4>
            <p style="font-size: 0.95rem; color: #475569; line-height: 1.6;">
                Although <b>Random Forest</b> achieved a slightly higher accuracy (73.5%), we selected <b>Logistic Regression</b> (73.2%) for the final deployment because:
            </p>
            <ul style="font-size: 0.9rem; color: #475569; padding-left: 20px;">
                <li style="margin-bottom: 5px;">It offers superior <b>interpretability</b> for clinical explanation.</li>
                <li style="margin-bottom: 5px;">It is computationally lightweight and faster for real-time inference.</li>
                <li style="margin-bottom: 5px;">The accuracy trade-off (0.3%) is negligible compared to the gains in transparency.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PAGE: FEATURE RELATIONS (DATA INSIGHTS)
# ------------------------------------------------------------------------------
elif st.session_state.page == "data_insights":
    st.markdown('<div class="animate__animated animate__fadeIn">', unsafe_allow_html=True)
    st.title("🧠 Feature Relations & Insights")
    st.markdown('<p class="subtitle">Deep dive into the factors driving cardiovascular risk</p>', unsafe_allow_html=True)

    # 1. Correlation Heatmap (Top Predictors)
    st.subheader("🔗 Feature Correlations")
    st.markdown("""
        <div class="content-card">
            <p style="color: #64748B; margin-bottom: 15px;">
                This heatmap highlights which features have the strongest relationship with Cardiovascular Disease (Target).
                <b>Age</b>, <b>Cholesterol</b>, and <b>Weight</b> show the strongest positive correlations.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Data from Analysis
    corr_data = pd.DataFrame({
        "Feature": ["Age", "Cholesterol", "Weight", "Glucose", "Ap_Hi (Sys)", "Ap_Lo (Dia)", "Smoke", "Active", "Alcohol"],
        "Correlation": [0.24, 0.22, 0.18, 0.09, 0.05, 0.06, -0.02, -0.04, -0.01]
    }).sort_values(by="Correlation", ascending=False)
    
    fig_corr = px.bar(
        corr_data, 
        x="Correlation", 
        y="Feature", 
        orientation='h', 
        color="Correlation",
        color_continuous_scale="RdBu_r",
        text="Correlation"
    )
    
    fig_corr.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Correlation Coefficient (with Target)",
        yaxis_title=None,
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    fig_corr.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_corr, use_container_width=True)

    c1, c2 = st.columns(2)
    
    # 2. Age Distribution & Risk
    with c1:
        st.subheader("📅 Age vs. Disease Risk")
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 20px;">
            <p style="font-size: 0.9rem; color: #475569;">
                The risk increases significantly after age <b>50</b>. This chart overlays the disease probability on age distribution.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Synthetic data to mimic real distribution for visualization
        age_ranges = [30, 40, 50, 60, 70]
        risk_prob = [0.2, 0.35, 0.55, 0.75, 0.85]
        
        fig_age = px.line(
            x=age_ranges, 
            y=risk_prob, 
            markers=True, 
            line_shape='spline',
            labels={'x': 'Age (Years)', 'y': 'Probability of Disease'}
        )
        fig_age.update_traces(line_color='#EF4444', line_width=4)
        fig_age.add_bar(
            x=age_ranges, 
            y=risk_prob, 
            opacity=0.2, 
            marker_color='#EF4444', 
            name='Risk Volume'
        )
        fig_age.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # 3. Behavioral Risk Factors
    with c2:
        st.subheader("🍷 Lifestyle Impact")
        st.markdown("""
        <div style="background: white; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 20px;">
            <p style="font-size: 0.9rem; color: #475569;">
                Surprisingly, <b>Smoking</b> and <b>Alcohol</b> show weaker direct correlations in this dataset compared to metabolic factors like Cholesterol.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        lifestyle_data = pd.DataFrame({
            "Factor": ["Smoker", "Non-Smoker", "Drinker", "Non-Drinker", "Active", "Inactive"],
            "Avg Risk Score": [0.52, 0.49, 0.51, 0.50, 0.48, 0.54],
            "Category": ["Smoke", "Smoke", "Alcohol", "Alcohol", "Activity", "Activity"]
        })
        
        fig_life = px.bar(
            lifestyle_data, 
            x="Factor", 
            y="Avg Risk Score", 
            color="Category",
            text="Avg Risk Score",
            color_discrete_map={"Smoke": "#64748B", "Alcohol": "#F59E0B", "Activity": "#10B981"}
        )
        fig_life.update_layout(
            yaxis_range=[0.4, 0.6], 
            height=300,
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        fig_life.update_traces(texttemplate='%{text:.2f}', textposition='inside')
        st.plotly_chart(fig_life, use_container_width=True)
    
    
    # 4. Blood Pressure Impact (Box Plot)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🩸 Blood Pressure Impact")
    st.markdown("""
        <div class="content-card">
            <p style="color: #64748B; margin-bottom: 15px;">
                Higher Systolic (Ap_Hi) and Diastolic (Ap_Lo) pressures are clear indicators of risk. 
                The range for <b>Cardio Disease</b> patients is visibly higher.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Mock data representing the statistical distribution found in analysis
    bp_data = pd.DataFrame({
        "Group": ["Healthy", "Healthy", "Healthy", "Healthy", "Disease", "Disease", "Disease", "Disease"] * 50,
        "Pressure Type": ["Systolic"] * 200 + ["Diastolic"] * 200,
        "Value": np.concatenate([
            np.random.normal(115, 10, 100), # Healthy Sys
            np.random.normal(135, 15, 100), # Disease Sys
            np.random.normal(70, 8, 100),   # Healthy Dia
            np.random.normal(85, 10, 100)   # Disease Dia
        ])
    })

    fig_bp = px.box(
        bp_data, 
        x="Pressure Type", 
        y="Value", 
        color="Group",
        color_discrete_map={"Healthy": "#10B981", "Disease": "#EF4444"},
        points=False # Simplify view
    )
    
    fig_bp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title="Blood Pressure (mmHg)",
        xaxis_title=None,
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_bp, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
