# HR Analytics Dashboard

An interactive HR analytics dashboard built with Python and Streamlit, designed to give HR teams and business stakeholders a clear view of workforce health.

## Live Demo

> Clone the repo and run locally — instructions below.

![Dashboard Preview](screenshots/dashboard_preview.png)

---

## What This Project Does

This dashboard turns raw HR data into actionable insights across 7 departments and 600 employee records. It covers the key questions any HR team actually cares about:

- Where is attrition the highest, and why?
- Is there a gender pay gap, and how large is it?
- Which departments are understaffed or overpaying?
- How has hiring evolved over time?
- Are low satisfaction scores predictive of turnover?

---

## Features

| Section | Description |
|---|---|
| **KPI Cards** | Headcount, attrition rate, avg salary, satisfaction, absence days |
| **Headcount by Department** | Horizontal bar chart with color gradient |
| **Attrition by Department** | Ranked by rate with % labels |
| **Salary Distribution** | Box plots per department showing spread and outliers |
| **Gender Pay Gap** | Side-by-side avg salary comparison by gender per department |
| **Performance Distribution** | Donut chart across 5 performance tiers |
| **Satisfaction vs Attrition** | Overlapping histogram showing correlation |
| **Hiring Trend** | Quarterly area chart from 2015 to 2024 |
| **Raw Data Table** | Filterable and collapsible employee-level view |

All charts respond to the sidebar filters (department, gender, remote work type, salary range) in real time.

---

## Tech Stack

- **Python 3.11**
- **Streamlit** — dashboard framework
- **Pandas** — data manipulation
- **Plotly Express** — interactive charts
- **NumPy** — dataset generation

---

## Dataset

`hr_data.csv` — 600 synthetic employee records with realistic distributions:

| Column | Description |
|---|---|
| `employee_id` | Unique identifier |
| `department` | One of 7 departments |
| `job_title` | Seniority-based title per department |
| `salary` | Annual salary in USD |
| `performance_score` | 1 (poor) to 5 (excellent) |
| `satisfaction_score` | Self-reported score, 1 to 10 |
| `attrition` | Whether the employee left (Yes/No) |
| `absence_days` | Annual absences |
| `tenure_years` | Years since hire date |
| `remote_work` | Full Remote / Hybrid / On-site |
| `gender` | Male / Female |
| `education` | High School to PhD |

The dataset includes intentional patterns (gender pay gap ~8%, higher attrition for low performers, satisfaction-attrition correlation) to make the analysis meaningful.

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/MarvinDadjo/hr-analytics-dashboard.git
cd hr-analytics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
hr-analytics-dashboard/
├── app.py                  # Main Streamlit application
├── hr_data.csv             # HR dataset (600 employees)
├── generate_dataset.py     # Script used to generate the dataset
├── requirements.txt        # Python dependencies
├── screenshots/
│   └── dashboard_preview.png
└── README.md
```

---

## Key Insights From the Data

- **Customer Support** shows the highest attrition rate (~28%) despite being the lowest-paid department
- A **~6-8% gender pay gap** is visible across most departments, most pronounced in Engineering
- Employees with a satisfaction score below **4/10** leave at 3x the rate of those above 7
- **60% of hires** between 2015-2024 stayed beyond 3 years — concentrated in Engineering and Operations

---

## Author

**Marvin Dadjo** — Data Analyst  
[LinkedIn](https://linkedin.com/in/marvindadjo) · [GitHub](https://github.com/MarvinDadjo) · marvindadjo21@gmail.com
