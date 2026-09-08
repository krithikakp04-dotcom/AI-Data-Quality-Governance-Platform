import pandas as pd
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def detect_anomalies(df):

    os.makedirs("reports", exist_ok=True)

    # Select numerical columns
    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    # Remove ID column from anomaly detection
    numerical_columns = [
        col for col in numerical_columns
        if col != "Customer_ID"
    ]

    if len(numerical_columns) == 0:
        print("No numerical columns available.")
        return df

    # Prepare data
    data = df[numerical_columns].copy()

    # Fill missing values with median
    data = data.fillna(data.median())

    # Scale numerical data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Isolation Forest model
    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )

    predictions = model.fit_predict(scaled_data)

    # Add anomaly result
    result = df.copy()

    result["Anomaly"] = predictions

    result["Anomaly Status"] = result["Anomaly"].map({
        1: "Normal",
        -1: "Anomaly"
    })

    # Save report
    anomaly_report = result[
        result["Anomaly"] == -1
    ]

    anomaly_report.to_csv(
        "reports/anomaly_records.csv",
        index=False
    )

    print("\n" + "=" * 60)
    print("ANOMALY DETECTION")
    print("=" * 60)

    print(
        "Numerical columns:",
        numerical_columns
    )

    print(
        "Total records:",
        len(result)
    )

    print(
        "Anomalies detected:",
        len(anomaly_report)
    )

    print("\nAnomaly Records:")
    print(anomaly_report)

    print(
        "\nReport saved to: "
        "reports/anomaly_records.csv"
    )

    return result