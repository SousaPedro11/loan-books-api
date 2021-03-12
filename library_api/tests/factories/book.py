import factory
from factory.django import DjangoModelFactory
from mimesis_factory import MimesisField

from library_api.models import Book


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = MimesisField('title')
    subtitle = MimesisField('title')
    author = MimesisField('full_name')
    isbn = MimesisField('isbn')
    edition = factory.Faker('pyint', min_value=1, max_value=50)
    pages = factory.Faker('pyint', min_value=100, max_value=1000)
    reservation_price = factory.Faker('pyfloat', max_value=500.0, positive=True, right_digits=2)
    reserved = False
