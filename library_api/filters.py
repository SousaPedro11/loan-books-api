from django_filters import rest_framework as filters, OrderingFilter
from django_filters.widgets import BooleanWidget

from library_api import models
from library_api.filters_util import get_fields_tuple


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='iexact')
    title__istartswith = filters.CharFilter(field_name='title', lookup_expr='istartswith')
    title__icontains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    subtitle = filters.CharFilter(field_name='subtitle', lookup_expr='iexact')
    subtitle__istartswith = filters.CharFilter(field_name='subtitle', lookup_expr='istartswith')
    subtitle__icontains = filters.CharFilter(field_name='subtitle', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='iexact')
    author__istartswith = filters.CharFilter(field_name='author', lookup_expr='istartswith')
    author__icontains = filters.CharFilter(field_name='author', lookup_expr='icontains')
    isbn = filters.CharFilter(field_name='isbn', lookup_expr='iexact')
    isbn__istartswith = filters.CharFilter(field_name='isbn', lookup_expr='istartswith')
    isbn__icontains = filters.CharFilter(field_name='isbn', lookup_expr='icontains')
    reservation_price = filters.NumberFilter(field_name='reservation_price', lookup_expr='exact')
    reservation_price_ne = filters.NumberFilter(field_name='reservation_price', lookup_expr='ne')
    reservation_price_lt = filters.NumberFilter(field_name='reservation_price', lookup_expr='lt')
    reservation_price_gt = filters.NumberFilter(field_name='reservation_price', lookup_expr='gt')
    reservation_price_lte = filters.NumberFilter(field_name='reservation_price', lookup_expr='lte')
    reservation_price_gte = filters.NumberFilter(field_name='reservation_price', lookup_expr='gte')
    reserved = filters.BooleanFilter(field_name='reserved', widget=BooleanWidget())

    class Meta:
        model = models.Book
        fields = [
            'title',
            'subtitle',
            'author',
            'isbn',
            'reservation_price',
            'reserved',
        ]

    ordering = OrderingFilter(
        fields=[
            *get_fields_tuple(Meta.model),
        ],
        label=f'Ordenation of {Meta.model.__name__}s'
    )


class ClientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    name__istartswith = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    name__icontains = filters.CharFilter(field_name='name', lookup_expr='icontains')
    username = filters.CharFilter(field_name='username', lookup_expr='iexact')
    username__istartswith = filters.CharFilter(field_name='username', lookup_expr='istartswith')
    username__icontains = filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='iexact')
    email__istartswith = filters.CharFilter(field_name='email', lookup_expr='istartswith')
    email__icontains = filters.CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = models.Client
        fields = [
            'name',
            'username',
            'email',
        ]

    ordering = OrderingFilter(
        fields=[
            *get_fields_tuple(Meta.model),
        ],
        label=f'Ordenation of {Meta.model.__name__}s'
    )


class ReservationFilter(filters.FilterSet):
    client_name = filters.CharFilter(field_name='client__name', lookup_expr='iexact')
    client_name__istartswith = filters.CharFilter(field_name='client__name', lookup_expr='istartswith')
    client_name__icontains = filters.CharFilter(field_name='client__name', lookup_expr='icontains')
    client_username = filters.CharFilter(field_name='client__username', lookup_expr='iexact')
    client_username__istartswith = filters.CharFilter(field_name='client__username', lookup_expr='istartswith')
    client_username__icontains = filters.CharFilter(field_name='client__username', lookup_expr='icontains')
    book_title = filters.CharFilter(field_name='book__title', lookup_expr='iexact')
    book_title__istartswith = filters.CharFilter(field_name='book__title', lookup_expr='istartswith')
    book_title__icontains = filters.CharFilter(field_name='book__title', lookup_expr='icontains')
    book_author = filters.CharFilter(field_name='book__author', lookup_expr='iexact')
    book_author__istartswith = filters.CharFilter(field_name='book__author', lookup_expr='istartswith')
    book_author__icontains = filters.CharFilter(field_name='book__author', lookup_expr='icontains')
    reserved_at = filters.DateFilter(field_name='reserved_at', lookup_expr='contains')
    returned_at = filters.DateFilter(field_name='returned_at', lookup_expr='contains')
    active = filters.BooleanFilter(field_name='active', widget=BooleanWidget())

    class Meta:
        model = models.Reservation
        fields = [
            'client_name',
            'client_username',
            'book_title',
            'book_author',
            'reserved_at',
            'returned_at',
            'active',
        ]

    ordering = OrderingFilter(
        fields=[
            ('client__name', 'client_name'),
            ('client__username', 'client_username'),
            ('book__title', 'book_title'),
            ('book__author', 'book_author'),
            *get_fields_tuple(Meta.model),
        ],
        label=f'Ordenation of {Meta.model.__name__}s'
    )
