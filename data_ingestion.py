import pandas as pd
import os
from datetime import datetime


def ingest_data(input_file="dataset.csv"):

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Dataset not found: {input_file}"
        )

    # Read dataset
    df = pd.read_csv(input_file)

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    # Create ingestion log
    log_data = pd.DataFrame({
        "Date": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],
        "Source File": [input_file],
        "Rows": [df.shape[0]],
        "Columns": [df.shape[1]],
        "Status": ["Success"]
    })

    log_file = "reports/ingestion_log.csv"

    if os.path.exists(log_file):
        old_log = pd.read_csv(log_file)
        log_data = pd.concat(
            [old_log, log_data],
            ignore_index=True
        )

    log_data.to_csv(log_file, index=False)

    print("=" * 60)
    print("DATA INGESTION")
    print("=" * 60)
    print("Source File:", input_file)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Status: Successfully ingested")
    print("Log:", log_file)
    print("=" * 60)

    return df