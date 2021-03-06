# Generated by Django 3.1.7 on 2021-03-12 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0009_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved_at', models.DateField(auto_now_add=True)),
                ('returned_at', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservation_books', to='library_api.book')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_reservation', to='library_api.client')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
                'db_table': 'tbl_reservation',
                'managed': True,
            },
        ),
    ]
