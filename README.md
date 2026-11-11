# DjangoStudyProject

Учебный проект на Django 6.0: приложение `main` с двумя страницами.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Открыть http://127.0.0.1:8000/

Переменные окружения (необязательно): `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` (`1`/`0`), `DJANGO_ALLOWED_HOSTS` (через запятую).
