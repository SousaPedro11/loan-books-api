from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from library_api.models import Book, Client, Reservation


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ReservationListSerializer(ModelSerializer):
    book = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ('id', 'book', 'client', 'reserved_at', 'returned_at', 'active')

    def get_book(self, obj):
        return obj.book.__str__()

    def get_client(self, obj):
        return obj.client.__str__()


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'book', 'client', 'reserved_at', 'returned_at', 'active')

    def to_representation(self, instance):
        ret = super(ReservationSerializer, self).to_representation(instance)
        ret['book'] = instance.book.__str__()
        ret['client'] = instance.client.__str__()
        return ret
