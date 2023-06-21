# Generated by Django 4.2.2 on 2023-06-21 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=500, verbose_name='Описание')),
                ('time', models.TimeField(verbose_name='Время проведения')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=10, unique=True, verbose_name='Телеграм идентификатор')),
                ('first_name', models.CharField(max_length=16, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=16, verbose_name='Фамилия')),
                ('about', models.CharField(max_length=250, verbose_name='О себе')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.user')),
            ],
            options={
                'verbose_name': 'Гость',
                'verbose_name_plural': 'Гости',
            },
            bases=('backend.user',),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.user')),
            ],
            options={
                'verbose_name': 'Спикер',
                'verbose_name_plural': 'Спикер',
            },
            bases=('backend.user',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250, verbose_name='Содержание')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='backend.event', verbose_name='События')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='backend.guest', verbose_name='Гость')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='backend.speaker', verbose_name='Спикер'),
        ),
    ]