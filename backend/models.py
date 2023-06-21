from django.db import models


class User(models.Model):
    telegram_id = models.CharField('Телеграм идентификатор', max_length=10, unique=True)
    first_name = models.CharField('Имя', max_length=16)
    last_name = models.CharField('Фамилия', max_length=16)
    about = models.CharField('О себе', max_length=250)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Guest(User):
    class Meta:
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'


class Speaker(User):
    class Meta:
        verbose_name = 'Спикер'
        verbose_name_plural = 'Спикер'


class Event(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.CharField('Описание', max_length=500)
    time = models.TimeField('Время проведения')
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, verbose_name='Спикер', related_name='events')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, verbose_name='Гость', related_name='questions')
    event = models.ForeignKey(Event, on_delete=models.CASCADE , verbose_name='События', related_name='questions')
    content = models.CharField('Содержание', max_length=250)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f"Вопрос к {self.event} от {self.guest}"
