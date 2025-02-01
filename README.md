# LMS REST-API

## Описание

Платформа для онлайн-обучения, на которой каждый желающий может размещать свои полезные материалы или курсы.

### Выполнено

- Настроен проект для работы с Celery
- Реализована асинхронная рассылка писем пользователям
- Добавлена проверка на отправку уведомлений
- Реализована фоновая задача для блокировки неактивных пользователей

## Зависимости

- celery 5.4.0
- coverage 7.6.10
- Django 5.1.4
- django-celery-beat 2.7.0
- django-filter 24.3
- djangorestframework 3.15.2
- djangorestframework-simplejwt 5.3.1
- drf-yasg 1.21.8
- ipython 8.31.0
- pillow 11.0.0
- psycopg2-binary 2.9.10
- python-dotenv 1.0.1
- redis 5.2.1
- stripe 11.4.1

## Установка

1. Клонируйте репозиторий:
   ```shell
   git clone git@github.com:ZorinVS/drf_hw.git
   ```
2. Установите зависимости:
   ```shell
   pip3 install -r requirements.txt
   ```

## Подключение БД
1. Создайте БД
2. Создайте файл `.env` из файла `.env.sample`

## Применение миграций
```shell
python manage.py migrate
```

## Создание суперпользователя
- С помощью менеджера:
   ```shell
   python3 manage.py createsuperuser
   ```

## Запуск
1. Запустите сервер Django:
   ```shell
   python3 manage.py runserver
   ```
2. Запустите брокер Redis:
   ```shell
   redis-server
   ```
3. Запустите Celery worker с планировщиком Celery beat:
   ```shell
   celery -A config worker --beat --scheduler django --loglevel=info
   ```

## Наполнение данными
```shell
python3 manage.py fill_lms
```
## Отчета о покрытии кода тестами

### Шаг 1: Сбор данных о покрытии
Запуск тестов с измерением покрытия кода:
```shell
coverage run --source='.' manage.py test
```

### Шаг 2: Генерация текстового отчёта
Создание текстового отчёта:
```shell
coverage report
```
