# Generated by Django 4.2.2 on 2023-06-23 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_meetup_remove_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='meetup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='backend.meetup', verbose_name='Митап'),
            preserve_default=False,
        ),
    ]
