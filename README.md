# blog-async-pg
Учебный проект.

### Используемые технологии
* Python 3.11
* PostgreSQL
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic

### Интерфейс приложения
* /signup - регистрация пользователя
* /auth - аутентификация пользователя
* /users/me - информация о текущем пользователе

### Рабочие заметки

За основу взята статья 
["Пишем веб сервис на Python с помощью FastAPI"](https://habr.com/ru/articles/513328/)
[исходники](https://github.com/NeverWalkAloner/async-blogs)

**Создать базу данных.**
> CREATE DATABASE blog_async;

В консоли PostgreSQL выполнить команду 
(для генерации uuid функцией uuid_generate_v4()):
> CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

Это действие тоже можно сделать через миграции.

Статья ["Как генерируются UUID"](https://habr.com/ru/companies/vk/articles/522094/)

**Установить необходимые пакеты:**
> pip install sqlalchemy
>
> pip install psycopg2
> 
> pip install alembic

Подготовить файлы с описанием таблиц с помощью sqlalchemy, 
к этим файлам будет отсылка из migrations\env.py.

Инициализировать Alembic 
(будет создан alembic.ini и каталог migrations с содержимым):
> alembic init migrations

В alembic.ini указать url базы:
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:5432/%(DB_NAME)s

Переопределить файл migrations\env.py.

Сгенерировать файл миграции:
> alembic revision --autogenerate -m "Added required tables"

Обновить БД (применить файл миграции):
> alembic upgrade head
