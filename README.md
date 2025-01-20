# LMS REST-API

## Описание

Платформа для онлайн-обучения, на которой каждый желающий может размещать свои полезные материалы или курсы.

### Выполнено

- Подключена и настроена документация проекта (использован пакет `drf-yasg`)
- Добавлена возможность оплаты курсов через Stripe
- Реализована проверка статуса платежа
- Написаны тесты

## Зависимости

- coverage==7.6.10
- Django 5.1.4
- django-filter 24.3
- djangorestframework 3.15.2
- djangorestframework-simplejwt 5.3.1
- drf-yasg 1.21.8
- ipython 8.31.0
- pillow 11.0.0
- psycopg2-binary 2.9.10
- python-dotenv 1.0.1
- stripe 11.4.1

## Установка

1. Клонируйте репозиторий:
```bash
git clone git@github.com:ZorinVS/drf_hw.git
```
2. Установите зависимости:
```bash
pip3 install -r requirements.txt
```

## Подключение БД
1. Создайте БД
2. Создайте файл `.env` из файла `.env.sample`

## Применение миграций
```bash
python manage.py migrate
```

## Создание суперпользователя
- С помощью менеджера:
```bash
python3 manage.py createsuperuser
```

## Запуск
1. В командной строке: `python3 manage.py runserver`

## Наполнение данными
```bash
python3 manage.py fill_lms
```
## Отчета о покрытии кода тестами

### Шаг 1: Сбор данных о покрытии
Запуск тестов с измерением покрытия кода:
```bash
coverage run --source='.' manage.py test
```

### Шаг 2: Генерация текстового отчёта
Создание текстового отчёта:
```bash
coverage report
```

### Результат выполнения команд
| Name                                                                      | Stmts | Miss | Cover |
|---------------------------------------------------------------------------|-------|------|-------|
| config/__init__.py                                                        |     0 |    0 |  100% |
| config/asgi.py                                                            |     4 |    4 |    0% |
| config/settings.py                                                        |    31 |    0 |  100% |
| config/urls.py                                                            |    11 |    0 |  100% |
| config/wsgi.py                                                            |     4 |    4 |    0% |
| lms/__init__.py                                                           |     0 |    0 |  100% |
| lms/admin.py                                                              |    14 |    0 |  100% |
| lms/apps.py                                                               |     4 |    0 |  100% |
| lms/management/__init__.py                                                |     0 |    0 |  100% |
| lms/management/commands/__init__.py                                       |     0 |    0 |  100% |
| lms/management/commands/fill_lms.py                                       |    17 |   17 |    0% |
| lms/migrations/0001_initial.py                                            |     5 |    0 |  100% |
| lms/migrations/0002_course_owner.py                                       |     6 |    0 |  100% |
| lms/migrations/0003_lesson_owner.py                                       |     6 |    0 |  100% |
| lms/migrations/0004_subscription.py                                       |     6 |    0 |  100% |
| lms/migrations/0005_alter_lesson_options.py                               |     4 |    0 |  100% |
| lms/migrations/__init__.py                                                |     0 |    0 |  100% |
| lms/models.py                                                             |    34 |    3 |   91% |
| lms/paginators.py                                                         |     5 |    0 |  100% |
| lms/serializers.py                                                        |    27 |    0 |  100% |
| lms/services.py                                                           |    10 |    2 |   80% |
| lms/tests.py                                                              |   159 |    0 |  100% |
| lms/urls.py                                                               |     8 |    0 |  100% |
| lms/validators.py                                                         |    11 |    0 |  100% |
| lms/views.py                                                              |    71 |    9 |   87% |
| manage.py                                                                 |    11 |    2 |   82% |
| users/__init__.py                                                         |     0 |    0 |  100% |
| users/admin.py                                                            |    11 |    0 |  100% |
| users/apps.py                                                             |     4 |    0 |  100% |
| users/migrations/0001_initial.py                                          |     6 |    0 |  100% |
| users/migrations/0002_payment.py                                          |     6 |    0 |  100% |
| users/migrations/0003_alter_payment_options.py                            |     4 |    0 |  100% |
| users/migrations/0004_payment_link_payment_session_id_payment_status.py   |     4 |    0 |  100% |
| users/migrations/__init__.py                                              |     0 |    0 |  100% |
| users/models.py                                                           |    56 |   16 |   71% |
| users/permissions.py                                                      |    19 |    2 |   89% |
| users/serializers.py                                                      |    26 |    5 |   81% |
| users/services.py                                                         |    40 |    5 |   88% |
| users/tests.py                                                            |    53 |    0 |  100% |
| users/urls.py                                                             |     7 |    0 |  100% |
| users/views.py                                                            |    74 |   12 |   84% |
| **TOTAL**                                                                 |   758 |   81 |   89% |
