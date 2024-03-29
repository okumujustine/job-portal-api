from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class JobPageNumberPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current': self.page.number,
            'count': self.page.paginator.count,
            'results': data
        })


class JobApplicationsPageNumberPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current': self.page.number,
            'count': self.page.paginator.count,
            'results': data
        })


class EmployeeJobApplicationsPageNumberPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current': self.page.number,
            'count': self.page.paginator.count,
            'results': data
        })
