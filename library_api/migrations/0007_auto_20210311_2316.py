# Generated by Django 3.1.7 on 2021-03-12 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0006_auto_20210311_2314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'managed': True, 'ordering': ['-id'], 'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
    ]
