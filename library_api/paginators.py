from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LibraryPaginator(LimitOffsetPagination):
    limit_query_param = 'size'
    default_limit = 50


class CustomPaginator(LibraryPaginator):
    def get_next_link(self):
        if self.offset + self.limit >= self.count:
            return None

        url = {'size': self.limit}

        offset = self.offset + self.limit
        url['offset'] = offset
        return url

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = {'size': self.limit}

        if self.offset - self.limit <= 0:
            url['offset'] = 0
            return url

        offset = self.offset - self.limit
        url['offset'] = offset
        return url

    def get_paginated_response(self, data):

        resposta = {
            "count": self.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        }

        return Response(resposta)
