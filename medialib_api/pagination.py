from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class SimplePagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "page": self.page.number,
            "pages": self.page.paginator.num_pages,
            "next": {
                "link": self.get_next_link(),
                "page": self.page.next_page_number()
            } if self.page.has_next() else None,
            "previous": {
                "link": self.get_previous_link(),
                "page": self.page.previous_page_number()
            } if self.page.has_previous() else None,
            "results": data
        })
