# Успеваемость студентов

Django-приложение для сохранения оценок в JSON/XML или SQLite. Записи из базы можно искать по имени студента, группе, предмету и преподавателю, редактировать и удалять. Дубликат — совпадение студента, группы, предмета, даты и преподавателя; оценка при этом не учитывается.

## Локальный запуск

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Откройте http://127.0.0.1:8000/. Для запуска тестов используйте `uv run python manage.py test`. Файлы хранятся в `storage/`, база — в `db.sqlite3`.

## Развёртывание на PythonAnywhere


### Шаг 1. В консоли bash выполните следующие команды:
```bash
# 1. Установите uv
pip install --user uv

# 2. Склонируйте проект и перейдите в него
git clone https://github.com/myuni-repos/web-lr-04-mysql.git
cd web-lr-04-mysql

# 3. Создайте .venv строго на Python 3.13 и поставьте пакеты из uv.lock
uv sync --python 3.13 --frozen

# 4. Подготовьте папку хранения, базу данных и статику
mkdir -p storage
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput

# 5. Сгенерируйте секретный ключ (скопируйте вывод из консоли для шага 2)
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Шаг 2. Создание web приложения в PythonAnywhere

1. Нажмите Add a new web app → Next → Manual configuration → выберите Python 3.13.
2. В разделе Virtualenv укажите полный путь с точкой перед venv:
/home/USERNAME/PROJECT/.venv
3. В разделе Static files добавьте строку:
	• URL: /static/
	• Directory: /home/USERNAME/PROJECT/staticfiles

### Шаг 3. Настройка запуска (файл WSGI)

Во вкладке Web откройте ссылку в строке WSGI configuration file, полностью удалите шаблонный код и вставьте свой (заменив USERNAME, PROJECT и вставив сгенерированный выше ключ):

```py
import os
import sys

project = '/home/USERNAME/PROJECT'
if project not in sys.path:
    sys.path.insert(0, project)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lr_04_mysql.settings'
os.environ['DJANGO_SECRET_KEY'] = 'ВСТАВЬТЕ-КЛЮЧ-ИЗ-ШАГА-1'
os.environ['DJANGO_DEBUG'] = 'false'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'USERNAME.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

```

### Шаг 4. Запуск и дальнейшие обновления

* Сохраните WSGI-файл (Ctrl+S или кнопка Save сверху) и нажмите зеленую кнопку Reload во вкладке Web. Сайт заработает по адресу https://pythonanywhere.com.
* Как обновлять сайт в будущем: зайдите в Bash-консоль в папку проекта, выполните `git pull && uv sync --frozen && uv run python manage.py migrate && uv run python manage.py collectstatic --noinput` и нажмите Reload во вкладке Web.
* Регулярно скачивайте резервные копии файла db.sqlite3 и папки storage/ через вкладку Files.