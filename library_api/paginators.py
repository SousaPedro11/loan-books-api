from rest_framework.pagination import LimitOffsetPagination


class LibraryPaginator(LimitOffsetPagination):
    limit_query_param = 'size'
    default_limit = 50


class CustomPaginator(LibraryPaginator):
    pass
