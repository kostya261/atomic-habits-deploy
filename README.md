# 🐍 Курсовая 5 Привычки

Курсовой проект по дисциплине "Программирование на Python". 
Веб-приложение для управления привычками.

## 🚀 Основные возможности

- **Управление получателями** - создание, редактирование, удаление списков рассылки
- **Создание сообщений** - шаблоны писем с темой и телом
- **Планирование рассылок** - настройка времени начала и окончания
- **Отслеживание отправок** - история попыток с статусами
- **Статистика** - детальная аналитика по рассылкам
- **Разграничение прав** - роли "пользователь" и "менеджер"
- **Кеширование** - серверное и клиентское для повышения производительности

## 📦 Установка и настройка


1. Клонируйте репозиторий:
   [ссылка](https://github.com/kostya261/Kursovay_4/pull/1)
   
3. Зависимости указанные в файле: *pyproject.toml*
```
[tool.poetry]
name = "atomic_habits"
version = "0.1.0"
description = ""
authors = ["Konstantin <kos26193@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.13"
django = "^5.0"
pillow = "^12.1.0"
djangorestframework = "^3.16.1"
python-dotenv = "^1.2.1"
django-filter = "^25.2"
djangorestframework-simplejwt = "^5.5.1"
drf-yasg = "^1.21.14"
stripe = "^14.3.0"
forex-python = "^1.9.2"
celery = "^5.6.2"
redis = "^7.1.0"
eventlet = "^0.40.4"
django-celery-beat = "^2.8.1"
poetry-core = "^2.3.1"
django-cors-headers = "^4.3.0"
psycopg2-binary = "^2.9.11"
psycopg = "^3.3.2"

[tool.poetry.group.lint.dependencies]
black = "^26.1.0"
flake8 = "^7.3.0"
isort = "^7.0.0"

[tool.poetry.group.dev.dependencies]
coverage = "^7.13.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"



```

## 📋 Модели данных

### Основные сущности:
- **Recipient** - получатель рассылки (клиент)
- **Message** - шаблон сообщения
- **Mailing** - рассылка с настройками времени
- **Attempt** - попытка отправки с результатом
- **UserStatistics** - статистика пользователя

### Пользователи:
- **CustomUser** - кастомная модель пользователя
- Роли: "user" (обычный) и "manager" (менеджер)

## Запуск
bash

### Django сервер
python manage.py runserver

### Celery worker (отдельный терминал)
celery -A config worker -l info --pool=solo

### Celery beat (отдельный терминал)
celery -A config beat -l info

## Настройка базы данных

### Создайте базу данных PostgreSQL
### Настройте .env файл (пример в .env.example)
### Отредактируйте .env с вашими настройками

### Миграции и суперпользователь

python manage.py migrate
python manage.py createsuperuser

### Загрузка тестовых данных

python manage.py loaddata users.json
python manage.py loaddata mailer.json

### Запуск сервера

python manage.py runserver

### Запуск Redis

redis-server



## 📱 Telegram Bot
Найди бота в Telegram по токену

Отправь /start
Получи свой chat_id через @userinfobot

Установи его в профиле:

text
PUT /api/users/telegram/
{
    "telegram_chat_id": "123456789"
}
✅ При создании привычки приходит уведомление
✅ За 10 минут до выполнения — напоминание

## 📚 API Документация
После запуска доступно:

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/


## Основные эндпоинты

### Метод	   URL	                        Описание
   POST	       /api/token/	                 Получить JWT токен
   POST	       /api/users/register/	         Регистрация
   GET	       /api/habits/	                 Список привычек
   POST	       /api/habits/	                 Создать привычку
   GET	       /api/habits/public/	         Публичные привычки
   POST	       /api/habits/{id}/complete/	 Отметить выполнение
   PUT	       /api/users/telegram/	         Установить Telegram ID


## Использование:

git clone <repository-url>
cd kursovaya_5


## 📁 Структура проекта
text
atomic_habits/
├── config/              # Настройки проекта
│   ├── settings.py      # Конфигурация
│   ├── celery.py        # Celery
│   └── urls.py          # Корневой роутинг
├── habits/              # Приложение привычек
│   ├── models.py        # Модель Habit
│   ├── serializers.py   # DRF сериализаторы
│   ├── views.py         # ViewSet'ы
│   ├── services.py      # Бизнес-логика, Telegram
│   ├── tasks.py         # Celery задачи
│   ├── validators.py    # Валидация ТЗ
│   └── tests.py         # 99% покрытие
├── users/               # Приложение пользователей
│   ├── models.py        # Кастомная модель User
│   ├── serializers.py   # Регистрация, профиль
│   └── views.py         # Эндпоинты
└── manage.py

👨‍💻 Автор
Константин

GitHub: https://github.com/kostya261

Email: kos261@yandex.ru


## Лицензия:
📄 Лицензия
Этот проект является курсовой работой и распространяется по лицензии MIT.В
