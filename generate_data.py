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


def generate_baseline_data(n_samples=5000):
    np.random.seed(42)
    data = {
        "age": np.random.normal(loc=35, scale=10, size=n_samples),
        "income": np.random.normal(loc=50000, scale=15000, size=n_samples),
        "score": np.random.uniform(low=0, high=100, size=n_samples),
    }
    return pd.DataFrame(data)


def generate_target_data(n_samples=5000):
    np.random.seed(100)
    data = {
        "age": np.random.normal(loc=42, scale=12, size=n_samples),
        "income": np.random.normal(loc=65000, scale=18000, size=n_samples),
        "score": np.random.uniform(low=0, high=100, size=n_samples),
    }
    return pd.DataFrame(data)


def main():
    print("Генерация baseline данных...")
    df_baseline = generate_baseline_data()
    df_baseline.to_sql(
        "baseline_data",
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=500,
    )

    print("Генерация target данных...")
    df_target = generate_target_data()
    df_target.to_sql(
        "target_data",
        engine,
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=500,
    )

    print("Данные успешно сгенерированы и загружены в БД.")


if __name__ == "__main__":
    main()