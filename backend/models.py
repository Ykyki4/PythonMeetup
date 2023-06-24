from django.db import models


class User(models.Model):
    telegram_id = models.CharField('Телеграм идентификатор', max_length=10, unique=True)
    name = models.CharField('Имя', max_length=32)
    is_speaker = models.BooleanField('Спикер', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name}'


class Meetup(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    date = models.DateField('Дата проведения')

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        return f'{self.title}'


class Event(models.Model):
    title = models.CharField('Заголовок', max_length=100, unique=True)
    description = models.CharField('Описание', max_length=500)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE, verbose_name='Митап', related_name='events')
    time = models.TimeField('Время проведения')
    speaker = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Спикер', related_name='events')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Гость', related_name='questions')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='События', related_name='questions')
    content = models.CharField('Содержание', max_length=250)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'Вопрос к {self.event} от {self.guest}'


class VisitCard(models.Model):
    owner = models.ForeignKey(User, verbose_name='Владелец', related_name='visit_card', on_delete=models.CASCADE)
    first_name = models.CharField('Имя', max_length=16)
    last_name = models.CharField('Фамилия', max_length=16)
    job_title = models.CharField('Должность', max_length=100)
    phone = models.CharField('Номер телефона', max_length=20)

    class Meta:
        verbose_name = 'Визитная карточка'
        verbose_name_plural = 'Визитные карточки'

    def __str__(self):
        return f'Визитная карточка {self.first_name} {self.last_name}'
