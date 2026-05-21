# Face Recognition System

Desktop-приложение для распознавания лиц, разработанное на Python.
Система позволяет выполнять идентификацию пользователей с использованием веб-камеры и технологий компьютерного зрения.

## Технологии

- Python
- PyQt5
- PostgreSQL
- OpenCV
- DeepFace
- MediaPipe
- NumPy
- bcrypt
- psycopg2

## Возможности

- Авторизация пользователей
- Распознавание лиц в реальном времени
- Работа с веб-камерой
- Хранение эмбеддингов лиц
- Работа с базой данных PostgreSQL

## Установка

### 1. Клонирование репозитория

git clone https://github.com/username/project.git

### 2. Создание виртуального окружения (опционально)

python -m venv venv

### 3. Активация окружения (опционально)

Windows:
venv\Scripts\activate

Linux:
source venv/bin/activate

### 4. Установка зависимостей

pip install -r requirements.txt

### 5. Создать файл .env и указать:

- DB_NAME=название БД
- DB_USER=пользователь БД
- DB_PASSWORD=пароль БД
- DB_HOST=хост БД
- DB_PORT=порт БД

# Скриншоты

### Окно авторизации

![Login](images/login.png)

### Главное окно

![Main](images/main.png)

### Окно добавления нового пользователя

![New_user](images/add_user.png)
