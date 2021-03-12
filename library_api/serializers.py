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
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = (
            'id',
            'book',
            'client',
            'reserved_at',
            'returned_at',
            'active',
            'delayed_days',
            'price',
            'total_price'
        )
        read_only_fields = ('price', 'total_price')

    def to_representation(self, instance):
        ret = super(ReservationSerializer, self).to_representation(instance)
        ret['book'] = instance.book.__str__()
        ret['client'] = instance.client.__str__()
        return ret

    def get_price(self, instance):
        return instance.book.reservation_price

    def get_total_price(self, instance):
        return instance.tax

    def validate_book(self, book):
        if book.reserved:
            raise serializers.ValidationError("The book already reserved")
        return book
