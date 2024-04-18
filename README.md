# Xone

API для хранения ссылок и коллекций пользователя с возможностью их создания, редактирования, удаления и просмотра

## ENVs:
```
SITE_HOST=localhost
SECRET_KEY=my_secret_key
DEBUG=True
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

## Third party packages:
```
rest_framework
drf_spectacular
```

### Локальный запуск проекта 
```shell
docker compose build
docker compose up
```

| Доступ  | Ссылка                        |
|---------|-------------------------------|
| Админка | http://0.0.0.0:8000/admin/    |
| Сваггер | http://0.0.0.0:8000/api/docs/ |


Задание №2 
```shell
SELECT "users_user"."id",
       "users_user"."email",
       COUNT("links_link"."id") AS "max_links"
FROM "users_user"
         LEFT OUTER JOIN "links_link" ON ("users_user"."id" = "links_link"."user_id")
GROUP BY "users_user"."id"
ORDER BY "max_links" DESC, "users_user"."date_joined" ASC
LIMIT 10;
```
