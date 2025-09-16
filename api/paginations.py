from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Implementierung von Custom Pagination
# https://www.django-rest-framework.org/api-guide/pagination/
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page-number'
    max_page_size = 1

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.page_size,
            'results': data
        })