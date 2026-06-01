# HR Analytics Dashboard

> **Python · Streamlit · SQLite · Pandas · Plotly**

Interactive HR analytics dashboard tracking attrition, salary equity, and workforce risk across departments. Powered by a local SQLite database with 8 pre-built analytical queries.

---

## Dashboard Preview

![Dashboard Preview](screenshots/dashboard_preview.png)

---

## Business Problem

HR teams often rely on static spreadsheets with no real-time filtering or cross-dimensional analysis. This dashboard replaces that workflow with an interactive tool that answers the key questions:

- Which departments and roles have the highest attrition risk?
- Is there a measurable gender pay gap by job role?
- Who are the employees most likely to leave in the next 6 months?
- Does overtime correlate with higher attrition — and at what cost?

---

## Features

| Dashboard Section | Description |
|---|---|
| **KPI Cards** | Total headcount, attrition rate, avg salary, gender split |
| **Attrition by Department** | Bar chart with rates per department |
| **Salary by Department & Gender** | Pay gap visualisation |
| **Tenure vs Attrition** | Line chart — when do employees leave? |
| **Satisfaction Breakdown** | Attrition rate by job satisfaction score |
| **Overtime Impact** | Attrition and salary split by overtime status |
| **Age Band Profile** | Headcount, salary and tenure by age group |
| **Flight Risk Table** | Top 50 current employees with highest risk score |
| **Gender Pay Gap by Role** | Gap % per job title, ranked by magnitude |

---

## Database Layer (SQLite)

All dashboard queries run against a local SQLite database (`hr_analytics.db`) loaded from `hr_data.csv`.  
The `database.py` module exposes 8 named queries and a `run_custom_query()` function for ad-hoc analysis.

```python
from database import init_db, run_query

init_db()                                  # creates hr_analytics.db
df = run_query("attrition_by_department")  # returns a pandas DataFrame
df = run_query("high_flight_risk")         # top 50 flight risk employees
df = run_query("gender_pay_gap_by_role")   # pay gap % by job title
```

### Available Named Queries

| Query name | Description |
|---|---|
| `attrition_by_department` | Headcount, attritions, rate % per department |
| `salary_by_department_gender` | Avg salary split by dept × gender |
| `tenure_vs_attrition` | Attrition rate by years at company |
| `satisfaction_breakdown` | Attrition rate by job satisfaction level |
| `overtime_impact` | Attrition and salary split by overtime |
| `age_band_profile` | Headcount, salary, tenure, attritions by age band |
| `high_flight_risk` | Top 50 current employees with composite risk score |
| `gender_pay_gap_by_role` | Pay gap % per job title, ranked |

### Flight Risk Scoring

Employees currently at the company are scored on 5 signals:

```sql
risk_score =
    CASE WHEN OverTime = 'Yes'        THEN 2 ELSE 0 END +
    CASE WHEN JobSatisfaction <= 2    THEN 2 ELSE 0 END +
    CASE WHEN YearsAtCompany <= 2     THEN 1 ELSE 0 END +
    CASE WHEN MonthlyIncome < 3500    THEN 1 ELSE 0 END +
    CASE WHEN WorkLifeBalance <= 2    THEN 1 ELSE 0 END
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data storage | SQLite (via `sqlite3` + `database.py`) |
| Data manipulation | Python, Pandas |
| Dashboard | Streamlit |
| Visualisation | Plotly |

---

## Run Locally

```bash
git clone https://github.com/MarvinDadjo/hr-analytics-dashboard.git
cd hr-analytics-dashboard

pip install -r requirements.txt

# Initialise the SQLite database
python database.py

# Launch the dashboard
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
hr-analytics-dashboard/
├── app.py           # Streamlit dashboard
├── database.py      # SQLite setup + 8 named analytical queries
├── hr_data.csv      # Source dataset (600 employees)
├── requirements.txt
├── screenshots/
│   └── dashboard_preview.png
└── README.md
```

---

## Author

**Marvin Dadjo** — Data Analyst  
[LinkedIn](https://linkedin.com/in/marvindadjo) · [GitHub](https://github.com/MarvinDadjo) · marvindadjo21@gmail.com
