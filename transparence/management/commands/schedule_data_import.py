from django.core.management import BaseCommand
from django_q.models import Schedule
from django_q.tasks import async_task
from datetime import datetime, timedelta, timezone
import json

from transparence.features.import_data import ImportData
from transparence.outbound.http.http import Http
from transparence.outbound.sources.poligraph_api import fetch_data
from transparence.models import LegalCase


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        job = Schedule.objects.filter(name="import_data").first()

        if job is None:
            Schedule.objects.create(
                name="import_data",
                func="transparence.management.commands.import_data",
                schedule_type=Schedule.DAILY,
                repeats=-1,
                next_run=datetime.now(timezone.utc).replace(hour=1, minute=0),
            )


def import_data():
    async_task("transparence.management.commands.import_data_by_page", page=1)


def import_data_by_page(page):
    print(f"Fetching page {page}")
    response = fetch_data(page, Http())
    data = response.get("data", [])
    print(f"{len(data)} legal cases")
    ImportData().perform(data)
    has_another_page = response.get("has_next", False)
    if has_another_page:
        print(f"scheduling task for page {page+1}")
        Schedule.objects.create(
            func="transparence.management.commands.import_data_by_page",
            kwargs=json.dumps({"page": page + 1}),
            schedule_type=Schedule.ONCE,
            next_run=datetime.now() + timedelta(seconds=5),
        )
    else:
        print(f"Done page count {page} => {LegalCase.objects.count()} legal cases")
