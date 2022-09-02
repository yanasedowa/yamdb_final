# yamdb_final
![Django-app workflow](https://github.com/yanasedowa/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)

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

git clone git@github.com:yanasedowa/yamdb_final.git

```
  

```

cd yamdb_final/infra/nginx

```

В файле `default.conf`:

```

`server_name`: публичный IP сервера

```

Скопировать файлы 'docker-compose.yaml' и 'nginx/default.conf' из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно:

В домашней директории на сервере:

```
mkdir nginx

```

В локальном репозитории:

```

scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>:/home/<username>/nginx/default.conf

```


Заполнить данные в `Settings - Secrets - Actions secrets`:

```

DOCKER_USERNAME: логин в DockerHub
DOCKER_PASSWORD: пароль пользователя в DockerHub
HOST: публичный ip-адрес сервера
USER: логин на сервере
SSH_KEY: приватный ssh-ключ (cat ~/.ssh/id_rsa)
PASSPHRASE: eсли при создании ssh-ключа вы использовали фразу-пароль
DB_ENGINE: django.db.backends.postgresql
DB_HOST: db
DB_PORT: 5432
TELEGRAM_TO: id своего телеграм-аккаунта
TELEGRAM_TOKEN: токен бота
DB_NAME: postgres
POSTGRES_USER: postgres 
POSTGRES_PASSWORD: postgres
SECRET_KEY: key

```

Войти на свой удаленный сервер в облаке.

Остановить службу nginx:

```

sudo systemctl stop nginx

```

Установить docker и docker-compose:

```

sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

```

После деплоя будут созданы и запущены в фоновом режиме контейнеры (db, web, nginx).

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
-   [GitHub Actions](https://github.com/features/actions)


### Автор
Седова Яна, 33 когорта 
