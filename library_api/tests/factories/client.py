from factory.django import DjangoModelFactory
from mimesis_factory import MimesisField

from library_api.models import Client


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    name = MimesisField('full_name')
    username = MimesisField('username')
    email = MimesisField('email')
