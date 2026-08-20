# ============================================================
# UPI TRANSACTION RISK ANALYZER
# AI-POWERED UPI FRAUD DETECTION SYSTEM
# ============================================================

import streamlit as st
import pandas as pd
import joblib


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UPI Transaction Risk Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN APPLICATION
       ======================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #050b16 0%,
            #0a1424 50%,
            #101b2d 100%
        );
    }

    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 3rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
        max-width: 1300px;
    }


    /* ========================================================
       GLOBAL TEXT
       ======================================================== */

    html,
    body,
    [class*="css"] {
        color: #ffffff;
    }

    p {
        color: #ffffff !important;
    }

    label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .security-badge {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 18px;
    }

    .security-badge span {
        display: inline-block;
        background: #102a43;
        color: #38bdf8;
        padding: 9px 22px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 700;
        border: 1px solid #1e6a8a;
        letter-spacing: 0.5px;
    }

    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        color: #ffffff !important;
        line-height: 1.2;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #ffffff !important;
        font-size: 17px;
        margin-bottom: 35px;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        font-size: 23px;
        font-weight: 700;
        color: #38bdf8 !important;
        margin-top: 15px;
        margin-bottom: 20px;
    }


    /* ========================================================
       INPUT LABELS
       ======================================================== */

    .stSelectbox label,
    .stNumberInput label {
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }


    /* ========================================================
       INPUT BOXES
       ======================================================== */

    .stSelectbox div[data-baseweb="select"] {
        background-color: #172235 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    .stSelectbox div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    .stNumberInput input {
        background-color: #172235 !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    .stNumberInput input::placeholder {
        color: #cbd5e1 !important;
    }


    /* ========================================================
       DROPDOWN MENU
       ======================================================== */

    div[data-baseweb="popover"] {
        background-color: #172235 !important;
    }

    div[data-baseweb="popover"] * {
        color: #ffffff !important;
    }

    li[role="option"] {
        background-color: #172235 !important;
        color: #ffffff !important;
    }

    li[role="option"]:hover {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        width: 100%;
        height: 55px;
        border-radius: 12px;
        border: 1px solid #38bdf8;
        background: linear-gradient(
            90deg,
            #0369a1,
            #2563eb
        );
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 700;
        transition: 0.2s;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #0284c7,
            #1d4ed8
        );
        transform: scale(1.01);
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #050b16 !important;
        border-right: 1px solid #26364d;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        background: #111c2e !important;
        border: 1px solid #334155 !important;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #111c2e !important;
        border: 1px solid #334155 !important;
        border-radius: 14px;
        padding: 18px;
    }

    div[data-testid="stMetric"] label {
        color: #ffffff !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: #ffffff !important;
    }


    /* ========================================================
       RESULT CARDS
       ======================================================== */

    .safe-card {
        background: linear-gradient(
            135deg,
            #052e16,
            #064e3b
        );
        border: 1px solid #10b981;
        border-radius: 18px;
        padding: 28px;
        text-align: center;
        margin-top: 15px;
    }

    .fraud-card {
        background: linear-gradient(
            135deg,
            #450a0a,
            #7f1d1d
        );
        border: 1px solid #ef4444;
        border-radius: 18px;
        padding: 28px;
        text-align: center;
        margin-top: 15px;
    }

    .result-title {
        font-size: 27px;
        font-weight: 800;
        color: #ffffff !important;
    }

    .probability {
        font-size: 46px;
        font-weight: 800;
        color: #ffffff !important;
        margin: 10px 0;
    }

    .result-description {
        color: #ffffff !important;
        font-size: 15px;
    }


    /* ========================================================
       DATAFRAME / TABLE
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
    }


    /* ========================================================
       INFO BOX
       ======================================================== */

    div[data-testid="stAlert"] {
        color: #ffffff !important;
    }

    div[data-testid="stAlert"] p {
        color: #ffffff !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #ffffff !important;
        font-size: 13px;
        margin-top: 40px;
        padding-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. LOAD TRAINED MODEL
# ============================================================

# Load the complete model artifact.
#
# The artifact contains:
# 1. Trained Logistic Regression model
# 2. Preprocessing pipeline
# 3. Optimized probability threshold

artifact = joblib.load(
    "models/upi_fraud_model.pkl"
)

model = artifact["model"]

preprocessor = artifact["preprocessor"]

threshold = artifact["threshold"]


# ============================================================
# 4. HEADER
# ============================================================

st.markdown(
    """
    <div class="security-badge">
        <span>🛡️ AI-POWERED TRANSACTION SECURITY</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-title">
        UPI Transaction Risk Analyzer
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Intelligent Machine Learning Based Fraud Detection System
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛡️ Risk Analyzer")

    st.write(
        "Analyze UPI transactions using a trained "
        "machine-learning classification model."
    )

    st.divider()

    st.markdown("### 🤖 Final Model")

    st.info(
        "Tuned Logistic Regression"
    )

    st.markdown("### 🎯 Detection Threshold")

    st.metric(
        "Threshold",
        f"{threshold:.2f}"
    )

    st.markdown("### 📊 Model Performance")

    st.metric(
        "Precision",
        "24.28%"
    )

    st.metric(
        "Recall",
        "45.65%"
    )

    st.metric(
        "F1 Score",
        "31.70%"
    )

    st.metric(
        "ROC-AUC",
        "74.41%"
    )

    st.divider()

    st.write(
        "Dataset: Synthetic UPI Transactions"
    )

    st.caption(
        "Educational machine-learning project "
        "for fraud detection demonstration."
    )


# ============================================================
# 6. TRANSACTION INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">💳 Transaction Analysis</div>',
    unsafe_allow_html=True
)

left_column, right_column = st.columns(2)


# ============================================================
# 7. LEFT COLUMN
# ============================================================

with left_column:

    amount = st.number_input(
        "💰 Transaction Amount",
        min_value=1.0,
        max_value=1000000.0,
        value=1000.0,
        step=100.0
    )

    transaction_type = st.selectbox(
        "🔄 Transaction Type",
        [
            "send",
            "receive",
            "merchant_payment"
        ]
    )

    location = st.selectbox(
        "📍 Location",
        [
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Kolkata",
            "Pune",
            "Ahmedabad"
        ]
    )

    device_type = st.selectbox(
        "📱 Device Type",
        [
            "mobile",
            "tablet"
        ]
    )


# ============================================================
# 8. RIGHT COLUMN
# ============================================================

with right_column:

    is_rooted_device = st.selectbox(
        "🔓 Rooted Device",
        [0, 1],
        format_func=lambda x:
        "No" if x == 0 else "Yes"
    )

    network_type = st.selectbox(
        "🌐 Network Type",
        [
            "4G",
            "5G",
            "WiFi"
        ]
    )

    time_of_day = st.selectbox(
        "🕒 Time of Day",
        [
            "morning",
            "afternoon",
            "evening",
            "night"
        ]
    )


# ============================================================
# 9. PREDICTION BUTTON
# ============================================================

st.markdown("")

predict_button = st.button(
    "🔍 ANALYZE TRANSACTION"
)


# ============================================================
# 10. FRAUD PREDICTION
# ============================================================

if predict_button:

    # --------------------------------------------------------
    # Create input DataFrame
    # --------------------------------------------------------

    input_data = pd.DataFrame({

        "amount": [amount],

        "transaction_type": [
            transaction_type
        ],

        "location": [
            location
        ],

        "device_type": [
            device_type
        ],

        "is_rooted_device": [
            is_rooted_device
        ],

        "network_type": [
            network_type
        ],

        "time_of_day": [
            time_of_day
        ],

        # Time-based features
        "year": [2026],
        "month": [8],
        "day": [20],
        "day_of_week": [3],
        "hour": [12],
        "is_weekend": [0]
    })


    # --------------------------------------------------------
    # Apply preprocessing
    # --------------------------------------------------------

    input_processed = preprocessor.transform(
        input_data
    )


    # --------------------------------------------------------
    # Calculate fraud probability
    # --------------------------------------------------------

    fraud_probability = model.predict_proba(
        input_processed
    )[0, 1]

    fraud_percentage = (
        fraud_probability * 100
    )


    # ========================================================
    # RISK ASSESSMENT
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Risk Assessment</div>',
        unsafe_allow_html=True
    )


    metric1, metric2, metric3 = st.columns(3)


    with metric1:

        st.metric(
            "Fraud Probability",
            f"{fraud_percentage:.2f}%"
        )


    with metric2:

        st.metric(
            "Detection Threshold",
            f"{threshold * 100:.0f}%"
        )


    with metric3:

        st.metric(
            "Transaction Amount",
            f"₹{amount:,.2f}"
        )


    # ========================================================
    # RISK STATUS
    # ========================================================

    if fraud_probability >= threshold:

        st.markdown(
            f"""
            <div class="fraud-card">

                <div class="result-title">
                    🚨 HIGH RISK TRANSACTION
                </div>

                <div class="probability">
                    {fraud_percentage:.2f}%
                </div>

                <div class="result-description">
                    The machine-learning model has identified
                    this transaction as potentially fraudulent.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="safe-card">

                <div class="result-title">
                    ✅ LOW RISK TRANSACTION
                </div>

                <div class="probability">
                    {fraud_percentage:.2f}%
                </div>

                <div class="result-description">
                    The machine-learning model has classified
                    this transaction as likely legitimate.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # TRANSACTION SUMMARY
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-title">📋 Transaction Summary</div>',
        unsafe_allow_html=True
    )


    summary = pd.DataFrame({

        "Feature": [
            "Transaction Amount",
            "Transaction Type",
            "Location",
            "Device Type",
            "Rooted Device",
            "Network Type",
            "Time of Day"
        ],

        "Value": [
            f"₹{amount:,.2f}",
            transaction_type,
            location,
            device_type,
            "Yes" if is_rooted_device == 1 else "No",
            network_type,
            time_of_day
        ]
    })


    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # MODEL INFORMATION
    # ========================================================

    st.markdown("")

    st.markdown(
        '<div class="section-title">🤖 Model Information</div>',
        unsafe_allow_html=True
    )


    info_col1, info_col2, info_col3 = st.columns(3)


    with info_col1:

        st.metric(
            "Algorithm",
            "Logistic Regression"
        )


    with info_col2:

        st.metric(
            "F1 Score",
            "31.70%"
        )


    with info_col3:

        st.metric(
            "ROC-AUC",
            "74.41%"
        )


# ============================================================
# 11. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🛡️ UPI Transaction Risk Analyzer
        &nbsp; | &nbsp;
        Machine Learning Project
        &nbsp; | &nbsp;
        Python + Scikit-learn + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)