# Generated by Django 3.1.3 on 2020-11-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_file',
            field=models.FileField(blank=True, upload_to='custom_files', verbose_name='картинка'),
        ),
    ]
