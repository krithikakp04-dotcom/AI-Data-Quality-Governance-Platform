import pandas as pd
import os


def analyze_data_quality(df):

    os.makedirs("reports", exist_ok=True)

    # ==========================================
    # 1. MISSING VALUES
    # ==========================================

    missing_values = df.isnull().sum()

    missing_report = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": missing_values.values
    })

    # ==========================================
    # 2. DUPLICATE ROWS
    # ==========================================

    duplicate_count = int(df.duplicated().sum())

    # ==========================================
    # 3. INVALID VALUES
    # ==========================================

    invalid_records = []

    # Invalid Age
    if "Age" in df.columns:
        invalid_age = df[
            (df["Age"] < 0) | (df["Age"] > 100)
        ]

        for index in invalid_age.index:
            invalid_records.append({
                "Row": index + 1,
                "Column": "Age",
                "Issue": "Invalid age value",
                "Value": df.loc[index, "Age"]
            })

    # Invalid Income
    if "Income" in df.columns:
        invalid_income = df[
            df["Income"] < 0
        ]

        for index in invalid_income.index:
            invalid_records.append({
                "Row": index + 1,
                "Column": "Income",
                "Issue": "Negative income",
                "Value": df.loc[index, "Income"]
            })

    invalid_report = pd.DataFrame(invalid_records)

    # ==========================================
    # 4. CATEGORICAL INCONSISTENCY
    # ==========================================

    inconsistent_records = []

    if "City" in df.columns:

        city_values = df["City"].dropna()

        city_normalized = city_values.str.lower().str.strip()

        city_groups = {}

        for original, normalized in zip(
            city_values,
            city_normalized
        ):
            if normalized not in city_groups:
                city_groups[normalized] = set()

            city_groups[normalized].add(original)

        for normalized, values in city_groups.items():

            if len(values) > 1:

                inconsistent_records.append({
                    "Field": "City",
                    "Normalized Value": normalized,
                    "Different Values": ", ".join(
                        sorted(values)
                    )
                })

    inconsistency_report = pd.DataFrame(
        inconsistent_records
    )

    # ==========================================
    # SAVE REPORTS
    # ==========================================

    missing_report.to_csv(
        "reports/missing_values.csv",
        index=False
    )

    invalid_report.to_csv(
        "reports/invalid_values.csv",
        index=False
    )

    inconsistency_report.to_csv(
        "reports/inconsistencies.csv",
        index=False
    )

    # ==========================================
    # PRINT RESULTS
    # ==========================================

    print("\n" + "=" * 60)
    print("DATA QUALITY ANALYSIS")
    print("=" * 60)

    print("\nMissing Values:")
    print(missing_report)

    print("\nDuplicate Rows:", duplicate_count)

    print("\nInvalid Records:")
    if len(invalid_report) > 0:
        print(invalid_report)
    else:
        print("No invalid records found.")

    print("\nCategorical Inconsistencies:")
    if len(inconsistency_report) > 0:
        print(inconsistency_report)
    else:
        print("No inconsistencies found.")

    print("\nReports saved in reports/")

    return {
        "missing": missing_report,
        "duplicates": duplicate_count,
        "invalid": invalid_report,
        "inconsistencies": inconsistency_report
    }