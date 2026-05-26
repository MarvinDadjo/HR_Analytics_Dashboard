import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────
# Page config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="HR Dashboard",
    page_icon="👥",
    layout="wide",
)

st.title("👥 HR Analytics Dashboard")
st.markdown("Workforce overview — interactive filters on the left sidebar.")

# ─────────────────────────────────────────
# Load data
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("hr_data.csv")
    df["hire_date"] = pd.to_datetime(df["hire_date"])
    return df

df = load_data()

# ─────────────────────────────────────────
# Sidebar filters
# ─────────────────────────────────────────
st.sidebar.header("Filters")

departments = st.sidebar.multiselect(
    "Department",
    options=sorted(df["department"].unique()),
    default=sorted(df["department"].unique()),
)

genders = st.sidebar.multiselect(
    "Gender",
    options=df["gender"].unique(),
    default=df["gender"].unique(),
)

remote_options = st.sidebar.multiselect(
    "Remote Work",
    options=df["remote_work"].unique(),
    default=df["remote_work"].unique(),
)

salary_range = st.sidebar.slider(
    "Salary range ($)",
    min_value=int(df["salary"].min()),
    max_value=int(df["salary"].max()),
    value=(int(df["salary"].min()), int(df["salary"].max())),
    step=1000,
)

# Apply filters
filtered = df[
    df["department"].isin(departments) &
    df["gender"].isin(genders) &
    df["remote_work"].isin(remote_options) &
    df["salary"].between(salary_range[0], salary_range[1])
]

# ─────────────────────────────────────────
# KPI cards — row 1
# ─────────────────────────────────────────
st.markdown("### Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

total_employees = len(filtered)
attrition_rate  = filtered["attrition"].eq("Yes").mean()
avg_salary      = filtered["salary"].mean()
avg_satisfaction = filtered["satisfaction_score"].mean()
avg_absence     = filtered["absence_days"].mean()

col1.metric("Total Employees",    f"{total_employees:,}")
col2.metric("Attrition Rate",     f"{attrition_rate:.1%}")
col3.metric("Avg Salary",         f"${avg_salary:,.0f}")
col4.metric("Avg Satisfaction",   f"{avg_satisfaction:.1f} / 10")
col5.metric("Avg Absence Days",   f"{avg_absence:.1f} days/yr")

st.divider()

# ─────────────────────────────────────────
# Row 2 — Headcount & Attrition by dept
# ─────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Headcount by Department")
    headcount = (
        filtered.groupby("department")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=True)
    )
    fig = px.bar(
        headcount,
        x="count", y="department",
        orientation="h",
        color="count",
        color_continuous_scale="Blues",
        labels={"count": "Employees", "department": ""},
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("#### Attrition Rate by Department")
    attrition_by_dept = (
        filtered.groupby("department")["attrition"]
        .apply(lambda x: x.eq("Yes").mean())
        .reset_index(name="attrition_rate")
        .sort_values("attrition_rate", ascending=True)
    )
    fig2 = px.bar(
        attrition_by_dept,
        x="attrition_rate", y="department",
        orientation="h",
        color="attrition_rate",
        color_continuous_scale="Reds",
        labels={"attrition_rate": "Attrition Rate", "department": ""},
        text=attrition_by_dept["attrition_rate"].map("{:.1%}".format),
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────
# Row 3 — Salary distribution & Gender pay
# ─────────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("#### Salary Distribution by Department")
    fig3 = px.box(
        filtered,
        x="department", y="salary",
        color="department",
        labels={"salary": "Annual Salary ($)", "department": ""},
    )
    fig3.update_layout(showlegend=False, xaxis_tickangle=-30, height=380)
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.markdown("#### Gender Pay Gap by Department")
    pay_gap = (
        filtered.groupby(["department", "gender"])["salary"]
        .mean()
        .reset_index(name="avg_salary")
    )
    fig4 = px.bar(
        pay_gap,
        x="department", y="avg_salary",
        color="gender",
        barmode="group",
        labels={"avg_salary": "Avg Salary ($)", "department": ""},
        color_discrete_map={"Male": "#4C9BE8", "Female": "#E87B4C"},
    )
    fig4.update_layout(xaxis_tickangle=-30, height=380)
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────
# Row 4 — Performance & Satisfaction
# ─────────────────────────────────────────
col_left3, col_right3 = st.columns(2)

with col_left3:
    st.markdown("#### Performance Score Distribution")
    perf_counts = (
        filtered["performance_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    perf_counts.columns = ["score", "count"]
    perf_labels = {1: "1 - Poor", 2: "2 - Below Avg", 3: "3 - Average", 4: "4 - Good", 5: "5 - Excellent"}
    perf_counts["label"] = perf_counts["score"].map(perf_labels)
    fig5 = px.pie(
        perf_counts,
        names="label", values="count",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.4,
    )
    fig5.update_layout(height=350)
    st.plotly_chart(fig5, use_container_width=True)

with col_right3:
    st.markdown("#### Satisfaction vs Attrition")
    fig6 = px.histogram(
        filtered,
        x="satisfaction_score",
        color="attrition",
        barmode="overlay",
        opacity=0.75,
        labels={"satisfaction_score": "Satisfaction Score (1-10)", "attrition": "Left company"},
        color_discrete_map={"Yes": "#E84C4C", "No": "#4CBE8A"},
    )
    fig6.update_layout(height=350)
    st.plotly_chart(fig6, use_container_width=True)

# ─────────────────────────────────────────
# Row 5 — Hiring trend
# ─────────────────────────────────────────
st.markdown("#### Hiring Trend Over Time")
hiring_trend = (
    filtered.set_index("hire_date")
    .resample("QS")["employee_id"]
    .count()
    .reset_index()
    .rename(columns={"hire_date": "quarter", "employee_id": "new_hires"})
)
fig7 = px.area(
    hiring_trend,
    x="quarter", y="new_hires",
    labels={"quarter": "Quarter", "new_hires": "New Hires"},
    color_discrete_sequence=["#4C9BE8"],
)
fig7.update_layout(height=300)
st.plotly_chart(fig7, use_container_width=True)

# ─────────────────────────────────────────
# Raw data table (collapsible)
# ─────────────────────────────────────────
with st.expander("🔍 View raw employee data"):
    st.dataframe(
        filtered.drop(columns=["first_name", "last_name"]),
        use_container_width=True,
        height=300,
    )
