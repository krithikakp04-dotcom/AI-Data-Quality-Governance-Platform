import pandas as pd
import os


def generate_governance_recommendations(df, quality_results, quality_score):

    os.makedirs("reports", exist_ok=True)

    recommendations = []

    # ==========================================
    # 1. MISSING DATA
    # ==========================================

    missing = quality_results["missing"]

    for _, row in missing.iterrows():

        if row["Missing Values"] > 0:

            recommendations.append({
                "Issue Type": "Missing Data",
                "Column": row["Column"],
                "Issue": f'{row["Missing Values"]} missing value(s)',
                "Recommendation":
                    "Impute missing values or collect the missing information.",
                "Priority": "High"
            })

    # ==========================================
    # 2. DUPLICATE DATA
    # ==========================================

    duplicate_count = quality_results["duplicates"]

    if duplicate_count > 0:

        recommendations.append({
            "Issue Type": "Duplicate Data",
            "Column": "All Columns",
            "Issue": f"{duplicate_count} duplicate row(s)",
            "Recommendation":
                "Remove duplicate records and enforce unique record identifiers.",
            "Priority": "High"
        })

    # ==========================================
    # 3. INVALID VALUES
    # ==========================================

    invalid = quality_results["invalid"]

    if len(invalid) > 0:

        invalid_columns = ", ".join(
            invalid["Column"].unique()
        )

        recommendations.append({
            "Issue Type": "Invalid Data",
            "Column": invalid_columns,
            "Issue": f"{len(invalid)} invalid record(s)",
            "Recommendation":
                "Validate values using business rules and acceptable ranges.",
            "Priority": "High"
        })

    # ==========================================
    # 4. CATEGORICAL INCONSISTENCY
    # ==========================================

    inconsistencies = quality_results["inconsistencies"]

    if len(inconsistencies) > 0:

        inconsistent_columns = ", ".join(
            inconsistencies["Field"].unique()
        )

        recommendations.append({
            "Issue Type": "Inconsistency",
            "Column": inconsistent_columns,
            "Issue": "Different representations of the same category",
            "Recommendation":
                "Standardize categorical values using a common format.",
            "Priority": "Medium"
        })

    # ==========================================
    # 5. OVERALL QUALITY
    # ==========================================

    overall_score = quality_score["overall_score"]

    if overall_score < 75:

        recommendations.append({
            "Issue Type": "Overall Quality",
            "Column": "Dataset",
            "Issue":
                f"Overall quality score is {overall_score:.2f}%",
            "Recommendation":
                "Perform data cleansing before using the dataset for analysis or ML.",
            "Priority": "High"
        })

    # ==========================================
    # CREATE REPORT
    # ==========================================

    governance_report = pd.DataFrame(
        recommendations
    )

    governance_report.to_csv(
        "reports/governance_recommendations.csv",
        index=False
    )

    # ==========================================
    # PRINT RESULTS
    # ==========================================

    print("\n" + "=" * 60)
    print("DATA GOVERNANCE RECOMMENDATIONS")
    print("=" * 60)

    if len(governance_report) > 0:

        print(governance_report.to_string(index=False))

    else:

        print("No governance issues detected.")

    print(
        "\nReport saved to:",
        "reports/governance_recommendations.csv"
    )

    return governance_report