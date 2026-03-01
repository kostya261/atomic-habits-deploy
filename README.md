# 🐍 Atomic Habits - Трекер полезных привычек

Веб-приложение для управления полезными привычками с Telegram-напоминаниями. Проект разработан в рамках курсовой работы по дисциплине "Программирование на Python".

## 🚀 Демо
**Сервер:** http://130.193.56.47  
**Админка:** http://130.193.56.47/admin  
**Документация API:** http://130.193.56.47/swagger/

---

## 📋 Содержание
- [О проекте](#о-проекте)
- [Технологии](#технологии)
- [Локальный запуск](#локальный-запуск)
- [Запуск через Docker](#запуск-через-docker)
- [CI/CD и деплой](#cicd-и-деплой)
- [Настройка сервера](#настройка-сервера)
- [Переменные окружения](#переменные-окружения)
- [Команды для работы](#команды-для-работы)

---

## 📝 О проекте

**Atomic Habits** - это трекер привычек, вдохновленный книгой Джеймса Клира "Атомные привычки". Приложение позволяет:


- Создавать полезные и приятные привычки
- Настраивать периодичность выполнения (ежедневно, через день, еженедельно)
- Получать напоминания в Telegram за 10 минут до выполнения
- Отслеживать прогресс и серии выполнения (streak)
- Делиться публичными привычками с другими пользователями

---

## 🛠 Технологии

### Backend
- **Python 3.13**
- **Django 5.2** + **Django REST Framework**
- **PostgreSQL 15** - основная БД
- **Redis 7** - брокер сообщений для Celery
- **Celery** - асинхронные задачи (напоминания)
- **JWT** - аутентификация

### Инфраструктура
- **Docker** + **Docker Compose** - контейнеризация
- **Nginx** - reverse proxy и раздача статики
- **GitHub Actions** - CI/CD
- **Yandex Cloud** - удаленный сервер

### Мониторинг и качество
- **Flake8** - линтинг
- **Black** - форматирование
- **Unittest** - тестирование

---

## 💻 Локальный запуск

### Предварительные требования
- Python 3.13+
- Poetry (рекомендуется) или pip
- PostgreSQL (или SQLite для разработки)
- Redis (опционально, для Celery)

## Шаг 1: Клонирование репозитория

[ссылка](https://github.com/kostya261/atomic-habits-deploy/pull/5)

git clone https://github.com/kostya261/atomic-habits-deploy/pull/5
cd kursovaya_5
git checkout itogovoe


## Шаг 2: Настройка виртуального окружения

### Установка зависимостей через poetry
poetry install

### Или через pip
python -m venv venv
source venv/bin/activate  # для Linux/Mac
### venv\Scripts\activate  # для Windows
pip install -r requirements.txt


## Шаг 3: Переменные окружения
Создайте файл .env в корне проекта:

.env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

### База данных (для SQLite закомментируйте PostgreSQL)
DB_NAME=habits_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

### Redis и Celery
REDIS_HOST=localhost
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

### Telegram
TELEGRAM_BOT_TOKEN=your-bot-token

### Email для админки
EMAIL_HOST_USER=your-email@yandex.ru
EMAIL_HOST_PASSWORD=your-password

## Шаг 4: Применение миграций и запуск

### Применить миграции
python manage.py migrate

### Создать суперпользователя
python manage.py createsuperuser

### Загрузить тестовые данные (опционально)
python manage.py loaddata users.json
python manage.py loaddata habits.json

### Запустить сервер
python manage.py runserver

### Шаг 5: Запуск Celery (для напоминаний)

## В отдельном терминале
celery -A config worker -l info
celery -A config beat -l info
Приложение будет доступно: http://localhost:8000


🐳 Запуск через Docker
Требования
Docker

Docker Compose

# Шаг 1: Настройка переменных окружения
Создайте файл .env аналогично локальному запуску, но измените хосты:

.env
DB_HOST=db
REDIS_HOST=redis
ALLOWED_HOSTS=localhost,127.0.0.1,web
# Шаг 2: Запуск контейнеров

## Сборка и запуск всех сервисов
docker-compose up -d --build

## Просмотр логов
docker-compose logs -f
### Шаг 3: Создание суперпользователя

docker-compose exec web python manage.py createsuperuser
### Шаг 4: Проверка работоспособности

## Проверка контейнеров
docker-compose ps

## Проверка логов
docker-compose logs web
docker-compose logs nginx

## Проверка статики
curl -I http://localhost/static/admin/css/base.css
Приложение будет доступно: http://localhost

🔄 CI/CD и деплой
Структура CI/CD пайплайна
В проекте настроен GitHub Actions workflow (.github/workflows/deploy.yml), который состоит из двух этапов:

1. Тестирование (test)
При пуше в ветки itogovoe, develop, main запускаются:

Линтинг кода (flake8, black)

Тесты Django

Проверка совместимости зависимостей

2. Деплой (deploy)
При пуше в ветки itogovoe или develop автоматически:

Копирует файлы на сервер через SCP

Создает .env файл с секретами

Пересобирает и перезапускает Docker-контейнеры (zero-downtime деплой)

Очищает старые Docker-образы

Настройка GitHub Secrets
Для работы CI/CD необходимо добавить следующие секреты в GitHub репозиторий (Settings → Secrets and variables → Actions):

Secret	Описание
SERVER_HOST	IP-адрес сервера (например, 130.193.56.47)
SERVER_USER	Имя пользователя на сервере (test)
SSH_PRIVATE_KEY	Приватный SSH-ключ для подключения
SECRET_KEY	Django секретный ключ
DB_NAME	Имя базы данных
DB_USER	Пользователь БД
DB_PASSWORD	Пароль БД
TELEGRAM_BOT_TOKEN	Токен Telegram бота
EMAIL_HOST_USER	Email для отправки
EMAIL_HOST_PASSWORD	Пароль от email
STRIPE_API_KEY	API ключ Stripe
ALLOWED_HOSTS	Разрешенные хосты (IP сервера)

# 🖥 Настройка сервера (Yandex Cloud)
## Шаг 1: Создание ВМ
Создайте виртуальную машину на Yandex Cloud с Ubuntu 22.04/24.04

Назначьте публичный IP-адрес

Откройте порты в firewall:

22 (SSH)
80 (HTTP)
443 (HTTPS, опционально)

## Шаг 2: Подключение к серверу и установка Docker
bash
ssh test@<IP-адрес-сервера>

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
# Выйти и зайти заново (или выполнить: newgrp docker)
Шаг 3: Настройка SSH для GitHub Actions
bash
# На локальном компьютере создать SSH-ключ
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github-actions

# Скопировать публичный ключ на сервер
ssh-copy-id -i ~/.ssh/github-actions.pub test@<IP-адрес-сервера>

# Проверить подключение
ssh -i ~/.ssh/github-actions test@<IP-адрес-сервера>

# Скопировать приватный ключ для GitHub Secrets
cat ~/.ssh/github-actions
# Всё содержимое (включая -----BEGIN и -----END) скопировать в секрет SSH_PRIVATE_KEY
Шаг 4: Настройка firewall (UFW)
bash
# Включить UFW и открыть порты
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Проверить статус
sudo ufw status
🔐 Переменные окружения
Полный список переменных окружения, используемых в проекте:

Переменная	Описание	Пример
SECRET_KEY	Секретный ключ Django	django-insecure-...
DEBUG	Режим отладки	False (в продакшене)
ALLOWED_HOSTS	Разрешенные хосты	130.193.56.47,localhost
DB_NAME	Имя БД	habits_db
DB_USER	Пользователь БД	postgres
DB_PASSWORD	Пароль БД	your-password
DB_HOST	Хост БД	db (в Docker) / localhost
DB_PORT	Порт БД	5432
REDIS_HOST	Хост Redis	redis (в Docker) / localhost
TELEGRAM_BOT_TOKEN	Токен Telegram бота	8295278310:...
EMAIL_HOST_USER	Email для отправки	money261@yandex.ru
EMAIL_HOST_PASSWORD	Пароль от email	app-password
STRIPE_API_KEY	API ключ Stripe	sk_test_...


# 📦 Структура проекта

atomic-habits/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD конфигурация
├── config/                      # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── habits/                      # Приложение привычек
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tasks.py                 # Celery задачи
├── users/                        # Приложение пользователей
│   ├── models.py
│   └── views.py
├── static/                       # Статические файлы
├── media/                         # Загруженные файлы
├── Dockerfile                     # Сборка Django приложения
├── docker-compose.yml             # Оркестрация контейнеров
├── nginx.conf                      # Конфигурация Nginx
├── pyproject.toml                  # Зависимости Poetry
├── poetry.lock
└── README.md                       # Документация


# 🛠 Команды для работы
Локальная разработка
bash
### Запуск тестов
python manage.py test

### Линтинг
flake8 .
black .

### Создание миграций
python manage.py makemigrations

### Применение миграций
python manage.py migrate
Docker
bash
### Сборка и запуск
docker-compose up -d --build

### Просмотр логов
docker-compose logs -f [service]

### Остановка
docker-compose down

### Полная остановка с удалением томов
docker-compose down -v

### Перезапуск конкретного сервиса
docker-compose restart web

### Зайти в контейнер
docker-compose exec web bash
Деплой (автоматически через GitHub Actions)
bash
### Просто запушить изменения в ветку itogovoe или develop
git add .
git commit -m "Описание изменений"
git push origin itogovoe
✅ Критерии выполнения
Все сервисы в отдельных контейнерах (Django, PostgreSQL, Redis, Celery, Nginx)

Используется docker-compose для оркестрации

Настроен CI/CD через GitHub Actions с тестированием и линтингом

Автоматический деплой на удаленный сервер

Подробная документация в README

Адрес сервера указан: http://130.193.56.47

Все изменения в Git, игнорируемые файлы в .gitignore

# 👨‍💻 Автор
Константин

GitHub: @kostya261

Email: kos261@yandex.ru

# 📄 Лицензия
Проект выполнен в рамках учебной программы и распространяется по лицензии MIT.