
import uuid
import pandas as pd


class ActionIntelligenceEngine:

    def __init__(self):
        self.recommendations = []

    def add_recommendation(
        self, category, title, evidence,
        recommended_action, priority="MEDIUM"
    ):
        item = {
            "id": str(uuid.uuid4())[:8],
            "category": category,
            "title": title,
            "priority": priority,
            "evidence": evidence,
            "recommended_action": recommended_action,
            "status": "PENDING_REVIEW",
            "human_approval_required": True
        }

        self.recommendations.append(item)

    def generate_recommendations(
        self, employees, recruitment, monthly
    ):

        self.recommendations = []

        # 1. Department engagement comparison
        if "engagement_score" in employees.columns:

            dept = employees.groupby(
                "department"
            )["engagement_score"].mean().sort_values()

            if len(dept) >= 2:

                lowest = dept.index[0]
                highest = dept.index[-1]

                self.add_recommendation(
                    "Employee Intelligence",
                    "Department engagement comparison",
                    f"{lowest}: {dept.iloc[0]:.1f}; "
                    f"{highest}: {dept.iloc[-1]:.1f}",
                    "Review department-level feedback and "
                    "identify improvement opportunities."
                )

        # 2. Recruitment pipeline
        if "stage" in recruitment.columns:

            stage = recruitment["stage"].value_counts()

            self.add_recommendation(
                "Recruitment Intelligence",
                "Recruitment pipeline distribution",
                str(stage.to_dict()),
                "Review pipeline conversion and recruitment "
                "bottlenecks."
            )

        # 3. Financial intelligence
        required = {
            "revenue_inr",
            "payroll_cost_inr",
            "headcount",
            "training_budget_inr"
        }

        if required.issubset(monthly.columns):

            financial = monthly.copy()

            numeric_cols = [
                "revenue_inr",
                "payroll_cost_inr",
                "headcount",
                "training_budget_inr"
            ]

            for col in numeric_cols:
                financial[col] = pd.to_numeric(
                    financial[col], errors="coerce"
                )

            financial = financial.dropna(
                subset=numeric_cols
            )

            financial = financial[
                (financial["revenue_inr"] > 0) &
                (financial["headcount"] > 0) &
                (financial["payroll_cost_inr"] >= 0) &
                (financial["training_budget_inr"] >= 0)
            ]

            if not financial.empty:

                latest = financial.iloc[-1]

                revenue = float(latest["revenue_inr"])
                payroll = float(latest["payroll_cost_inr"])
                headcount = float(latest["headcount"])
                training = float(latest["training_budget_inr"])

                reporting_period = (
                    str(latest["month"])
                    if "month" in latest.index
                    else "Period not available"
                )

                payroll_ratio = payroll / revenue * 100
                revenue_per_employee = revenue / headcount
                training_ratio = training / revenue * 100

                # Payroll-to-revenue monitoring
                trend_text = "Previous month unavailable"

                if len(financial) >= 2:

                    previous = financial.iloc[-2]

                    previous_ratio = (
                        previous["payroll_cost_inr"] /
                        previous["revenue_inr"] * 100
                    )

                    difference = payroll_ratio - previous_ratio

                    if difference > 0:
                        trend_text = (
                            f"Increased by {difference:.2f} "
                            "percentage points"
                        )
                    elif difference < 0:
                        trend_text = (
                            f"Decreased by {abs(difference):.2f} "
                            "percentage points"
                        )
                    else:
                        trend_text = "Unchanged"

                self.add_recommendation(
                    "Financial Intelligence",
                    "Payroll-to-revenue monitoring",
                    f"Reporting month: {reporting_period}. "
                    f"Latest ratio: {payroll_ratio:.2f}%. "
                    f"Trend: {trend_text}.",
                    "Review workforce cost trends alongside "
                    "revenue performance before making "
                    "budget decisions.",
                    "MEDIUM" if payroll_ratio > 30 else "LOW"
                )

                # Revenue per employee
                self.add_recommendation(
                    "Financial Intelligence",
                    "Revenue per employee analysis",
                    f"Reporting month: {reporting_period}. "
                    f"Revenue per employee: "
                    f"INR {revenue_per_employee:,.2f}. "
                    f"Headcount: {int(headcount)}.",
                    "Compare revenue per employee across "
                    "months and departments before drawing "
                    "productivity conclusions.",
                    "LOW"
                )

                # Training investment
                self.add_recommendation(
                    "Financial Intelligence",
                    "Workforce training investment",
                    f"Reporting month: {reporting_period}. "
                    f"Training budget: INR {training:,.2f}. "
                    f"Training-to-revenue ratio: "
                    f"{training_ratio:.2f}%.",
                    "Review training investment alongside "
                    "workforce skill requirements and "
                    "business outcomes.",
                    "LOW"
                )

        return self.recommendations

    def get_summary(self):
        return {
            "total": len(self.recommendations),
            "pending_review": sum(
                x["status"] == "PENDING_REVIEW"
                for x in self.recommendations
            )
        }
