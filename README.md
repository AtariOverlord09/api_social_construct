### Описание проекта:

Этот проект является решением задачи взаимодействия с данными проекта **yatube** через **API**. Его цель состоит в том, чтобы обеспечить полноценную возможность осуществлять **CRUD** операции через **API**. Проект предоставляет преимущества с точки зрения *простоты*, *скорости работы* и *безопасности*.

### Как запустить проект:
Чтобы настроить проект на локальном компьютере, выполните следующие действия:

1.Клонируйте репозиторий на свой локальный компьютер командой:
```
git clone https://github.com/AtariOverlord09/api_final_yatube.git
```

2.Установите необходимые зависимости, запустив pip install -r requirements.txt.

3.Настройте базу данных, запустив миграцию командой:
```
python manage.py migrate.
```

4.Запустите локальный сервер разработки командой:
```
python manage.py runserver.
```

### Примеры запросов:

Вот несколько примеров запросов API, которые можно сделать в проекте:

Пример 1:

GET http://127.0.0.1:8000/api/v1/posts/
```
{

    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
    "results": [

        { ... }
    ]

}
```
Так же поддерживает все другие операции CRUD.

Пример 2:

GET http://127.0.0.1:8000/api/v1/groups/
```
[

    {
        "id": 0,
        "title": "string",
        "slug": "string",
        "description": "string"
    }

]
```
Поддерживает только GET запросы

 Пример 3:

GET http://127.0.0.1:8000/api/v1/follow/
```
[

    {
        "user": "string",
        "following": "string"
    }

]
```
Поддерживает только POST и GET запросы.

***Примечание: Убедитесь, что сервер разработки запущен, и при необходимости замените localhost:8000 на соответствующий URL-адрес.***
Автор: Иван Сахневич(AtariOverlord09)