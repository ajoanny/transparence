from django.core.management import BaseCommand

from transparence.features.import_data import ImportData
from transparence.outbound.http.http import Http
from transparence.outbound.sources.poligraph_api import fetch_data


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        http = Http()
        has_next = True
        page = 1

        while has_next:
            print(f"fetch Page {page}")
            response = fetch_data(page, http)
            data = response.get("data", [])
            print(f"{len(data)} legal cases")

            ImportData().perform(data)
            has_next = response.get("has_next", False)
            page += 1
