# Успеваемость студентов

Django-приложение для сохранения оценок в JSON/XML или SQLite. Записи из базы можно искать по имени студента, группе, предмету и преподавателю, редактировать и удалять. Дубликат — совпадение студента, группы, предмета, даты и преподавателя; оценка при этом не учитывается.

## Локальный запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Откройте http://127.0.0.1:8000/. Для запуска тестов используйте `python manage.py test`. Файлы хранятся в `storage/`, база — в `db.sqlite3`.

## Развёртывание на PythonAnywhere

1. Загрузите проект на GitHub, клонируйте его на PythonAnywhere и создайте виртуальное окружение с Python версии, совместимой с `requirements.txt`. Установите зависимости и выполните `python manage.py migrate`.
2. Создайте веб-приложение с ручной настройкой и укажите виртуальное окружение. В WSGI-конфигурации добавьте путь к проекту в `sys.path` и задайте переменные окружения до импорта приложения:

   ```python
   import os
   import sys

   project = '/home/USERNAME/PROJECT'
   if project not in sys.path:
       sys.path.insert(0, project)
   os.environ['DJANGO_SETTINGS_MODULE'] = 'lr_03_django_xml_json.settings'
   os.environ['DJANGO_SECRET_KEY'] = 'УСТАНОВИТЕ-ДЛИННЫЙ-СЛУЧАЙНЫЙ-СЕКРЕТ'
   os.environ['DJANGO_DEBUG'] = 'false'
   os.environ['DJANGO_ALLOWED_HOSTS'] = 'USERNAME.pythonanywhere.com'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

3. Замените `USERNAME`, `PROJECT` и секрет своими значениями. Для генерации секрета можно выполнить `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Не публикуйте его в репозитории.
4. Выполните `python manage.py collectstatic` и настройте отображение URL `/static/` на каталог `PROJECT/staticfiles` в разделе Web. Перезапустите веб-приложение. Каталоги проекта, `storage/` и файл SQLite должны быть доступны для записи; регулярно сохраняйте их резервные копии.

Это учебное приложение не ограничивает редактирование и удаление записей пользователями сайта. Перед публичным использованием добавьте авторизацию и проверьте настройки безопасности Django.
