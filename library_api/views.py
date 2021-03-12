from library_api.baseviews import BaseDefaultViewset
from library_api import filters
from library_api.models import Book, Client, Reservation
from library_api.serializers import BookSerializer, ClientSerializer, ReservationSerializer


class BookViewSet(BaseDefaultViewset):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = filters.BookFilter


class ClientViewSet(BaseDefaultViewset):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_class = filters.ClientFilter


class ReservationViewSet(BaseDefaultViewset):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filterset_class = filters.ReservationFilter

    def create(self, request, *args, **kwargs):
        self.serializer_class = ReservationSerializer
        return super(ReservationViewSet, self).create(request, *args, **kwargs)
