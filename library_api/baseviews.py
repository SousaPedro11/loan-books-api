from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet


class BaseDefaultViewset(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    class Meta:
        abstract = True

    def get_queryset(self):
        if not self.request:
            return self.queryset.model.objects.none()

        return self.queryset
