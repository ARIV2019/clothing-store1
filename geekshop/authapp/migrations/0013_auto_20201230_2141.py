# Generated by Django 3.1.3 on 2020-12-30 18:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_auto_20201230_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 1, 18, 41, 46, 302401, tzinfo=utc)),
        ),
    ]
