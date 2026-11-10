
class OnboardingEngine:

    REQUIRED_COLUMNS = [
        "employee_id",
        "department",
        "job_title",
        "hire_date",
        "annual_salary_inr"
    ]

    def calculate_readiness(self, df):

        profile_score = 25
        dataset_score = 25

        available = [
            col for col in self.REQUIRED_COLUMNS
            if col in df.columns
        ]

        column_score = (
            len(available) / len(self.REQUIRED_COLUMNS)
        ) * 25

        missing = int(df.isna().sum().sum())
        duplicates = int(df.duplicated().sum())

        quality_score = 25 if missing == 0 and duplicates == 0 else 0

        total = (
            profile_score
            + dataset_score
            + column_score
            + quality_score
        )

        return {
            "readiness_score": round(total, 1),
            "required_columns_found": len(available),
            "required_columns_total": len(self.REQUIRED_COLUMNS),
            "missing_values": missing,
            "duplicate_rows": duplicates,
            "status": "READY" if total >= 80 else "REVIEW REQUIRED"
        }
