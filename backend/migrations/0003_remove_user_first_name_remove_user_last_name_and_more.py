# Generated by Django 4.2.2 on 2023-06-21 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_remove_speaker_user_ptr_user_is_speaker_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=None, max_length=32, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='О себе'),
        ),
    ]
