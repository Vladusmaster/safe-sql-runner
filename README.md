# safe-sql-runner

Консольное приложение на Python принимает SQL-запросы, выполняет команды SELECT и автоматически добавляет LIMIT 5 если его нет.

## Установка
1. Клонируйте репозиторий.
2. Установите зависимости: `pip install -r requirements.txt`
3. Скопируйте `.env.example` в `.env` и укажите данные для подключения к вашей PostgreSQL.

## Запуск
```bash
python main.py
