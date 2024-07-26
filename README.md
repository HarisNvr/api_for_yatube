# Yatube API

### Описание
Проект позволяет пользователям получать доступ через API к постам, группам, 
подписчикам и комментариям.
Создавать, удалять объекты, редактировать их по своему усмотрению
### Технологии
- Python 3.9
- Django 3.2

### Запуск проекта локально
- Клонировать репозиторий и перейти в него в командной строке
```
https://github.com/HarisNvr/api_for_yatube.git
cd api_for_yatube
```
- Cоздать и активировать виртуальное окружение:
```
python -m venv env
venv/scripts/activate
```
- Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
- Запустить проект:
```
python manage.py runserver
```
## К проекту можно обратиться по адресу 127.0.0.1


### Документация API:
http://127.0.0.1:8000/redoc/

### Примеры запросов:
- GET api/v1/posts/

Возвращает список всех постов.

```
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": "2019-08-24T14:15:22Z",
    "image": "string",
    "group": 0
  }
]
```
- GET api/v1/posts/?limit=1&offset=2

Возвращает список постов, с результатом ответа, ограниченным паджинацией.

```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

- POST api/v1/posts/

Добавление новой публикации в коллекцию публикаций. Анонимные запросы запрещены.
Обязательная переменная при отправлении запроса "text": "string". Автором
записи автоматически назначается зарегистрированный пользователь, отправивший 
запрос.

```
"id": 0,
"author": "string",
"text": "string",
"pub_date": "2019-08-24T14:15:22Z",
"image": "string",
"group": 0
```
