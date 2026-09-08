import pandas as pd
import os


def calculate_quality_score(df, quality_results):

    os.makedirs("reports", exist_ok=True)

    total_rows = len(df)

    if total_rows == 0:
        return 0

    # ==========================================
    # 1. MISSING DATA SCORE
    # ==========================================

    total_missing = int(
        df.isnull().sum().sum()
    )

    total_cells = df.shape[0] * df.shape[1]

    missing_rate = (
        total_missing / total_cells
        if total_cells > 0 else 0
    )

    missing_score = max(
        0,
        100 - (missing_rate * 100)
    )

    # ==========================================
    # 2. DUPLICATE SCORE
    # ==========================================

    duplicate_count = quality_results["duplicates"]

    duplicate_rate = (
        duplicate_count / total_rows
    )

    duplicate_score = max(
        0,
        100 - (duplicate_rate * 100)
    )

    # ==========================================
    # 3. INVALID DATA SCORE
    # ==========================================

    invalid_count = len(
        quality_results["invalid"]
    )

    invalid_rate = (
        invalid_count / total_rows
    )

    invalid_score = max(
        0,
        100 - (invalid_rate * 100)
    )

    # ==========================================
    # 4. INCONSISTENCY SCORE
    # ==========================================

    inconsistency_count = len(
        quality_results["inconsistencies"]
    )

    # Use number of inconsistent categories
    inconsistency_rate = (
        inconsistency_count / df.shape[1]
    )

    inconsistency_score = max(
        0,
        100 - (inconsistency_rate * 100)
    )

    # ==========================================
    # OVERALL SCORE
    # ==========================================

    overall_score = (
        missing_score * 0.25 +
        duplicate_score * 0.25 +
        invalid_score * 0.25 +
        inconsistency_score * 0.25
    )

    # ==========================================
    # QUALITY LEVEL
    # ==========================================

    if overall_score >= 90:
        quality_level = "Excellent"

    elif overall_score >= 75:
        quality_level = "Good"

    elif overall_score >= 50:
        quality_level = "Needs Improvement"

    else:
        quality_level = "Poor"

    # ==========================================
    # CREATE REPORT
    # ==========================================

    score_report = pd.DataFrame({
        "Metric": [
            "Missing Data Score",
            "Duplicate Data Score",
            "Validity Score",
            "Consistency Score",
            "Overall Quality Score"
        ],
        "Score": [
            round(missing_score, 2),
            round(duplicate_score, 2),
            round(invalid_score, 2),
            round(inconsistency_score, 2),
            round(overall_score, 2)
        ]
    })

    score_report.to_csv(
        "reports/quality_score.csv",
        index=False
    )

    # ==========================================
    # PRINT RESULTS
    # ==========================================

    print("\n" + "=" * 60)
    print("DATA QUALITY SCORE")
    print("=" * 60)

    print(
        "Missing Data Score:",
        round(missing_score, 2)
    )

    print(
        "Duplicate Data Score:",
        round(duplicate_score, 2)
    )

    print(
        "Validity Score:",
        round(invalid_score, 2)
    )

    print(
        "Consistency Score:",
        round(inconsistency_score, 2)
    )

    print(
        "\nOverall Quality Score:",
        round(overall_score, 2),
        "%"
    )

    print(
        "Quality Level:",
        quality_level
    )

    print(
        "\nReport saved to:",
        "reports/quality_score.csv"
    )

    return {
        "missing_score": missing_score,
        "duplicate_score": duplicate_score,
        "invalid_score": invalid_score,
        "consistency_score": inconsistency_score,
        "overall_score": overall_score,
        "quality_level": quality_level
    }