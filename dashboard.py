import streamlit as st
import pandas as pd
import os

from data_ingestion import ingest_data
from data_quality import analyze_data_quality
from anomaly_detection import detect_anomalies
from quality_scoring import calculate_quality_score
from governance import generate_governance_recommendations
from monitoring import monitor_data_quality


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Data Quality & Governance",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("📊 AI-Powered Data Quality & Governance Platform")

st.subheader("Project Details")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
        **Project Topic**

        AI-Powered Data Quality & Governance Platform
        """
    )

with col2:
    st.info(
        """
        **Student Details**

        **Full Name:** Krithika K P

        **Registered Email ID:** krithikakp04@gmail.com
        """
    )

st.markdown("---")


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Overview",
        "Data Quality",
        "Anomaly Detection",
        "Quality Score",
        "Governance",
        "Monitoring"
    ]
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    df = ingest_data("dataset.csv")

    quality_results = analyze_data_quality(df)

    anomaly_data = detect_anomalies(df)

    quality_score = calculate_quality_score(
        df,
        quality_results
    )

    governance_report = generate_governance_recommendations(
        df,
        quality_results,
        quality_score
    )

    monitoring_result = monitor_data_quality(
        quality_score
    )

    return (
        df,
        quality_results,
        anomaly_data,
        quality_score,
        governance_report,
        monitoring_result
    )


df, quality_results, anomaly_data, quality_score, governance_report, monitoring_result = load_data()


# ==========================================
# OVERVIEW
# ==========================================

if page == "Overview":

    st.header("📋 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Total Columns",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Quality Score",
            f"{quality_score['overall_score']:.2f}%"
        )

    with col4:
        st.metric(
            "Anomalies",
            int((anomaly_data["Anomaly"] == -1).sum())
        )

    st.markdown("---")

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================================
# DATA QUALITY
# ==========================================

elif page == "Data Quality":

    st.header("🔍 Data Quality Analysis")

    # Missing values

    st.subheader("Missing Values")

    st.dataframe(
        quality_results["missing"],
        use_container_width=True
    )

    # Duplicate records

    st.subheader("Duplicate Records")

    st.metric(
        "Duplicate Rows",
        quality_results["duplicates"]
    )

    # Invalid records

    st.subheader("Invalid Values")

    if len(quality_results["invalid"]) > 0:

        st.dataframe(
            quality_results["invalid"],
            use_container_width=True
        )

    else:

        st.success("No invalid values detected.")

    # Inconsistencies

    st.subheader("Categorical Inconsistencies")

    if len(quality_results["inconsistencies"]) > 0:

        st.dataframe(
            quality_results["inconsistencies"],
            use_container_width=True
        )

    else:

        st.success("No categorical inconsistencies detected.")


# ==========================================
# ANOMALY DETECTION
# ==========================================

elif page == "Anomaly Detection":

    st.header("🤖 AI Anomaly Detection")

    anomaly_count = int(
        (anomaly_data["Anomaly"] == -1).sum()
    )

    normal_count = int(
        (anomaly_data["Anomaly"] == 1).sum()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Normal Records",
            normal_count
        )

    with col2:

        st.metric(
            "Anomalies Detected",
            anomaly_count
        )

    st.markdown("---")

    st.subheader("Detected Anomalies")

    anomalies = anomaly_data[
        anomaly_data["Anomaly"] == -1
    ]

    if len(anomalies) > 0:

        st.dataframe(
            anomalies,
            use_container_width=True
        )

    else:

        st.success("No anomalies detected.")


# ==========================================
# QUALITY SCORE
# ==========================================

elif page == "Quality Score":

    st.header("📈 Data Quality Score")

    score = quality_score["overall_score"]
    level = quality_score["quality_level"]

    st.metric(
        "Overall Quality Score",
        f"{score:.2f}%"
    )

    st.progress(
        min(score / 100, 1.0)
    )

    st.subheader(
        f"Quality Level: {level}"
    )

    score_data = pd.DataFrame({
        "Metric": [
            "Missing Data",
            "Duplicate Data",
            "Validity",
            "Consistency"
        ],
        "Score": [
            quality_score["missing_score"],
            quality_score["duplicate_score"],
            quality_score["invalid_score"],
            quality_score["consistency_score"]
        ]
    })

    st.bar_chart(
        score_data.set_index("Metric")
    )


# ==========================================
# GOVERNANCE
# ==========================================

elif page == "Governance":

    st.header("🛡️ Data Governance Recommendations")

    if len(governance_report) > 0:

        st.dataframe(
            governance_report,
            use_container_width=True
        )

    else:

        st.success(
            "No governance issues detected."
        )


# ==========================================
# MONITORING
# ==========================================

elif page == "Monitoring":

    st.header("📊 Data Quality Monitoring")

    monitoring_file = (
        "reports/quality_monitoring.csv"
    )

    if os.path.exists(monitoring_file):

        monitoring_data = pd.read_csv(
            monitoring_file
        )

        st.subheader("Quality Score Trend")

        st.line_chart(
            monitoring_data[
                "Overall Quality Score"
            ]
        )

        st.subheader("Monitoring History")

        st.dataframe(
            monitoring_data,
            use_container_width=True
        )

        st.metric(
            "Current Trend",
            monitoring_result["trend"]
        )

    else:

        st.warning(
            "Monitoring data is not available yet."
        )