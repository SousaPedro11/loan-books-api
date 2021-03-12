# Generated by Django 3.1.7 on 2021-03-11 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('isbn', models.CharField(blank=True, max_length=20, null=True)),
                ('number_pages', models.SmallIntegerField()),
                ('reservation_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('reserved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'db_table': 'tbl_book',
                'managed': True,
            },
        ),
    ]