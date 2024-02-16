from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
from django.conf import settings


class CustomPageNumberPagination(PageNumberPagination):
    default_page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]

    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get("page_size", self.default_page_size)
        if page_size == "all":
            self.page_size = len(queryset)
        else:
            try:
                self.page_size = int(page_size)
            except ValueError:
                self.page_size = self.default_page_size

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        try:
            previous_page_number = self.page.previous_page_number()
        except:
            previous_page_number = None

        try:
            next_page_number = self.page.next_page_number()
        except:
            next_page_number = None
        return Response(
            OrderedDict(
                [
                    ("data", data),
                    ("count", len(data)),
                    ("totalCnt", self.page.paginator.count),
                    ("pageCnt", self.page.paginator.num_pages),
                    ("curPage", self.page.number),
                    ("next", self.get_next_link()),
                    ("nextPage", next_page_number),
                    ("previous", self.get_previous_link()),
                    ("previousPage", previous_page_number),
                ]
            )
        )
