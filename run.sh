#!/bin/sh
sleep 20
alembic upgrade head

# Запуск фоновой задачи
exec python src/main.py
exec uvicorn --reload --host 0.0.0.0 --port 8002 src/main.py

# Ожидание фоновой задачи
tail -f /dev/null
