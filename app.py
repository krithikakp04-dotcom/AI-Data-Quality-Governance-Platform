from data_ingestion import ingest_data
from data_quality import analyze_data_quality
from anomaly_detection import detect_anomalies
from quality_scoring import calculate_quality_score


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