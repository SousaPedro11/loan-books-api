# Generated by Django 3.1.7 on 2021-03-12 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0008_auto_20210311_2322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'db_table': 'tbl_client',
                'managed': True,
                'unique_together': {('name', 'email')},
            },
        ),
    ]
