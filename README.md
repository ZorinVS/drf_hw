# LMS REST-API

## Описание

Платформа для онлайн-обучения, на которой каждый желающий может размещать свои полезные материалы или курсы.

### Выполнено

- Создан новый Django-проект и подключен DRF в настройках проекта
- Созданы модели `User`, `Course`, `Lesson`
- Описан CRUD для моделей курса и урока
- Реализован эндпоинт для редактирования профиля любого пользователя
- Работа каждого эндпоинта проверена с помощью Postman

## Зависимости

- Django 5.1.4
- djangorestframework 3.15.2
- pillow 11.0.0
- psycopg2-binary 2.9.10
- python-dotenv 1.0.1

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
