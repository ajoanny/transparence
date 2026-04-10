from django.db.models.functions import Greatest
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.paginator import Paginator

from transparence.models import LegalCase
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    TrigramSimilarity,
)
from django.db.models import Value, QuerySet, Q


class LegalCaseViewSet(ViewSet):
    def list(self, request):
        page_number = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("pageSize", 10))
        party_id = request.GET.get("party_id")
        politician_id = request.GET.get("politician_id")
        statuses = request.GET.getlist("statuses", [])
        search = request.GET.get("search")
        query = (
            LegalCase.objects.annotate(rank=Value(1), similarity=Value(1))
            .order_by("-rank", "-similarity", "-date")
            .all()
        )
        print(statuses)
        if party_id:
            query = query.filter(party__id=party_id)
        if politician_id:
            query = query.filter(politician_id=politician_id)
        if statuses:
            query = query.filter(status__in=statuses).distinct()
        if search:
            query = self.text_filter(query, search)

        paginator = Paginator(query, page_size)
        page = paginator.get_page(page_number)

        data = list(map(map_legal_cases, page.object_list))
        pagination = {
            "page": page.number,
            "page_size": paginator.per_page,
            "pages_count": paginator.num_pages,
            "total": paginator.count,
        }

        return Response({"data": data, "pagination": pagination})

    def text_filter(
        self, query: QuerySet[LegalCase, LegalCase], search
    ) -> QuerySet[LegalCase, LegalCase]:
        vector = (
            SearchVector("party__name", config="french", weight="A")
            + SearchVector("politician__full_name", config="french", weight="B")
            + SearchVector("title", config="french", weight="C")
            + SearchVector("description", config="french", weight="D")
        )

        search_query = SearchQuery(search, config="french")
        search_rank = SearchRank(vector, search_query, weights=[0.1, 1, 1, 1])
        query = query.annotate(
            rank=search_rank,
            similarity=Greatest(
                TrigramSimilarity("title", search),
                TrigramSimilarity("party__name", search),
                TrigramSimilarity("politician__full_name", search),
                TrigramSimilarity("status", search),
            ),
        ).filter(Q(similarity__gte=0.1) | Q(rank__gte=0.1))

        return query


def map_legal_cases(case):
    return {
        "category": case.category,
        "title": case.title,
        "description": case.description,
        "status": case.status,
        "date": case.date,
        "verdict_date": case.verdict_date,
        "party": {
            "id": case.party.id,
            "name": case.party.name,
        },
        "politician": {
            "id": case.politician.id,
            "full_name": case.politician.full_name,
        },
        "sources": list(map(map_sources, case.sources.all())),
    }


def map_sources(source):
    return {
        "url": source.url,
        "publisher": source.publisher,
        "type": source.type,
        "title": source.title,
        "published_at": source.published_at,
    }
