from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "limit": self.page_size,
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                "results": data,
            }
        )