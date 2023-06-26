# Проект PythonMeetup
Проект содержит телеграм бота для помощи в проведении митапов и админ-панель для управления базой данных.

Бот позволяет: 
- Ознакомиться с программой мероприятия,
- Оставить свою визитку другим участникам и ознакомиться с чужими
- Задать вопросы спикерам, ведущим мероприятия
- Поддержать проект на любую сумму
## Как установить
- Необходимо создать телеграм бота с помощью отца ботов @BotFather, написав ему и выбрав имена для бота. 
После этого будет получен токен, подобный этому: `1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234`.
- Для работы системы пожертвований к боту необходимо подключить оплату в тестовом или полноценном режиме. 
- В проекте используется тестовая оплата. Для её подключения воспользуйтесь [инструкцией](https://core.telegram.org/bots/payments#getting-a-token).
После подключения оплаты будет получен токен подобный этому: `12345678:TEST:12345678-9555-3396-35d8-adfsdcsgf`
Проект использует базу данных PostgreSQL. Для её работы необходимо создать БД и получить её адрес,  подобный этому:
`python-meetup:5555@66.7.123.125/python-meetup`
- Для хранения токенов в проекте используются переменные окружения. Все полученные токены и адрес БД 
необходимо добавить в файл `.env`. Так же необходимо создать переменную `SECRET_KEY`, 
использующуюся для работы админ-панели Django. Пример заполненного файла:
```
TELEGRAM_TOKEN=1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234
PAYMENTS_PROVIDER_TOKEN=12345678:TEST:12345678-9555-3396-35d8-adfsdcsgf
DB_URL=python-meetup:5555@66.7.123.125/python-meetup
SECRET_KEY=secret_key
```
- Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
## Запуск проекта
### Запуск бота
Для запуска телеграм бота используется команда:
`python manage.py runtgbot`
### Запуск админ-панели
Для запуска админ панели используется команда:
`python manage.py runserver`
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).