import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def generate_baseline_data(n_samples=1000):
    """Генерация эталонных данных (Baseline)"""
    np.random.seed(42)  

    age = np.random.normal(loc=35, scale=10, size=n_samples).clip(18, 70)
    income = np.random.normal(loc=50000, scale=15000, size=n_samples).clip(
        15000, 150000
    )
    score = np.random.uniform(1, 100, size=n_samples)

    df = pd.DataFrame(
        {
            "user_id": range(1, n_samples + 1),
            "age": np.round(age, 1),
            "income": np.round(income, 2),
            "score": np.round(score, 1),
        }
    )
    return df


def generate_drifted_data(n_samples=1000):
    """Генерация новых данных со сдвигом (Current/Drifted)"""
    np.random.seed(100)

    age = np.random.normal(loc=42, scale=12, size=n_samples).clip(18, 70)
    income = np.random.normal(loc=65000, scale=20000, size=n_samples).clip(
        15000, 200000
    )
    score = np.random.uniform(1, 100, size=n_samples)

    df = pd.DataFrame(
        {
            "user_id": range(1001, 1001 + n_samples),
            "age": np.round(age, 1),
            "income": np.round(income, 2),
            "score": np.round(score, 1),
        }
    )
    return df


def main():
    print("Генерация данных...")
    df_baseline = generate_baseline_data()
    df_target = generate_drifted_data()

    print("Запись baseline_data в базу данных...")
    df_baseline.to_sql(
        "baseline_data",
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=500,
    )

    print("Запись target_data в базу данных...")
    df_target.to_sql(
        "target_data",
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=500,
    )

    print("Данные успешно сгенерированы и сохранены в PostgreSQL!")


if __name__ == "__main__":
    main()