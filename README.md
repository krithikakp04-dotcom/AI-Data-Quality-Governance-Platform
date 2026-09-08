# AI-Powered Data Quality & Governance Platform

## Project Overview

The **AI-Powered Data Quality & Governance Platform** is a Python-based data analytics and governance application designed to identify, analyze, and monitor data-quality problems.

The platform detects common data-quality issues such as missing values, duplicate records, invalid values, categorical inconsistencies, and unusual records. It also calculates an overall data-quality score and generates governance recommendations.

A Streamlit dashboard provides an interactive interface for analyzing datasets and viewing the results.

---

## Project Details

**Project Topic:** AI-Powered Data Quality & Governance Platform

**Student Name:** Krithika K P

**Registered Email ID:** [krithikakp04@gmail.com](mailto:krithikakp04@gmail.com)

---

## Objectives

The main objectives of this project are:

* Detect missing values in datasets.
* Identify duplicate records.
* Detect invalid values using predefined rules.
* Identify inconsistent categorical values.
* Detect unusual records using machine learning.
* Calculate an overall data-quality score.
* Generate data-governance recommendations.
* Monitor data-quality changes over multiple analysis runs.
* Provide downloadable data-quality reports.
* Provide an interactive Streamlit dashboard.

---

## Key Features

### 1. Data Ingestion

The system reads datasets from CSV files and records basic ingestion information such as:

* Source file
* Number of rows
* Number of columns
* Ingestion date and time
* Ingestion status

The ingestion information is stored in:

`reports/ingestion_log.csv`

---

### 2. Data Quality Analysis

The platform analyzes the dataset for:

* Missing values
* Duplicate records
* Invalid age values
* Negative income values
* Categorical inconsistencies

The generated reports include:

* `missing_values.csv`
* `invalid_values.csv`
* `inconsistencies.csv`

---

### 3. AI-Based Anomaly Detection

The project uses the **Isolation Forest** machine-learning algorithm to identify unusual records.

Numerical features are standardized before anomaly detection, and missing numerical values are handled using median imputation.

The anomaly results are stored in:

`reports/anomaly_records.csv`

---

### 4. Data Quality Scoring

The platform calculates scores for four dimensions:

* Missing Data Score
* Duplicate Data Score
* Validity Score
* Consistency Score

These scores are combined to calculate the overall data-quality score.

The quality level is classified as:

| Score      | Quality Level     |
| ---------- | ----------------- |
| 90% – 100% | Excellent         |
| 75% – 89%  | Good              |
| 50% – 74%  | Needs Improvement |
| Below 50%  | Poor              |

The result is stored in:

`reports/quality_score.csv`

---

### 5. Data Governance

Detected quality problems are converted into actionable governance recommendations.

Issues are assigned priorities such as:

* High
* Medium
* Low

Examples of recommendations include:

* Imputing missing values.
* Removing duplicate records.
* Validating values using business rules.
* Standardizing categorical values.
* Performing data cleansing before analysis or machine learning.

The recommendations are stored in:

`reports/governance_recommendations.csv`

---

### 6. Continuous Monitoring

The monitoring module records the quality score for each analysis run.

It identifies whether data quality is:

* Improving
* Declining
* Stable
* Initial Run

The monitoring history is stored in:

`reports/quality_monitoring.csv`

---

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard with the following modules:

### 📋 Overview

Displays:

* Total rows
* Total columns
* Missing values
* Duplicate rows
* Detected anomalies
* Overall quality score
* Dataset preview
* Numerical statistics

### 🔍 Data Quality

Displays:

* Missing-value analysis
* Duplicate records
* Invalid values
* Categorical inconsistencies
* Visualizations

### 🤖 Anomaly Detection

Displays:

* Total records
* Normal records
* Anomalies
* Anomaly rate
* Anomaly distribution
* Detected anomalous records
* Isolation Forest methodology

### 📈 Quality Score

Displays:

* Overall quality score
* Quality level
* Individual quality metrics
* Score visualization
* Score interpretation

### 🛡️ Governance

Displays:

* High-priority issues
* Medium-priority issues
* Low-priority issues
* Governance recommendations
* Recommended actions

### 📊 Monitoring

Displays:

* Current quality score
* Quality level
* Quality trend
* Historical quality scores
* Score changes between runs

---

## Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn
* Streamlit

### Machine Learning

* Isolation Forest
* StandardScaler

### Data Format

* CSV

---

## Project Structure

```text
AI_Data_Quality_Governance/
│
├── app.py
├── dashboard.py
├── data_ingestion.py
├── data_quality.py
├── anomaly_detection.py
├── quality_scoring.py
├── governance.py
├── monitoring.py
│
├── dataset.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── reports/
    ├── ingestion_log.csv
    ├── missing_values.csv
    ├── invalid_values.csv
    ├── inconsistencies.csv
    ├── anomaly_records.csv
    ├── quality_score.csv
    ├── governance_recommendations.csv
    └── quality_monitoring.csv
```

---

## Installation

Clone the repository or download the project files.

Open a terminal inside the project folder.

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Run the Data Analysis

```bash
python app.py
```

This performs:

1. Data ingestion
2. Data-quality analysis
3. Anomaly detection
4. Quality scoring
5. Governance recommendation generation
6. Quality monitoring

---

### Run the Streamlit Dashboard

```bash
streamlit run dashboard.py
```

The Streamlit dashboard will open in the browser.

Upload a CSV dataset from the sidebar or use the default `dataset.csv`.

Then click:

**🔄 Run Analysis**

to perform the complete analysis.

---

## Sample Dataset

The project includes a sample customer dataset containing intentionally introduced data-quality problems such as:

* Missing age values
* Duplicate customer records
* Negative income values
* Invalid age values
* Inconsistent city representations

This allows the platform to demonstrate its data-quality detection capabilities.

---

## Generated Reports

The platform automatically generates CSV reports inside the `reports` folder.

| Report                           | Purpose                                |
| -------------------------------- | -------------------------------------- |
| `ingestion_log.csv`              | Records dataset ingestion              |
| `missing_values.csv`             | Identifies missing values              |
| `invalid_values.csv`             | Identifies invalid records             |
| `inconsistencies.csv`            | Identifies categorical inconsistencies |
| `anomaly_records.csv`            | Stores detected anomalies              |
| `quality_score.csv`              | Stores quality scores                  |
| `governance_recommendations.csv` | Stores recommended actions             |
| `quality_monitoring.csv`         | Stores quality-monitoring history      |

---

## Workflow

```text
CSV Dataset
     ↓
Data Ingestion
     ↓
Data Quality Analysis
     ↓
 ┌───────────────┬──────────────────┐
 ↓               ↓                  ↓
Missing       Invalid          Inconsistent
Values        Values             Values
     └───────────────┬──────────────┘
                     ↓
             Anomaly Detection
                     ↓
             Quality Scoring
                     ↓
          Governance Recommendations
                     ↓
            Continuous Monitoring
                     ↓
             Streamlit Dashboard
                     ↓
              Download Reports
```

---

## Expected Outcome

The platform provides an end-to-end solution for data-quality assessment and governance.

It helps users understand the health of a dataset, identify problematic records, detect anomalies using machine learning, quantify overall data quality, and receive actionable recommendations for improving the dataset.

---

## Conclusion

The **AI-Powered Data Quality & Governance Platform** demonstrates how Python, data analytics, machine learning, and dashboarding can be combined to build an automated data-quality management system.

The project provides a practical workflow for detecting data problems, evaluating data quality, recommending corrective actions, and continuously monitoring dataset health.
