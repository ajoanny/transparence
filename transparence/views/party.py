from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.paginator import Paginator

from transparence.models import Party

class PartyViewSet(ViewSet):

    def list(self, request):
        page_number = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("pageSize", 10))

        parties = Party.objects.all().order_by("name")
        paginator = Paginator(parties, page_size)
        page = paginator.get_page(page_number)

        data = [({ 'name': party.name, 'abbreviation': party.abbreviation }) for party in page]
        pagination = {
            "page": page.number,
            "page_size": page_size,
            "pages_count": paginator.num_pages,
            "total": paginator.count,
         }

        return Response({ "data": data, "pagination": pagination })
