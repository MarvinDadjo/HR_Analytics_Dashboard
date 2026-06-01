"""
database.py
-----------
Loads hr_data.csv into a local SQLite database and exposes
pre-built analytical queries used by the Streamlit dashboard.

Columns: employee_id, first_name, last_name, gender, age, department,
         job_title, hire_date, tenure_years, salary, performance_score,
         satisfaction_score, absence_days, attrition, remote_work, education

Usage:
    from database import init_db, run_query
    df = run_query("attrition_by_department")
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "hr_analytics.db"
CSV_PATH = "hr_data.csv"


# ─────────────────────────────────────────
# Setup
# ─────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db(force: bool = False):
    """Load CSV into SQLite. Skip if DB already exists, unless force=True."""
    if Path(DB_PATH).exists() and not force:
        return

    df = pd.read_csv(CSV_PATH)
    con = get_connection()
    df.to_sql("employees", con, if_exists="replace", index=False)
    con.close()
    print(f"Database initialised — {len(df)} rows loaded into '{DB_PATH}'")


# ─────────────────────────────────────────
# Analytical queries
# ─────────────────────────────────────────

QUERIES = {

    "attrition_by_department": """
        SELECT
            department,
            COUNT(*)                                                AS total_employees,
            SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)     AS attritions,
            ROUND(
                100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1
            )                                                       AS attrition_rate_pct
        FROM employees
        GROUP BY department
        ORDER BY attrition_rate_pct DESC;
    """,

    "salary_by_department_gender": """
        SELECT
            department,
            gender,
            ROUND(AVG(salary), 0)  AS avg_salary,
            COUNT(*)               AS headcount
        FROM employees
        GROUP BY department, gender
        ORDER BY department, gender;
    """,

    "tenure_vs_attrition": """
        SELECT
            CAST(tenure_years AS INTEGER)                           AS tenure_years,
            COUNT(*)                                                AS total,
            SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)     AS attritions,
            ROUND(
                100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1
            )                                                       AS attrition_rate_pct
        FROM employees
        GROUP BY CAST(tenure_years AS INTEGER)
        ORDER BY tenure_years;
    """,

    "satisfaction_breakdown": """
        SELECT
            ROUND(satisfaction_score, 0)                            AS satisfaction_level,
            COUNT(*)                                                AS total,
            SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)     AS attritions,
            ROUND(
                100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1
            )                                                       AS attrition_rate_pct
        FROM employees
        GROUP BY ROUND(satisfaction_score, 0)
        ORDER BY satisfaction_level;
    """,

    "remote_work_impact": """
        SELECT
            remote_work,
            COUNT(*)                                                AS total,
            SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)     AS attritions,
            ROUND(
                100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1
            )                                                       AS attrition_rate_pct,
            ROUND(AVG(salary), 0)                                   AS avg_salary,
            ROUND(AVG(satisfaction_score), 2)                       AS avg_satisfaction
        FROM employees
        GROUP BY remote_work;
    """,

    "age_band_profile": """
        SELECT
            CASE
                WHEN age < 25 THEN '< 25'
                WHEN age < 35 THEN '25-34'
                WHEN age < 45 THEN '35-44'
                WHEN age < 55 THEN '45-54'
                ELSE '55+'
            END                                                     AS age_band,
            COUNT(*)                                                AS headcount,
            ROUND(AVG(salary), 0)                                   AS avg_salary,
            ROUND(AVG(tenure_years), 1)                             AS avg_tenure,
            SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)     AS attritions
        FROM employees
        GROUP BY age_band
        ORDER BY MIN(age);
    """,

    "high_flight_risk": """
        -- Current employees with highest cumulative attrition risk signals
        SELECT
            employee_id,
            first_name || ' ' || last_name                         AS full_name,
            department,
            job_title,
            age,
            ROUND(tenure_years, 1)                                  AS tenure_years,
            salary,
            ROUND(satisfaction_score, 1)                            AS satisfaction_score,
            absence_days,
            (
                CASE WHEN satisfaction_score < 2.5    THEN 2 ELSE 0 END +
                CASE WHEN tenure_years < 2             THEN 2 ELSE 0 END +
                CASE WHEN salary < 45000               THEN 1 ELSE 0 END +
                CASE WHEN absence_days > 10            THEN 1 ELSE 0 END +
                CASE WHEN performance_score < 2.5      THEN 1 ELSE 0 END
            )                                                       AS risk_score
        FROM employees
        WHERE attrition = 'No'
        ORDER BY risk_score DESC, salary ASC
        LIMIT 50;
    """,

    "gender_pay_gap_by_role": """
        SELECT
            job_title,
            ROUND(AVG(CASE WHEN gender = 'Male'   THEN salary END), 0) AS avg_male_salary,
            ROUND(AVG(CASE WHEN gender = 'Female' THEN salary END), 0) AS avg_female_salary,
            ROUND(
                100.0 * (
                    AVG(CASE WHEN gender = 'Male'   THEN salary END) -
                    AVG(CASE WHEN gender = 'Female' THEN salary END)
                ) / AVG(CASE WHEN gender = 'Male' THEN salary END)
            , 1)                                                        AS gap_pct
        FROM employees
        GROUP BY job_title
        HAVING avg_male_salary IS NOT NULL AND avg_female_salary IS NOT NULL
        ORDER BY ABS(gap_pct) DESC;
    """,

    "performance_vs_attrition": """
        SELECT
            ROUND(performance_score, 0)                             AS perf_level,
            COUNT(*)                                                AS total,
            SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END)     AS attritions,
            ROUND(
                100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1
            )                                                       AS attrition_rate_pct,
            ROUND(AVG(salary), 0)                                   AS avg_salary
        FROM employees
        GROUP BY ROUND(performance_score, 0)
        ORDER BY perf_level;
    """,

}


def run_query(name: str) -> pd.DataFrame:
    """Execute a named query and return a DataFrame."""
    if name not in QUERIES:
        raise ValueError(f"Unknown query: '{name}'. Available: {list(QUERIES.keys())}")
    con = get_connection()
    df = pd.read_sql_query(QUERIES[name], con)
    con.close()
    return df


def run_custom_query(sql: str) -> pd.DataFrame:
    """Execute an arbitrary SQL string and return a DataFrame."""
    con = get_connection()
    df = pd.read_sql_query(sql, con)
    con.close()
    return df


# ─────────────────────────────────────────
# CLI — run all queries for inspection
# ─────────────────────────────────────────

if __name__ == "__main__":
    init_db(force=True)
    for name in QUERIES:
        print(f"\n{'─'*50}")
        print(f"Query: {name}")
        print(run_query(name).to_string(index=False))
