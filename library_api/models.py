from datetime import date
from decimal import Decimal, getcontext

from django.db import models
from django.db.models import Lookup, Field
from rest_framework.exceptions import ValidationError

from library_api.util import Penalty, InterestPerDay


@Field.register_lookup
class NotEqualLookup(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


class Book(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    edition = models.SmallIntegerField(default=1)
    pages = models.SmallIntegerField(default=0, null=True)
    reservation_price = models.DecimalField(max_digits=8, decimal_places=2)
    reserved = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_book'
        managed = True
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        unique_together = ('title', 'author', 'edition'),
        ordering = ['title', 'author', 'edition']

    def save(self, *args, **kwargs):
        for f in self._meta.fields:
            if isinstance(f, models.CharField):
                field_name = f.attname
                val = getattr(self, field_name, False)
                if val:
                    setattr(self, field_name, val.upper())
        if Book.objects.filter(title=self.title, author=self.author, edition=self.edition,
                               reserved=self.reserved).first():
            raise ValidationError(detail="Book already exists!")
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}, {self.author}, Ed {self.edition}'


class Client(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'tbl_client'
        managed = True
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        unique_together = ('name', 'email'),
        ordering = ['name', 'username']

    def __str__(self):
        return f'{self.username}'


class Reservation(models.Model):
    MAX_DAYS = 3
    tax = 0
    book = models.ForeignKey('Book', on_delete=models.PROTECT, related_name='reservation_books')
    client = models.ForeignKey('Client', on_delete=models.PROTECT, related_name='client_reservation')
    reserved_at = models.DateField(auto_now_add=True)
    returned_at = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_reservation'
        managed = True
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ['-reserved_at', 'book__title']

    def save(self, *args, **kwargs):
        super(Reservation, self).save(*args, **kwargs)
        book = self.book
        book.reserved = True
        book.save()

    @property
    def delayed_days(self):
        today = date.today()

        loan_days = today - self.reserved_at
        return loan_days.days

    @property
    def tax(self):
        getcontext().prec = 4
        if self.delayed_days > 0:
            reservation_price = self.book.reservation_price
            penalty = Penalty(self.delayed_days).calculate(reservation_price) - reservation_price
            interest_per_day = InterestPerDay(self.delayed_days).calculate(reservation_price) - reservation_price
            return reservation_price + penalty + interest_per_day
        return Decimal(0)

    def __str__(self):
        return f'{self.client.username}: {self.book.__str__()}'
