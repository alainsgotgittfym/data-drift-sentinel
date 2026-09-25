Скрипт для проверки сдвига данных в Postgres. Сравнивает новую выборку с эталоном через тест кс и показывает, типо, шо поплыло.
Стек
Python, PostgreSQL 15 Docker, SQLAlchemy, Pandas, SciPy, dotenv

Как работает

Подтягивает из базы baseline_data и target_data.
Сравнивает распределения через ks_2samp.
При p-value < 0.05 фиксирует дрифт.
Выводит логи в консоль, сохраняет их в drift.log и закидывает итоговый результат в drift_report.json.

Запуск

Поднимаем базу: docker compose up -d
Накатываем тестовые данные: python generate_data.py
Запускаем проверку: python detect_drift.py