from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://sentinel_user:sentinel_password@localhost:5432/sentinel_db"

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            row = result.fetchone()
            print("Успешное подключение к PostgreSQL!")
            print(f"Версия БД: {row[0]}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_connection()