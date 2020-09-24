# URL-SH0RT - легковесный сокращатель ссылок на Flask/JSON API. 

API размещено по адресу https://url-sh0rt.herokuapp.com . Авторизация не требуется.

Также есть UI в виде телеграм-бота https://t.me/url_sh0rt_bot (возможна нестабильная работа, хостится дома на Raspberry Pi.)

---

## Установка и настройка. (локальный хостинг)

Для работы приложения необходим Python версии 3.x (протестировано на Python 3.7.2 и Python 3.8.5)

Скачайте и распакуйте архив: 

```
git clone https://github.com/Malomalsky/url_shrt.git

cd url_shrt
```

Находясь в директории, рекомендуется активировать виртуальное окружение (опционально).  Далее установите зависимости: 

```
pip install -r requirements.txt
```

Следом необходимо создать базу данных: 

```
python url_shortener/createdb.py
```
Приложение готово к работе! Запустите его командой (находясь в корневой директории проекта): 

```
flask run
```

## Доступные методы 

Обязательный заголовок всех запросов - "Content-Type": "application/json". JSON API все-таки!

Схема JSON-объекта выглядит следующим образом: 
```
{ 
  "id" : "", (Автоинкремент)
  "original_url" : "", 
  "custom_url": "", (Опционально, по дефолту - null; должно быть уникально)
  "short_url": "", (Автогенерация, длинна = 5 букв),
  "date_created": "" (Автогенерация)
}
```

Методы, предоставляемые API: 

| url         | method | action                                                                                                | Тело запроса                                                                                                                                                                        |
|-------------|--------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /add_link   | POST   | Добавляет ссылку в базу данных, возвращает JSON с сокращенной ссылкой и (если была введена) кастомной | "original_url" : валидная оригинальная ссылка (adress.host);  "custom_url" (опционально) : желаемая кастомная ссылка, обычное слово по которому будет доступна оригинальная ссылка  |
| /links      | GET    | Возвращает JSON-список со всеми обьектами.                                                            | -                                                                                                                                                                                   |
| /links/<id> | GET    | Возвращает JSON с определенным объектом (по id)                                                       | -                                                                                                                                                                                   |
| /links/<id> | PUT    | Обновление информации в БД (по id)                                                                    | "original_url", "short_url", "custom_url"                                                                                                                                           |
| /links/<id> | DELETE | Удаление информации (по id)                                                                           | -                                                                                                                                                                                   |


**Важно** - редирект на оригинальные URL происходит при обращении на имя хоста 

```
hostname/<short|custom>,
где hostname - 
127.0.0.1:5000, если запущено локально; 
https://url-sh0rt.herokuapp.com - захосченный сервис
```



.
## Примеры работы. 

Демонстрация проводится на https://url-sh0rt.herokuapp.com

Если программа запущена локально - обращаться по 127.0.0.1:5000

---
### Добавим валидную ссылку:

Запрос:

```
curl --location --request POST 'https://url-sh0rt.herokuapp.com/add_link' \
--header 'Content-Type: application/json' \
--data-raw '{
    "original_url": "avito.ru"
}'
```

Ответ: 
```
{
    "custom_url": null,
    "date_created": "2020-09-24T16:18:59.181662",
    "id": 2,
    "original_url": "https://avito.ru",
    "short_url": "hYCEm"
}
 ```
 
 
 ---
 ### Попробуем добавить невалидную ссылку: 
 
 Запрос:
 ```
 curl --location --request POST 'https://url-sh0rt.herokuapp.com/add_link' \
--header 'Content-Type: application/json' \
--data-raw '{
    "original_url": "avito" 
}'
```

Ответ: 
```
{
    "message": "Not valid URL. Try again."
}
```
 
 Можно заметить, что если была введена валидная ссылка, сокращатель добавляет к ней 'https:///'
 
 ---
 
 ### Добавим валидную ссылку вместе с кастомной 
 
Запрос:

```
curl --location --request POST 'https://url-sh0rt.herokuapp.com/add_link' \
--header 'Content-Type: application/json' \
--data-raw '{
    "original_url": "avito.ru",
    "custom_url": "best-marketplace"
}'
```

Ответ:

```
{
    "custom_url": "best-marketplace",
    "date_created": "2020-09-24T16:16:41.195786",
    "id": 1,
    "original_url": "https://avito.ru",
    "short_url": "aAE1l"
}
```

Попробуем перейти по https://url-sh0rt.herokuapp.com/best-marketplace и https://url-sh0rt.herokuapp.com/hYCEm

Спойлер - редирект работает! 
 
--- 

Внесем еще пару ссылок - для проверки PUT и DELETE - запросов: 

```
{
    "custom_url": null,
    "date_created": "2020-09-24T16:24:35.876784",
    "id": 3,
    "original_url": "https://vk.com",
    "short_url": "ANjno"
}
```

```
{
    "custom_url": "search",
    "date_created": "2020-09-24T16:31:15.454145",
    "id": 4,
    "original_url": "https://yandex.ru",
    "short_url": "L91Zy"
}
```

---

### Обновим информацию о vk.com. Добавим кастомное имя 'soc': 

Запрос: 
```
curl --location --request PUT 'https://url-sh0rt.herokuapp.com/links/3' \
--header 'Content-Type: application/json' \
--data-raw '{
    "custom_url": "soc"
}'
```

Ответ: 
```
{
    "custom_url": "soc",
    "date_created": "2020-09-24T16:24:35.876784",
    "id": 3,
    "original_url": "https://vk.com",
    "short_url": "ANjno"
}
```

*Кстати, если попытаться ввести неуникальное кастомное имя, программа вернет следующее сообщение:* 
```
{
    "message": "Entered custom URL already existed."
}
```

---

### Удалим данные о vk.com 

Запрос: 

```
curl --location --request DELETE 'https://url-sh0rt.herokuapp.com/links/3' \
--header 'Content-Type: application/json' \
--data-raw ''
```

Ответ: 
```
{
    "custom_url": "soc",
    "date_created": "2020-09-24T16:24:35.876784",
    "id": 3,
    "original_url": "https://vk.com",
    "short_url": "ANjno"
}
```

После чего данная информация будет удалена из БД. 


## Технические моменты (и усложнения) 

### Генерация сокращенных ссылок. 

Генерация сокращенной ссылки очень проста - с помощью пайтоновского модуля random! 5 случайных выборов (random.choices) из последовательности цифр, строчных и прописных букв английского алфавита. При этом, каждая короткая ссылка должна быть уникальной, что предусмотрено в коде. 

### Кастомные ссылки.

Добавить кастомную ссылку можно с помощью включения в POST-запрос поля "custom_url". После чего 

### Валидация URL. 

Валидация введенных URL производится с помощью регулярных выражений. Валидными считаются URL формата example.com или http|s://example.com. В первом случае к URL будет автоматически добавлен протокол: 'https://' 

### Тесты. 
)                                                                    |
Все тесты лежат [тут](https://github.com/Malomalsky/url_shrt/tree/master/url_shortener/tests)

### Бесплатный хостинг.

Как было сказано выше, API размещено на heroku.com. Обращаться по https://url-sh0rt.herokuapp.com

### Нагрузочное тестирование 

Нагрузочное тестирование можно провести с помощью встроенных в heroku методов! Но есть ли смысл, если приложение крутится на бесплатном плане? 









