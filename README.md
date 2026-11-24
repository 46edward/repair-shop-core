# Repair Shop Core

Модульное backend-ядро системы управления сервисным центром на Python 3.13 и SQLAlchemy 2.0. Дальнейшие возможности: подключения внешних интерфейсов (CLI, Telegram-бот, API/дашборд).

## Архитектура моего проекта

Проект разделён на:

* `src/models/`
* `src/repositories/` — слой доступа к БД
* `src/services/`
* `src/exceptions.py`
* `src/database.py`
* `alembic/` — миграции схемы базы данных.
* `tests/` — unit и интеграционные тесты на pytest

## Стек моего проекта

* **Язык:** Python 3.13
* **ORM и миграции:** SQLAlchemy 2.0, Alembic
* **Тестирование:** pytest
* **Качество кода:** ruff, mypy
* **CI:** GitHub Actions
