import os
import pandas as pd
from dotenv import load_dotenv
from scipy.stats import ks_2samp
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def load_data():
    df_baseline = pd.read_sql("SELECT * FROM baseline_data", engine)
    df_target = pd.read_sql("SELECT * FROM target_data", engine)
    return df_baseline, df_target


def detect_drift(df_baseline, df_target, alpha=0.05):
    numerical_cols = ["age", "income", "score"]
    drift_results = {}

    print("\n--- Результаты анализа дрифта ---")

    for col in numerical_cols:
        stat, p_value = ks_2samp(df_baseline[col], df_target[col])
        has_drift = p_value < alpha

        drift_results[col] = {
            "statistic": round(stat, 4),
            "p_value": round(p_value, 5),
            "drift_detected": has_drift,
        }

        status = "Обнаружен дрифт" if has_drift else "Стабильно"
        print(f"Признак '{col}': {status} (p-value: {p_value:.5f})")

    return drift_results


def main():
    df_baseline, df_target = load_data()
    detect_drift(df_baseline, df_target)


if __name__ == "__main__":
    main()