from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response

from library_api import filters
from library_api.baseviews import BaseDefaultViewset
from library_api.models import Book, Client, Reservation
from library_api.serializers import BookSerializer, ClientSerializer, ReservationSerializer


class BookViewSet(BaseDefaultViewset):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = filters.BookFilter
    lookup_field = 'pk'

    @action(detail=True, methods=['POST'])
    def reserve(self, request, pk=None):
        data = {
            'client': request.data.get('client', None),
            'book': pk
        }
        serializer = ReservationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        try:
            return super(BookViewSet, self).create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": e.detail}, exception=e, status=status.HTTP_400_BAD_REQUEST)
        except APIException as e:
            return Response({"detail": e.detail}, exception=e, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"detail": e.__repr__()}, exception=e, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(BaseDefaultViewset):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_class = filters.ClientFilter
    lookup_field = 'pk'

    @action(detail=True, methods=['GET'])
    def books(self, request, pk=None):
        client = self.get_object()
        reservation_serializer = ReservationSerializer(client.client_reservation, many=True)
        return Response(reservation_serializer.data, status.HTTP_200_OK)


class ReservationViewSet(BaseDefaultViewset):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filterset_class = filters.ReservationFilter
    lookup_field = 'book'
