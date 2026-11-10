
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "synthetic"
REPORT_DIR = BASE_DIR / "reports"

st.set_page_config(
    page_title="TalentOS | Workforce Intelligence",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():

    employees = pd.read_csv(DATA_DIR / "employee_master.csv")
    recruitment = pd.read_csv(DATA_DIR / "recruitment_pipeline.csv")
    monthly = pd.read_csv(DATA_DIR / "monthly_workforce_metrics.csv")

    return employees, recruitment, monthly

employees, recruitment, monthly = load_data()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("TalentOS")
st.sidebar.caption("Workforce Intelligence Platform")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Employee Intelligence",
        "Recruitment Intelligence",
        "Financial Intelligence",
        "ROI Calculator",
        "Hiring Simulator",
        "Data Trust Centre",
        "Integration & Migration Centre",
        "Cold-Start Onboarding Wizard",
        "Action Intelligence Centre"
    ]
)

st.sidebar.divider()
st.sidebar.caption("DEMONSTRATION EDITION")
st.sidebar.caption("Company: Nexora Technologies")
st.sidebar.caption("Version: 1.0.0")

# -----------------------------
# EXECUTIVE OVERVIEW
# -----------------------------

if page == "Executive Overview":

    st.title("Executive Overview")
    st.caption("Company-wide workforce intelligence dashboard")

    total_employees = len(employees)
    departments = employees["department"].nunique()
    payroll = employees["annual_salary_inr"].sum()
    avg_engagement = employees["engagement_score"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Employees", f"{total_employees:,}")
    c2.metric("Departments", departments)
    c3.metric("Annual Salary Base", f"₹{payroll/10000000:.2f} Cr")
    c4.metric("Average Engagement", f"{avg_engagement:.1f}/100")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Department Distribution")

        dept_data = employees["department"].value_counts().reset_index()
        dept_data.columns = ["Department", "Employees"]

        fig = px.pie(
            dept_data,
            names="Department",
            values="Employees",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Workforce Location")

        location_data = employees["location"].value_counts().reset_index()
        location_data.columns = ["Location", "Employees"]

        fig = px.bar(
            location_data,
            x="Location",
            y="Employees",
            text="Employees"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Workforce Trends")

    fig = px.line(
        monthly,
        x="month",
        y=["headcount", "new_hires", "exits"],
        markers=True,
        title="Headcount, Hires and Exits"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# EMPLOYEE INTELLIGENCE
# -----------------------------

elif page == "Employee Intelligence":

    st.title("Employee Intelligence")
    st.caption("Explore workforce composition and skills")

    departments = ["All"] + sorted(employees["department"].unique())

    selected_department = st.selectbox(
        "Select Department",
        departments
    )

    filtered = employees.copy()

    if selected_department != "All":
        filtered = filtered[
            filtered["department"] == selected_department
        ]

    c1, c2, c3 = st.columns(3)

    c1.metric("Employees", len(filtered))

    c2.metric(
        "Average Salary",
        f"₹{filtered['annual_salary_inr'].mean():,.0f}"
    )

    c3.metric(
        "Average Performance",
        f"{filtered['performance_rating'].mean():.2f}/5"
    )

    st.subheader("Employee Records")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Skills Distribution")

    skill_counts = (
        filtered["skills"]
        .str.split(", ")
        .explode()
        .value_counts()
        .reset_index()
    )

    skill_counts.columns = ["Skill", "Frequency"]

    fig = px.bar(
        skill_counts.head(12),
        x="Skill",
        y="Frequency",
        title="Most Frequently Listed Skills"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# RECRUITMENT INTELLIGENCE
# -----------------------------

elif page == "Recruitment Intelligence":

    st.title("Recruitment Intelligence")

    total_applications = len(recruitment)
    hired = (recruitment["stage"] == "Hired").sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("Applications", total_applications)
    c2.metric("Hired Records", int(hired))
    c3.metric(
        "Average Pipeline Days",
        f"{recruitment['days_in_pipeline'].mean():.1f}"
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Recruitment Pipeline")

        stage_data = recruitment["stage"].value_counts().reset_index()
        stage_data.columns = ["Stage", "Applications"]

        fig = px.bar(
            stage_data,
            x="Stage",
            y="Applications"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Application Sources")

        source_data = recruitment["source"].value_counts().reset_index()
        source_data.columns = ["Source", "Applications"]

        fig = px.pie(
            source_data,
            names="Source",
            values="Applications",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recruitment Records")

    st.dataframe(
        recruitment,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# FINANCIAL INTELLIGENCE
# -----------------------------

elif page == "Financial Intelligence":

    st.title("Workforce Financial Intelligence")

    total_revenue = monthly["revenue_inr"].sum()
    total_payroll = monthly["payroll_cost_inr"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("12-Month Revenue", f"₹{total_revenue/10000000:.2f} Cr")
    c2.metric("12-Month Payroll", f"₹{total_payroll/10000000:.2f} Cr")
    c3.metric(
        "Revenue / Employee",
        f"₹{(total_revenue/monthly['headcount'].mean()):,.0f}"
    )

    st.subheader("Monthly Revenue and Payroll")

    fig = px.line(
        monthly,
        x="month",
        y=["revenue_inr", "payroll_cost_inr"],
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Financial Records")

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# ROI CALCULATOR
# -----------------------------

elif page == "ROI Calculator":

    st.title("ROI Calculator")
    st.caption("Estimate potential benefits using your own assumptions.")

    st.info(
        "This is a scenario calculator. It does not represent "
        "verified TalentOS customer savings."
    )

    col1, col2 = st.columns(2)

    with col1:
        annual_hr_cost = st.number_input(
            "Annual HR operational cost (₹)",
            min_value=0,
            value=5000000,
            step=100000
        )

        time_saving = st.slider(
            "Estimated time saving (%)",
            0, 80, 20
        )

    with col2:
        implementation_cost = st.number_input(
            "Estimated annual platform cost (₹)",
            min_value=0,
            value=500000,
            step=50000
        )

        other_savings = st.number_input(
            "Other estimated annual savings (₹)",
            min_value=0,
            value=200000,
            step=50000
        )

    estimated_savings = (
        annual_hr_cost * time_saving / 100
    ) + other_savings

    net_benefit = estimated_savings - implementation_cost

    roi = (
        net_benefit / implementation_cost * 100
        if implementation_cost > 0 else None
    )

    st.divider()

    a, b, c = st.columns(3)

    a.metric(
        "Estimated Annual Savings",
        f"₹{estimated_savings:,.0f}"
    )

    b.metric(
        "Estimated Net Benefit",
        f"₹{net_benefit:,.0f}"
    )

    c.metric(
        "Estimated ROI",
        f"{roi:.1f}%" if roi is not None else "N/A"
    )

    st.caption(
        "Formula: ROI = (Estimated Savings - Platform Cost) "
        "/ Platform Cost × 100"
    )

# -----------------------------
# HIRING SIMULATOR
# -----------------------------

elif page == "Hiring Simulator":

    st.title("What-If Hiring Simulator")

    st.caption("Explore hypothetical hiring and budget scenarios.")

    current_headcount = st.number_input(
        "Current Headcount",
        min_value=0,
        value=500
    )

    planned_hires = st.number_input(
        "Additional Planned Hires",
        min_value=0,
        value=25
    )

    average_salary = st.number_input(
        "Average Annual Salary per New Hire (₹)",
        min_value=0,
        value=800000,
        step=50000
    )

    recruitment_cost = st.number_input(
        "Recruitment Cost per Hire (₹)",
        min_value=0,
        value=30000,
        step=5000
    )

    additional_headcount = current_headcount + planned_hires

    annual_salary_budget = planned_hires * average_salary

    recruitment_budget = planned_hires * recruitment_cost

    total_first_year_budget = (
        annual_salary_budget + recruitment_budget
    )

    st.divider()

    a, b, c = st.columns(3)

    a.metric("Projected Headcount", f"{additional_headcount:,}")

    b.metric(
        "Annual Salary Budget",
        f"₹{annual_salary_budget:,.0f}"
    )

    c.metric(
        "First-Year Hiring Budget",
        f"₹{total_first_year_budget:,.0f}"
    )

    st.warning(
        "Illustrative scenario only. Taxes, benefits, "
        "salary increments and other costs are excluded."
    )

# -----------------------------
# DATA TRUST CENTRE
# -----------------------------

elif page == "Data Trust Centre":

    st.title("Data Trust Centre")

    report_file = REPORT_DIR / "data_trust_report.csv"
    summary_file = REPORT_DIR / "data_trust_summary.json"

    if report_file.exists():

        report = pd.read_csv(report_file)

        st.subheader("Dataset Quality Assessment")

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        overall_score = report["data_quality_score"].mean()

        st.metric(
            "Overall Data Quality Score",
            f"{overall_score:.1f}/100"
        )

        st.progress(
            min(max(float(overall_score) / 100, 0), 1)
        )

        st.download_button(
            "Download Data Trust Report",
            data=report.to_csv(index=False),
            file_name="TalentOS_Data_Trust_Report.csv",
            mime="text/csv"
        )

    else:
        st.error("Data Trust report not found.")

    st.caption(
        "The displayed score uses the initial demonstration "
        "scoring methodology."
    )



# -----------------------------
# INTEGRATION & MIGRATION CENTRE
# -----------------------------

elif page == "Integration & Migration Centre":

    from src.modules.integration_centre import IntegrationCentre

    st.title("Integration & Migration Centre")
    st.caption("Connect, inspect and prepare workforce datasets.")

    st.info("Use synthetic or non-confidential data only.")

    uploaded = st.file_uploader(
        "Upload CSV or Excel dataset",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded is not None:

        try:
            df = IntegrationCentre.load_dataset(uploaded)

            st.subheader("Dataset Preview")
            st.dataframe(df.head(20), use_container_width=True)

            quality = IntegrationCentre.inspect_dataset(df)

            a, b, c, d = st.columns(4)
            a.metric("Records", quality["records"])
            b.metric("Columns", quality["columns"])
            c.metric("Missing Values", quality["missing_values"])
            d.metric("Duplicates", quality["duplicate_rows"])

            approved = st.checkbox(
                "Approve removal of exact duplicate rows"
            )

            if st.button("Process Dataset"):

                cleaned = IntegrationCentre.clean_dataset(
                    df, approved=approved
                )

                st.session_state["processed_dataset"] = cleaned
                st.success("Dataset processing completed.")

            if "processed_dataset" in st.session_state:

                result = st.session_state["processed_dataset"]

                st.dataframe(result.head(20))

                st.download_button(
                    "Download Processed CSV",
                    result.to_csv(index=False),
                    "TalentOS_Processed_Dataset.csv",
                    "text/csv"
                )

        except Exception as e:
            st.error(str(e))

    st.warning(
        "Demonstration supports upload, inspection and duplicate "
        "removal. Full schema mapping and migration history remain "
        "under development."
    )


# -----------------------------
# COLD-START ONBOARDING WIZARD
# -----------------------------

elif page == "Cold-Start Onboarding Wizard":

    from src.modules.onboarding_engine import OnboardingEngine

    st.title("Cold-Start Onboarding Wizard")
    st.caption("Organisation workforce-data readiness assessment.")

    organisation = st.text_input(
        "Organisation Name",
        value="Nexora Technologies"
    )

    if st.button("Calculate Readiness"):

        engine = OnboardingEngine()
        result = engine.calculate_readiness(employees)

        st.session_state["onboarding_result"] = result
        st.session_state["onboarding_org"] = organisation

    if "onboarding_result" in st.session_state:

        result = st.session_state["onboarding_result"]

        st.subheader(st.session_state["onboarding_org"])

        a, b, c = st.columns(3)

        a.metric(
            "Readiness Score",
            f'{result["readiness_score"]}/100'
        )

        b.metric(
            "Required Columns",
            f'{result["required_columns_found"]}/'
            f'{result["required_columns_total"]}'
        )

        c.metric("Status", result["status"])

        st.progress(result["readiness_score"] / 100)

        st.write("Missing Values:", result["missing_values"])
        st.write("Duplicate Rows:", result["duplicate_rows"])

        st.caption("Illustrative demonstration readiness score.")


# -----------------------------
# ACTION INTELLIGENCE CENTRE
# -----------------------------

elif page == "Action Intelligence Centre":

    from src.modules.action_intelligence import ActionIntelligenceEngine

    st.title("Action Intelligence Centre")
    st.caption("Evidence-backed recommendations with human review.")

    if st.button("Generate Recommendations"):

        engine = ActionIntelligenceEngine()

        recommendations = engine.generate_recommendations(
            employees, recruitment, monthly
        )

        st.session_state["action_recommendations"] = recommendations

    recommendations = st.session_state.get(
        "action_recommendations", []
    )

    for item in recommendations:

        key = "review_" + item["id"]

        if key not in st.session_state:
            st.session_state[key] = "PENDING_REVIEW"

        with st.container(border=True):

            st.subheader(item["title"])

            st.write("Priority:", item["priority"])
            st.write("Evidence:", item["evidence"])
            st.write("Recommended Action:", item["recommended_action"])
            st.write("Status:", st.session_state[key])

            if st.session_state[key] == "PENDING_REVIEW":

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Approve", key="approve_" + item["id"]):
                        st.session_state[key] = "APPROVED"
                        st.rerun()

                with col2:
                    if st.button("Reject", key="reject_" + item["id"]):
                        st.session_state[key] = "REJECTED"
                        st.rerun()

    st.warning(
        "Review decisions are session-only demonstration records, "
        "not persistent production audit logs."
    )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "TalentOS V1.0 | Complete Demonstration Edition | "
    "Synthetic data | Not for production use"
)
