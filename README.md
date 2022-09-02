# yamdb_final
[![YAMDB workflow status](https://github.com/yanasedowa/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

### Описание

Проект **YaMDb** — собирает отзывы пользователей на произведения. Произведения делятся на категории, список которых может быть расширен администратором. В каждой категории есть произведения: книги, фильмы или музыка.
Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.


### Основной функционал:

REVIEWS
> -   Получить список всех отзывов
> -   Создать новый отзыв
> -   Получить отзыв по id
> -   Частично обновить отзыв по id
> -   Удалить отзыв по id
COMMENTS
> -   Получить список всех комментариев к отзыву по id
> -   Создать новый комментарий для отзыва
> -   Получить комментарий для отзыва по id
> -   Частично обновить комментарий к отзыву по id
> -   Удалить комментарий к отзыву по id
AUTH
> -   Отправление confirmation_code на переданный email
> -   Получение JWT-токена в обмен на email и confirmation_code
USERS
> -   Получить список всех пользователей
> -   Создание пользователя
> -   Получить пользователя по username
> -   Изменить данные пользователя по username
> -   Удалить пользователя по username
> -   Получить данные своей учетной записи
> -   Изменить данные своей учетной записи
CATEGORIES
> -   Получить список всех категорий
> -   Создать категорию
> -   Удалить категорию
GENRES
> -   Получить список всех жанров
> -   Создать жанр
> -   Удалить жанр
TITLES
> -   Получить список всех объектов
> -   Создать произведение для отзывов
> -   Информация об объекте
> -   Обновить информацию об объекте
> -   Удалить произведение


### Как запустить проект:

На macOS или Linux запустите программу Терминал. 
Если у вас Windows — запускайте [Git Bash](https://gitforwindows.org/)

Установите интерпретатор Python 3.7

Для Windows:
www.python.org/downloads/#

Для MacOS:

```
brew install python@3.7
```

Для Linux (Ubuntu):

```
sudo apt-get install python3.7
```

Клонировать репозиторий и перейти в него в командной строке:


```

git clone git@github.com:yanasedowa/infra_sp2.git

```
  

```

cd infra_sp2

```

Перейти в директорию infra:


```

cd infra

```

Создать файл .env и прописать переменные окружения в нём для работы с базой данных:

```

touch .env

```

```

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=key 

```

Проверить, установлен ли Docker:

```

docker -v

```

Если Docker не установлен:

Скачать [Docker Desktop](https://www.docker.com/products/docker-desktop/). 

Для Linux:

```

sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

```

Установить Docker, а вместе с ним Docker Compose:

```

sudo apt install docker-ce docker-compose -y 

```

Запустить docker-compose:

```

docker-compose up -d

```

Будут созданы и запущены в фоновом режиме контейнеры (db, web, nginx).

Выполнить миграции, создать суперпользователя, подгрузить статику:

```

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 

```

Приложение становится доступным по адресу http://localhost.

Заполнить базу тестовыми данными:

```

docker-compose exec web python manage.py loaddata fixtures.json

```

Документация к проекту:

http://127.0.0.1:8000/redoc

### Примеры запросов:

Получить список всех категорий

Права доступа: Доступно без токена

**GET**
/http://localhost/api/v1/categories/

*Ответ*
**200**
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

Создать категорию.

Права доступа: Администратор.

Поле slug каждой категории должно быть уникальным.

**POST**
http://localhost/api/v1/categories/

*Передаваемые данные*

```
{
  "name": "string",
  "slug": "string"
}
```

*Ответ*
**201**
```
{
  "name": "string",
  "slug": "string"
}
```

*Ответ*
**400**
```
{
  "field_name": [
    "string"
  ]
}
```
Удалить категорию.

Права доступа: Администратор.

**DELETE**
http://localhost/api/v1/categories/{slug}/

Обновить информацию о произведении

Права доступа: Администратор

**PATCH**
http://localhost/api/v1/titles/{titles_id}/

*Передаваемые данные*

```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

*Ответ*
**200**
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

### Технологии

-   [Python](https://www.python.org/)
-   [Django](https://www.djangoproject.com/)
-   [Django REST framework](https://www.django-rest-framework.org/)
-   [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
-   [PostgreSQL](https://postgrespro.ru/docs/postgresql/12/)
-   [Gunicorn](https://gunicorn.org/)
-   [nginx](https://www.nginx.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)


### Автор
Седова Яна, 33 когорта 
