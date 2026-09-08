import pandas as pd
import os
from datetime import datetime


def monitor_data_quality(quality_score):

    os.makedirs("reports", exist_ok=True)

    # ==========================================
    # CURRENT QUALITY SCORE
    # ==========================================

    current_score = quality_score["overall_score"]
    quality_level = quality_score["quality_level"]

    # ==========================================
    # CREATE MONITORING RECORD
    # ==========================================

    monitoring_record = pd.DataFrame({
        "Date": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "Overall Quality Score": [
            round(current_score, 2)
        ],
        "Quality Level": [
            quality_level
        ]
    })

    monitoring_file = "reports/quality_monitoring.csv"

    # ==========================================
    # APPEND TO HISTORY
    # ==========================================

    if os.path.exists(monitoring_file):

        old_data = pd.read_csv(monitoring_file)

        monitoring_record = pd.concat(
            [old_data, monitoring_record],
            ignore_index=True
        )

    # ==========================================
    # SAVE MONITORING DATA
    # ==========================================

    monitoring_record.to_csv(
        monitoring_file,
        index=False
    )

    # ==========================================
    # CALCULATE TREND
    # ==========================================

    if len(monitoring_record) >= 2:

        previous_score = monitoring_record[
            "Overall Quality Score"
        ].iloc[-2]

        score_change = current_score - previous_score

        if score_change > 0:
            trend = "Improving"

        elif score_change < 0:
            trend = "Declining"

        else:
            trend = "Stable"

    else:

        score_change = 0
        trend = "Initial Run"

    # ==========================================
    # PRINT RESULTS
    # ==========================================

    print("\n" + "=" * 60)
    print("DATA QUALITY MONITORING")
    print("=" * 60)

    print(
        "Current Quality Score:",
        round(current_score, 2),
        "%"
    )

    print(
        "Quality Level:",
        quality_level
    )

    print(
        "Score Change:",
        round(score_change, 2)
    )

    print(
        "Quality Trend:",
        trend
    )

    print(
        "\nMonitoring history saved to:",
        monitoring_file
    )

    print("=" * 60)

    return {
        "current_score": current_score,
        "quality_level": quality_level,
        "score_change": score_change,
        "trend": trend,
        "history": monitoring_record
    }