# QA-Hopper


>*Преа́мбула: в связи со спецификой условий выполнения задачи, код далее написан исходя из  следующих принципов:*
>   - *Больше, не значит лучше.*
>   - *Сначала функционал, потом оптимизация.*
>   - *Делаешь, как понимаешь.*<br>
>
>*Подробности специфики не уточняю, однако автор полностью согласен со всей критикой в части, например, оптимизации кода.*

<br>

## Общее описание.

### Код написан по заданию [Hopper IT](https://hopper-it.ru/).

Работаем с [репозиторием](https://gitlab.monq.ru/p.alekseev/flask-app-example).

<br>

**Поставленные задачи:**
- Реализовать набор автотестов для представленного web-сервиса на Python.

<br>

## 1. Подготовка. 
<br>

Для того, чтобы проверить в работе автотесты, мы будем работать с локальной копией web-сервиса из [репозитория](https://gitlab.monq.ru/p.alekseev/flask-app-example). Для этого...
<br><br>
1.1 Разверните сервис согласно инструкции предложенного [репозитория](https://gitlab.monq.ru/p.alekseev/flask-app-example) или, если что-то пошло не так, то [исходного репозитория](https://github.com/zeburek/flask-mongoengine-example).
<br><br>
1.2 Скачайте код:<br>
`https://github.com/Sam1808/QA-Hopper`
<br><br>
1.3 Создайте виртуальное окружение, [активируте](https://devpractice.ru/python-lesson-17-virtual-envs/#p33) его и перейдите в папку `QA-Hopper`:<br>
`python3 -m venv _название_окружения_`
<br><br>
1.4 Обновите установщик пакетов `pip` (*не помешает*) и установите зависимости:<br>
`pip install --upgrade pip`<br>
`pip install -r requirements.txt`
<br><br>
1.5 Вы сделали почти все, пора приступать к тестам... 
<br><br>

## 2. Описание и запуск тестов.

**Лирика:** *Согласно инструкций предложенных репозиториев, для web-сервисов реализован API по ссылкам `/api/subscribe` и `/api/subscribers`, однако... у меня по указанным ссылкам API не доступен :(. 
<br>
Причины выяснять не стал, откопав в коде доступный API по ссылке `/subscriptions`.
<br>
Далее весь код реализован с помощью фреймворка `PyTest` на основании доступности API сервиса.*

2.1 Определите URL по которому доступен сервис (по умолчанию `http://localhost:4000`).
<br>
2.2 Убедитесь в доступности API (по умолчанию `http://localhost:4000/subscriptions`).

2.3 В папке представлено три основных файла для работы: 
<br>
`conftest.py` - конфигурация наших тестов.
<br>
`tests.py` - сами тесты.
<br>
`load_data.txt` - данные для использования в тестировании. 
<br>
О каждом файле по порядку...

### `conftest.py`:

Используется для переопределения URL сайта (п.2.1) и API URL сайта (п.2.2). Таким образом, если URL сайтов у вас отличаются от значения по умолчанию, вы можете их переопределить в командной строке, при запуске тестов. Подробнее в **Примерах**.

### `tests.py`:

Непосредственно сами тесты. Название функции определяет цель теста. 
<br>
Например, `test_create_subscriber` на самом деле тестирует создание подписчика.

### `load_data.txt`:

Файл с тестовыми данными. 
<br>
Мы тестируем `Cервис подписок`, данных много и очень удобно, если у нас есть возможность вынести их в отдельный файл. Каждая новая строка - новый словарь с тестовыми данными. В текущем репозитории приложен пример, который вы можете изменять по своему усмотрению: 
```
{"email": "test@email.com","name": "test_name","time": "7s","comment": "Test0 - Pozitive",}
{"email": "test@email.com","name": "test_name","time": "7m","comment": "Test1 - Pozitive",}
{"email": "test@email.com","name": "test_name","time": "7d","comment": "Test2 - Pozitive"}
{"email": "test@email.com","name": "","time": "7d","comment": "Test3 - Negative"}
{"email": "test@email.com","name": "","time": "7d","comment": "Test4 - Negative"}
{"email": "test@email","name": "test_name","time": "7d","comment": "Test5 - Negative"}
{"email": "@email.com","name": "test_name","time": "7d","comment": "Test6 - Negative"}
```
Поля `email`, `name`, `time` используются для создания подписчика, поле `comment` никак не используется сервисом (хотя и возвращается через API), поэтому мы можем пользовать его на свое усмотрение, например, чтобы комментировать характер теста. 
<br>
При отсуствии требований к приложению тяжело судить, будет ли конкретная ситуация считаться ошибкой (например, имя пользователя с использованием спецсиволов?), но отследить поведение приложения можно без проблем.

2.4. Предлагаю уже запускать тесты. Итак примеры: 

`pytest tests.py `
<br>
Запускает тесты в минимальным выводом в консоль и отчетом об ошибках.
<br>
*В текущей конфигурации это 51 тест меньше, чем за 2 секунды. ;)*

`pytest -v tests.py `
<br>
Тесты с более подробной детализацией в консоли. 

`pytest -s -v tests.py `
<br>
Тесты с более подробной детализацией в консоли. Плюс, если были отладочные принты - то вы бы их тоже увидели. Учень удобно пользовать такие принты с полем комментариев, которое есть у нас в файле с тестовыми данными.

`pytest -v --site_url=http://localhost:8000 --api_url=http://localhost:8000/api/ tests.py  `
<br>
Здесь вы запустили тесты с переопределенными URL самого сайта и его API на `http://localhost:8000` и `http://localhost:8000/api/`, соответвенно.

<br>

2.5 И последнее, что хочется напомнить... `AssertionError` - кратко расскажет вам причину ошибки. Обращайте внимание на `test_data` в заголовке отчета, чтобы понимать, с какими именно данными приложение вызвало ошибку. 


<br>

*TODO:*

 - *Можно все переписать на Selenium, тестов будет немного больше, но и их длительность существенно увеличится;* <br>
 - *Можно ещё отмаркировать тестовые функции, для того, чтобы была возможность запускать конкретные тесты;*<br>
 - *Если вы ошибётесь в файле с данными - система этого не поймет... по хорошему надо добавить проверку тестовых данных перед тем как запускать тесты;*<br>
 - *А ещё, можно попробовать управлять тестовыми данными через командную строку;*<br>
  - *Этот список можно придумывать бесконечно...*<br>
 
 <br><br>


> Ого! Вы дочитали до конца! Вам понравилось? В любом случае - поставте *звездочку* репозиторию, так хотя бы будет ясно, что его смотрели.<br>