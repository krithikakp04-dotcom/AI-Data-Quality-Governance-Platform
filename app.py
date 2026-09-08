from data_ingestion import ingest_data
from data_quality import analyze_data_quality
from anomaly_detection import detect_anomalies
from quality_scoring import calculate_quality_score
from governance import generate_governance_recommendations
from monitoring import monitor_data_quality


# ==========================================
# DATA INGESTION
# ==========================================

df = ingest_data("dataset.csv")


# ==========================================
# DATA QUALITY ANALYSIS
# ==========================================

quality_results = analyze_data_quality(df)


# ==========================================
# ANOMALY DETECTION
# ==========================================

df_with_anomalies = detect_anomalies(df)

# ==========================================
# QUALITY SCORING
# ==========================================

quality_score = calculate_quality_score(
    df,
    quality_results
)

# ==========================================
# GOVERNANCE RECOMMENDATIONS
# ==========================================

governance_report = generate_governance_recommendations(
    df,
    quality_results,
    quality_score
)

# ==========================================
# DATA QUALITY MONITORING
# ==========================================

monitoring_result = monitor_data_quality(
    quality_score
)