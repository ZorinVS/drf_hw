# LMS REST-API

## Описание

Платформа для онлайн-обучения, на которой каждый желающий может размещать свои полезные материалы или курсы.

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
2. Создайте файл `.env` из файла `.env.sample`
3. Соберите и запустите контейнеры:
   
   Команда собирает и запускает контейнеры, применяет миграции и запускает проект:
   ```shell
   docker-compose up -d --build
   ```

## Повторный запуск проекта

```shell
docker-compose up -d
```

## Проверка работоспособности каждого сервиса

### Приложение LMS REST-API (Django)

После запуска проекта, приложение будет доступно по адресу http://localhost:8000. 
Чтобы проверить, что сервис работает правильно, откройте этот URL в браузере.

### База данных (PostgreSQL)

Чтобы проверить, что PostgreSQL работает, выполните:

```shell
docker-compose exec db pg_isready -U "$(echo $POSTGRES_USER)"
```

### Redis

Чтобы проверить работу Redis, выполните команду:
```shell
docker-compose exec redis redis-cli ping
```

### Celery

Для проверки работы Celery, выполните:

```shell
docker-compose exec celery celery -A config status
```

### Celery Beat

Для проверки работы Celery Beat, выполните:
```shell
docker-compose logs celery_beat
```

## Отчета о покрытии кода тестами

### Шаг 1: Сбор данных о покрытии
Запуск тестов с измерением покрытия кода:
```shell
docker-compose exec app coverage run --source='.' manage.py test
```

### Шаг 2: Генерация текстового отчёта
Создание текстового отчёта:
```shell
docker-compose exec app coverage report
```
