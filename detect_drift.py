import json
import logging
import os
import pandas as pd
from dotenv import load_dotenv
from scipy.stats import ks_2samp
from sqlalchemy import create_engine

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("drift.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def load_data():
    logging.info("Чтение baseline и target таблиц из БД...")
    df_baseline = pd.read_sql("SELECT * FROM baseline_data", engine)
    df_target = pd.read_sql("SELECT * FROM target_data", engine)
    return df_baseline, df_target


def detect_drift(df_baseline, df_target, alpha=0.05):
    numerical_cols = ["age", "income", "score"]
    drift_results = {}

    logging.info("Запуск анализа дрифта...")

    for col in numerical_cols:
        stat, p_value = ks_2samp(df_baseline[col], df_target[col])
        has_drift = bool(p_value < alpha)

        drift_results[col] = {
            "statistic": round(float(stat), 4),
            "p_value": round(float(p_value), 5),
            "drift_detected": has_drift,
        }

        if has_drift:
            logging.warning(
                f"Признак '{col}': Обнаружен дрифт (p-value: {p_value:.5f})"
            )
        else:
            logging.info(f"Признак '{col}': Стабильно (p-value: {p_value:.5f})")

    return drift_results


def save_report(results, output_file="drift_report.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    logging.info(f"Отчет успешно сохранен в файл {output_file}")


def main():
    df_baseline, df_target = load_data()
    results = detect_drift(df_baseline, df_target)
    save_report(results)


if __name__ == "__main__":
    main()