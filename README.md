![example workflow](https://github.com/korchemkinsw/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# api_yamdb

## Краткое описание
Данный учебный проект представляет собой реализацию API для доступа к базе данных, содержащей описание, отзывы и комментарии о различных произведениях.

## Технологии в проекте
Целью данной работы является запуск проекта api_yatube с базой данных postgresql на сервере при помощи gunicorn и nginx  в контейнерах docker.

Поскольку в материале курса не учтено, что doker может просто не установиться на компьютер, задание выполнено на виртуальной машине в облаке Яндекса и временно доступно по адресу: 178.154.241.184 (данный адрес так же фигурирует в настройках django и nginx и при развертывании проекта его необходимо заменить)

## Инструкции по запуску
[Данный проект предполагает наличие установленного docker](https://www.docker.com/products/docker-desktop)

- скопировать проект (например с github ```git clone https://github.com/korchemkinsw/infra_sp2```)
- в файлах api_yamdb/settings.ru и nginx/default.conf указать имя или ip своего сервера
- перейти в папку с проектом
- собрать и запустить контейнеры командой ```docker-compose up -d --build```
- выполнить миграции базы данных ```docker-compose exec web python manage.py migrate --noinput```
- создать суперпользователя ```docker-compose exec web python manage.py createsuperuser```
- собрать статику ```docker-compose exec web python manage.py collectstatic --no-input```

Проект доступен по указанному адресу

