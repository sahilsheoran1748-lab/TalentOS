
import pandas as pd
from pathlib import Path

class IntegrationCentre:

    @staticmethod
    def validate_file(file_name):
        extension = Path(file_name).suffix.lower()
        return extension in [".csv", ".xlsx", ".xls"]

    @staticmethod
    def load_dataset(file):
        name = file.name.lower()

        if name.endswith(".csv"):
            return pd.read_csv(file)
        elif name.endswith((".xlsx", ".xls")):
            return pd.read_excel(file)

        raise ValueError("Unsupported file format")

    @staticmethod
    def inspect_dataset(df):
        return {
            "records": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "column_names": list(df.columns)
        }

    @staticmethod
    def clean_dataset(df, approved=False):
        if not approved:
            raise PermissionError(
                "Human approval is required before cleaning."
            )

        cleaned = df.drop_duplicates().copy()
        return cleaned
