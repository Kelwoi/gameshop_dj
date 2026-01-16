# Django Game Store (навчальний проект)

Фічі:
- Головна сторінка зі списком ігор
- Пагінація
- Фільтрація (категорія, платформа, ціна, "в наявності")
- Пошук по назві/опису
- Стандартна адмін-панель Django для керування товарами/категоріями
- Профіль користувача (створення/редагування)

## Швидкий старт

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Відкрий:
- Головна: http://127.0.0.1:8000/
- Адмінка: http://127.0.0.1:8000/admin/
- Реєстрація: http://127.0.0.1:8000/accounts/signup/
- Профіль: http://127.0.0.1:8000/accounts/profile/
