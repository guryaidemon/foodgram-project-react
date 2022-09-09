![foodgram _workflow Status](https://github.com/guryaidemon/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)

# Foodgram, «Продуктовый помощник».

## Описание 
На этом сервисе пользователи смогут публиковать рецепты,
подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное»,
а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

## Для работы с удаленным сервером (на ubuntu):
* Выполните вход на свой удаленный сервер

* Установите docker на сервер:
  ```
    sudo apt install docker.io 
  ```
* Установите docker-compose на сервер:
  ```
    sudo apt install docker-compose -y
  ```
* Локально отредактируйте файл nginx.conf и в строке server_name впишите свой IP
  * Скопируйте файлы docker-compose.yml и nginx.conf из репозитория на сервер:
  ```
    scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
    scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
  ```

* Cоздайте .env файл и впишите:
  ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
  ```
  
* На сервере соберите docker-compose:
  ```
    sudo docker-compose up -d --build
  ```
* После успешной сборки на сервере выполните команды (только после первого деплоя):

- Соберите статические файлы:
  ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
  ```
- Примените миграции:
  ```
    sudo docker-compose exec backend python manage.py migrate --noinput
  ```
- Создать суперпользователя Django:
  ```
    sudo docker-compose exec backend python manage.py createsuperuser
  ```
- Дополнительно можно наполнить DB ингредиентами и тэгами::  
  ```
    sudo docker-compose exec backend python manage.py load_tags
    sudo docker-compose exec backend python manage.py load_ingrs
  ```

- Проект будет доступен по вашему IP
