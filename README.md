# Romagram — учебный проект (аналог Instagram)

## Описание
Полнофункциональная социальная сеть, разработанная для практики production-стека.  
Поддерживает профили, посты, комментарии, лайки, друзей, подписки, поиск, уведомления и чат в реальном времени.  

## Функционал
- Регистрация и аутентификация (JWT, Celery для фоновой отправки почты).
- Профили пользователей.
- Посты с изображениями, комментарии, лайки.
- Друзья и подписки.
- Уведомления (Celery + Redis).
- Поиск пользователей (Elasticsearch).
- Чат в реальном времени (Django Channels / WebSockets).
- Тесты апи.

## Стек

**Backend**  
- Python  
- Django, DRF  
- Django Channels (WebSockets)  
- Celery  
- Redis  
- PostgreSQL  
- Elasticsearch  
- JWT  
- DRF Apitest  

**Frontend**  
- React  
- HTML, CSS  
- Tailwind  

**DevOps**  
- Docker Compose  
- Nginx  
- SSL/HTTPS  
- Git  

## Стиль и архитектура кода бэкенда
- Проект реализован в соответствии с [Django Styleguide от HackSoft](https://github.com/HackSoftware/Django-Styleguide).
- `models.py` — определение таблиц и связей в базе данных.
- `services.py` — бизнес-логика и изменение данных.
- `selectors.py` — выборка данных из базы (read-only).
- `serializers.py` — валидация входных данных и их сериализация.
- `utils.py` — переиспользуемые вспомогательные функции.
- `tasks.py` — фоновые задачи, выполняемые через Celery.
- `views.py` — приём запроса, валидация данных и возврат ответа.

- Такой подход позволяет поддерживать чистую архитектуру, минимум магии под капотом, легко тестировать и расширять код.

## Запуск
```sh
# 1. Клонируем репозиторий
git clone https://github.com/RTMoo/social_network.git

# 2. Переключаемся на продакшн-ветку (Опционально)
git switch prod

# 3. Переходим в корневой каталог
cd social_network

# 4. Собираем и запускаем контейнеры
docker compose up --build

# 5. Создаем тестовых пользователей (Опционально)
docker exec -it backend uv run manage.py create_test_users
```

## Документация API
- Swagger UI: `/api/docs/swagger/`
- Redoc: `/api/docs/redoc/`
- OpenAPI схема: `/api/schema/`

## Тестирование
```sh
# Запуск тестов
docker exec backend uv run manage.py test
```
