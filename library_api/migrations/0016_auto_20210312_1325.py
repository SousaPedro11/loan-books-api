# Generated by Django 3.1.7 on 2021-03-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0015_auto_20210312_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
