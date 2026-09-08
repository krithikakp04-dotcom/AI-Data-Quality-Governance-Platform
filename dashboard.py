import streamlit as st
import pandas as pd
import os

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
# DATASET UPLOAD
# ==========================================

st.sidebar.subheader("📂 Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.sidebar.success(
        f"Uploaded: {uploaded_file.name}"
    )

else:

    df = pd.read_csv("dataset.csv")

    st.sidebar.info(
        "Using default dataset.csv"
    )


# ==========================================
# SIDEBAR NAVIGATION
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
# RUN ANALYSIS BUTTON
# ==========================================

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Analysis")

run_analysis = st.sidebar.button(
    "🔄 Run Analysis",
    use_container_width=True
)


# ==========================================
# ANALYSIS
# ==========================================

if run_analysis:

    with st.spinner("Analyzing dataset..."):

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

        # Store results in session state
        st.session_state.quality_results = quality_results
        st.session_state.anomaly_data = anomaly_data
        st.session_state.quality_score = quality_score
        st.session_state.governance_report = governance_report
        st.session_state.monitoring_result = monitoring_result
        st.session_state.analysis_complete = True

    st.sidebar.success("✅ Analysis completed!")


# ==========================================
# CHECK ANALYSIS STATUS
# ==========================================

if "analysis_complete" not in st.session_state:

    st.session_state.analysis_complete = False


if not st.session_state.analysis_complete:

    st.info(
        """
        👈 **Upload a CSV dataset if required and click
        `🔄 Run Analysis` from the sidebar to begin.**
        """
    )

    st.stop()


# ==========================================
# GET ANALYSIS RESULTS
# ==========================================

quality_results = st.session_state.quality_results

anomaly_data = st.session_state.anomaly_data

quality_score = st.session_state.quality_score

governance_report = st.session_state.governance_report

monitoring_result = st.session_state.monitoring_result


# ==========================================
# REPORT DOWNLOADS
# ==========================================

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Download Reports")

report_files = {
    "Quality Score": "reports/quality_score.csv",
    "Anomaly Records": "reports/anomaly_records.csv",
    "Governance Recommendations":
        "reports/governance_recommendations.csv",
    "Missing Values":
        "reports/missing_values.csv",
    "Invalid Values":
        "reports/invalid_values.csv",
    "Inconsistencies":
        "reports/inconsistencies.csv",
    "Quality Monitoring":
        "reports/quality_monitoring.csv"
}

for report_name, file_path in report_files.items():

    if os.path.exists(file_path):

        with open(file_path, "rb") as file:

            st.sidebar.download_button(
                label=f"⬇️ {report_name}",
                data=file,
                file_name=os.path.basename(file_path),
                mime="text/csv"
            )


# ==========================================
# OVERVIEW
# ==========================================

if page == "Overview":

    st.header("📋 Dataset Overview")

    # ==========================================
    # KEY METRICS
    # ==========================================

    total_rows = df.shape[0]
    total_columns = df.shape[1]

    missing_count = int(
        df.isnull().sum().sum()
    )

    duplicate_count = quality_results["duplicates"]

    anomaly_count = int(
        (anomaly_data["Anomaly"] == -1).sum()
    )

    quality_score_value = quality_score[
        "overall_score"
    ]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "📄 Total Rows",
            total_rows
        )

    with col2:
        st.metric(
            "📊 Total Columns",
            total_columns
        )

    with col3:
        st.metric(
            "⚠️ Missing Values",
            missing_count
        )

    with col4:
        st.metric(
            "🔁 Duplicate Rows",
            duplicate_count
        )

    with col5:
        st.metric(
            "🤖 Anomalies",
            anomaly_count
        )

    st.markdown("---")

    # ==========================================
    # QUALITY SUMMARY
    # ==========================================

    st.subheader("📈 Data Quality Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Overall Quality Score",
            f"{quality_score_value:.2f}%"
        )

        st.progress(
            min(quality_score_value / 100, 1.0)
        )

        st.write(
            f"**Quality Level:** "
            f"{quality_score['quality_level']}"
        )

    with col2:

        quality_summary = pd.DataFrame({
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
            quality_summary.set_index("Metric")
        )

    st.markdown("---")

    # ==========================================
    # DATASET PREVIEW
    # ==========================================

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ==========================================
    # NUMERICAL STATISTICS
    # ==========================================

    st.subheader("📊 Numerical Statistics")

    numerical_data = df.select_dtypes(
        include=["int64", "float64"]
    )

    if len(numerical_data.columns) > 0:

        statistics = numerical_data.describe().T

        statistics = statistics.round(2)

        st.dataframe(
            statistics,
            use_container_width=True
        )

    else:

        st.info(
            "No numerical columns available."
        )

    st.markdown("---")

    # ==========================================
    # PLATFORM SUMMARY
    # ==========================================

    st.subheader("🚀 Platform Summary")

    st.info(
        """
        **AI-Powered Data Quality & Governance Platform**

        This platform provides an end-to-end workflow for
        identifying and managing data-quality problems.

        🔍 **Data Quality** – Detects missing, duplicate,
        invalid, and inconsistent data.

        🤖 **Anomaly Detection** – Uses Isolation Forest
        to identify unusual records.

        📈 **Quality Scoring** – Calculates an overall
        data-quality score.

        🛡️ **Governance** – Provides prioritized
        recommendations for data improvement.

        📊 **Monitoring** – Tracks quality changes
        across analysis runs.

        📥 **Reports** – Allows users to download
        generated analysis reports.
        """
    )



# ==========================================
# DATA QUALITY
# ==========================================

elif page == "Data Quality":

    st.header("🔍 Data Quality Analysis")

    # ==========================================
    # MISSING VALUES
    # ==========================================

    st.subheader("Missing Values")

    missing_data = quality_results["missing"]

    col1, col2 = st.columns(2)

    with col1:

        st.dataframe(
            missing_data,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        missing_chart = missing_data[
            missing_data["Missing Values"] > 0
        ]

        if len(missing_chart) > 0:

            st.bar_chart(
                missing_chart.set_index("Column")
            )

        else:

            st.success(
                "✅ No missing values detected."
            )

    st.markdown("---")

    # ==========================================
    # DUPLICATES
    # ==========================================

    st.subheader("Duplicate Records")

    duplicate_count = quality_results["duplicates"]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Duplicate Rows",
            duplicate_count
        )

    with col2:

        if duplicate_count > 0:

            st.warning(
                f"⚠️ {duplicate_count} duplicate "
                "record(s) detected."
            )

        else:

            st.success(
                "✅ No duplicate records detected."
            )

    st.markdown("---")

    # ==========================================
    # INVALID VALUES
    # ==========================================

    st.subheader("Invalid Values")

    invalid_data = quality_results["invalid"]

    if len(invalid_data) > 0:

        st.dataframe(
            invalid_data,
            use_container_width=True,
            hide_index=True
        )

        invalid_counts = (
            invalid_data["Column"]
            .value_counts()
            .reset_index()
        )

        invalid_counts.columns = [
            "Column",
            "Invalid Records"
        ]

        st.bar_chart(
            invalid_counts.set_index("Column")
        )

    else:

        st.success(
            "✅ No invalid values detected."
        )

    st.markdown("---")

    # ==========================================
    # CATEGORICAL INCONSISTENCIES
    # ==========================================

    st.subheader(
        "Categorical Inconsistencies"
    )

    inconsistency_data = (
        quality_results["inconsistencies"]
    )

    if len(inconsistency_data) > 0:

        st.dataframe(
            inconsistency_data,
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            "⚠️ Different representations of "
            "the same category were detected."
        )

    else:

        st.success(
            "✅ No categorical inconsistencies detected."
        )


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

    # ==========================================
    # SUMMARY
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Records",
            len(anomaly_data)
        )

    with col2:

        st.metric(
            "Normal Records",
            normal_count
        )

    with col3:

        st.metric(
            "Anomalies Detected",
            anomaly_count
        )

    st.markdown("---")

    # ==========================================
    # ANOMALY DISTRIBUTION
    # ==========================================

    st.subheader("📊 Anomaly Distribution")

    distribution = pd.DataFrame({
        "Status": [
            "Normal",
            "Anomaly"
        ],
        "Records": [
            normal_count,
            anomaly_count
        ]
    })

    st.bar_chart(
        distribution.set_index("Status")
    )

    st.markdown("---")

    # ==========================================
    # ANOMALY RATE
    # ==========================================

    anomaly_percentage = (
        anomaly_count / len(anomaly_data) * 100
        if len(anomaly_data) > 0
        else 0
    )

    st.subheader("📈 Anomaly Rate")

    st.progress(
        min(anomaly_percentage / 100, 1.0)
    )

    st.write(
        f"**{anomaly_percentage:.2f}%** of the records "
        "were identified as potential anomalies."
    )

    st.markdown("---")

    # ==========================================
    # DETECTED ANOMALIES
    # ==========================================

    st.subheader("🚨 Detected Anomalies")

    anomalies = anomaly_data[
        anomaly_data["Anomaly"] == -1
    ]

    if len(anomalies) > 0:

        st.warning(
            f"⚠️ {len(anomalies)} potential "
            "anomalous record(s) detected."
        )

        st.dataframe(
            anomalies,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "✅ No anomalies detected."
        )

    st.markdown("---")

    # ==========================================
    # AI METHOD
    # ==========================================

    st.subheader("🧠 Detection Method")

    st.info(
        """
        **Isolation Forest**

        The platform uses the Isolation Forest machine
        learning algorithm to identify unusual records
        based on numerical data patterns.

        • 1 → Normal record

        • -1 → Potential anomaly

        Missing numerical values are handled using
        median imputation before anomaly detection.
        """
    )


# ==========================================
# QUALITY SCORE
# ==========================================

elif page == "Quality Score":

    st.header("📈 Data Quality Score")

    score = quality_score["overall_score"]

    level = quality_score["quality_level"]

    # ==========================================
    # OVERALL SCORE
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Overall Quality Score",
            f"{score:.2f}%"
        )

        st.progress(
            min(score / 100, 1.0)
        )

    with col2:

        st.metric(
            "Quality Level",
            level
        )

        if level == "Excellent":

            st.success(
                "✅ Excellent data quality"
            )

        elif level == "Good":

            st.success(
                "✅ Good data quality"
            )

        elif level == "Needs Improvement":

            st.warning(
                "⚠️ Data quality needs improvement"
            )

        else:

            st.error(
                "❌ Poor data quality"
            )

    st.markdown("---")

    # ==========================================
    # QUALITY METRICS
    # ==========================================

    st.subheader("📊 Quality Metrics")

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

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(
            score_data.set_index("Metric")
        )

    with col2:

        st.dataframe(
            score_data,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # ==========================================
    # SCORE INTERPRETATION
    # ==========================================

    st.subheader("📋 Score Interpretation")

    interpretation = pd.DataFrame({
        "Score Range": [
            "90% – 100%",
            "75% – 89%",
            "50% – 74%",
            "Below 50%"
        ],
        "Quality Level": [
            "Excellent",
            "Good",
            "Needs Improvement",
            "Poor"
        ]
    })

    st.dataframe(
        interpretation,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        """
        **Quality Score Calculation**

        The overall score combines four data-quality
        dimensions:

        • Missing Data Score – measures completeness

        • Duplicate Data Score – measures uniqueness

        • Validity Score – checks whether values follow
          valid rules

        • Consistency Score – checks consistent
          representation

        Each dimension contributes equally to the
        final score.
        """
    )


# ==========================================
# GOVERNANCE
# ==========================================

elif page == "Governance":

    st.header(
        "🛡️ Data Governance Recommendations"
    )

    # ==========================================
    # PRIORITY COUNTS
    # ==========================================

    if len(governance_report) > 0:

        high_count = int(
            (
                governance_report["Priority"]
                == "High"
            ).sum()
        )

        medium_count = int(
            (
                governance_report["Priority"]
                == "Medium"
            ).sum()
        )

        low_count = int(
            (
                governance_report["Priority"]
                == "Low"
            ).sum()
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "🔴 High Priority",
                high_count
            )

        with col2:

            st.metric(
                "🟠 Medium Priority",
                medium_count
            )

        with col3:

            st.metric(
                "🟢 Low Priority",
                low_count
            )

        st.markdown("---")

        # ==========================================
        # GOVERNANCE CHART
        # ==========================================

        st.subheader(
            "📊 Governance Issue Distribution"
        )

        priority_data = pd.DataFrame({
            "Priority": [
                "High",
                "Medium",
                "Low"
            ],
            "Issues": [
                high_count,
                medium_count,
                low_count
            ]
        })

        st.bar_chart(
            priority_data.set_index("Priority")
        )

        st.markdown("---")

        # ==========================================
        # RECOMMENDATIONS
        # ==========================================

        st.subheader(
            "📋 Recommended Actions"
        )

        st.dataframe(
            governance_report,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ==========================================
        # HIGH PRIORITY
        # ==========================================

        st.subheader(
            "🚨 High Priority Actions"
        )

        high_priority = governance_report[
            governance_report["Priority"] == "High"
        ]

        if len(high_priority) > 0:

            st.warning(
                "The following issues should be "
                "addressed first:"
            )

            st.dataframe(
                high_priority,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No high-priority governance issues."
            )

    else:

        st.success(
            "✅ No governance issues detected."
        )

    st.markdown("---")

    # ==========================================
    # GOVERNANCE INFORMATION
    # ==========================================

    st.subheader("🛡️ Governance Approach")

    st.info(
        """
        The governance module converts detected
        data-quality problems into actionable
        recommendations.

        **High Priority:** Issues requiring immediate
        attention.

        **Medium Priority:** Issues that should be
        corrected during data standardization.

        **Low Priority:** Minor issues that can be
        addressed during routine data maintenance.
        """
    )


# ==========================================
# MONITORING
# ==========================================

elif page == "Monitoring":

    st.header("📊 Data Quality Monitoring")

    monitoring_file = (
        "reports/quality_monitoring.csv"
    )

    # ==========================================
    # CURRENT STATUS
    # ==========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Current Quality Score",
            f"{quality_score['overall_score']:.2f}%"
        )

    with col2:

        st.metric(
            "Quality Level",
            quality_score["quality_level"]
        )

    with col3:

        st.metric(
            "Current Trend",
            monitoring_result["trend"]
        )

    st.markdown("---")

    # ==========================================
    # MONITORING HISTORY
    # ==========================================

    if os.path.exists(monitoring_file):

        monitoring_data = pd.read_csv(
            monitoring_file
        )

        st.subheader(
            "📈 Quality Score Trend"
        )

        st.line_chart(
            monitoring_data[
                "Overall Quality Score"
            ]
        )

        st.markdown("---")

        # ==========================================
        # SCORE CHANGE
        # ==========================================

        if len(monitoring_data) >= 2:

            previous_score = monitoring_data[
                "Overall Quality Score"
            ].iloc[-2]

            current_score = monitoring_data[
                "Overall Quality Score"
            ].iloc[-1]

            score_change = (
                current_score - previous_score
            )

            st.subheader(
                "📊 Score Change"
            )

            if score_change > 0:

                st.success(
                    f"⬆️ Quality score improved by "
                    f"{score_change:.2f} points."
                )

            elif score_change < 0:

                st.error(
                    f"⬇️ Quality score decreased by "
                    f"{abs(score_change):.2f} points."
                )

            else:

                st.info(
                    "➡️ Quality score remains stable."
                )

        st.markdown("---")

        # ==========================================
        # MONITORING HISTORY TABLE
        # ==========================================

        st.subheader(
            "📋 Monitoring History"
        )

        st.dataframe(
            monitoring_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No monitoring history is available yet."
        )

    st.markdown("---")

    # ==========================================
    # MONITORING INFORMATION
    # ==========================================

    st.subheader(
        "🔄 Continuous Monitoring"
    )

    st.info(
        """
        The monitoring module tracks data-quality
        scores over multiple analysis runs.

        **Improving:** Quality score increased.

        **Declining:** Quality score decreased.

        **Stable:** Quality score remained unchanged.

        This helps organizations continuously monitor
        the health of their datasets.
        """
    )