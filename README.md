# mini_online_store# Mini Online Store API

## Описание

Этот проект представляет собой API для мини интернет-магазина с регистрацией, аутентификацией по логину/паролю и использованием JWT-токенов для аутентификации.

## Установка

1. Клонируйте репозиторий:
    ```
    git clone <URL>
    ```

2. Перейдите в директорию проекта:
    ```
    cd mini_online_store
    ```

3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```

4. Примените миграции:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Запустите сервер разработки:
    ```
    python manage.py runserver
    ```

## Настройки базы данных

DB_ENGINE: Движок базы данных, который будет использоваться. Например, django.db.backends.postgresql.
DB_NAME: Имя базы данных, используемой вашим приложением. Например, postgres.
POSTGRES_USER: Имя пользователя базы данных. Например, postgres.
POSTGRES_PASSWORD: Пароль для подключения к базе данных. Например, password12345.
DB_HOST: Хост, на котором работает база данных. Например, db для Docker контейнера или localhost для локальной установки.
DB_PORT: Порт, на котором работает база данных. Например, 5432.

## Настройки электронной почты

EMAIL_HOST_PASSWORD: Пароль для почтового сервера(создано с помощью "Пароль для приложения")
EMAIL_HOST_USER: Электронная почта, используемая для отправки писем. Например, forprogrammerstuff@gmail.com.
EMAIL_HOST: Хост почтового сервера. Например, smtp.gmail.com.
DEFAULT_FROM_EMAIL: Электронная почта по умолчанию для отправки писем. Например, forprogrammerstuff@gmail.com.
EMAIL_PORT: Порт для подключения к почтовому серверу. Например, 587.

# API Endpoints

### Регистрация

 ### Регистрация нового пользователя.

- **URL:** `/register/`
- **Метод:** `POST`
- **Тело запроса:**
    ```json
    {
        "email": "example@mail.com",
        "username": "exampleuser",
        "password": "yourpassword"
    }
    ```
- **Пример ответа:**
    ```json
    {
        "message": "Registration successful. Please check your email to confirm your account."
    }
    ```

### Вход

 ### Аутентификация пользователя с выдачей JWT-токенов.

- **URL:** `/login/`
- **Метод:** `POST`
- **Заголовки:**
    - `Content-Type: application/json`
- **Тело запроса:**
    ```json
    {
        "email": "example@mail.com",
        "password": "yourpassword"
    }
    ```
- **Пример ответа:**
    ```json
    {
        "refresh": "your_refresh_token_here",
        "access": "your_access_token_here"
    }
    ```

### После получения токенов

Используйте `access` токен для аутентификации в последующих запросах, добавляя его в заголовок `Authorization`.

- **Заголовок:** 
    - `Authorization: Bearer your_access_token_here`

Пример запроса с токеном:

- **URL:** `/some-protected-endpoint/`
- **Метод:** `GET`
- **Заголовки:**
    - `Authorization: Bearer your_access_token_here`

### Выход

- **URL:** `/logout/`
- **Метод:** `POST`
- **Заголовки:**
    - `Content-Type: application/json`
    - `Authorization: Bearer your_access_token_here`
- **Тело запроса:**
    ```json
    {
        "refresh": "your_refresh_token_here",  // Опционально
        "blacklist": true  // Опционально, по умолчанию false
    }
    ```
- **Пример ответа:**
    ```json
    {
        "message": "Logout successful"
    }
    ```

## API продуктов

 ### Создание продукта

- **URL:** `/products/`
- **Метод:** `POST`
- **Заголовки:**
    - `Content-Type: application/json`
- **Тело запроса:**
    ```json
    {
        "name": "Smartphone",
        "regular_price": "700.00",
        "discount_price": "650.00",
        "stock": 100,
        "description": "A new smartphone",
        "categories": [1, 2]
    }
    ```
- **Пример ответа:**
    ```json
    {
        "id": 1,
        "name": "Smartphone",
        "regular_price": "700.00",
        "discount_price": "650.00",
        "stock": 100,
        "description": "A new smartphone",
        "categories": [1, 2]
    }
    ```

### Получение списка продуктов

- **URL:** `/products/`
- **Метод:** `GET`
- **Заголовки:**
    - `Content-Type: application/json`
- **Пример ответа:**
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Smartphone",
                "regular_price": "700.00",
                "discount_price": "650.00",
                "stock": 100,
                "description": "A new smartphone",
                "categories": [1, 2]
            }
        ]
    }
    ```

### Обновление продукта

- **URL:** `/products/{product_id}/`
- **Метод:** `PUT`
- **Заголовки:**
    - `Content-Type: application/json`
- **Тело запроса:**
    ```json
    {
        "name": "Smartphone",
        "regular_price": "700.00",
        "discount_price": "600.00",
        "stock": 80,
        "description": "An updated smartphone",
        "categories": [1, 3]
    }
    ```
- **Пример ответа:**
    ```json
    {
        "id": 1,
        "name": "Smartphone",
        "regular_price": "700.00",
        "discount_price": "600.00",
        "stock": 80,
        "description": "An updated smartphone",
        "categories": [1, 3]
    }
    ```

### Удаление продукта

- **URL:** `/products/{product_id}/`
- **Метод:** `DELETE`
- **Заголовки:**
    - `Content-Type: application/json`
- **Пример ответа:**
    ```json
    {
        "message": "Product deleted successfully"
    }
    ```