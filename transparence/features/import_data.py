from transparence.models import Politician, LegalCase, Party, Source


class ImportData:
    def perform(self, cases):
        for case in cases:
            update_legal_case(case)


def update_legal_case(case):
    legal_case = (
        LegalCase.objects.filter(external_id=case["external_id"]).first() or LegalCase()
    )
    if (
        not legal_case.external_updated_at
        or legal_case.external_updated_at < case["external_updated_at"]
    ):
        attributes = {
            "external_id": case["external_id"],
            "category": case["category"],
            "external_updated_at": case["external_updated_at"],
            "title": case["title"],
            "description": case["description"],
            "status": case["status"],
            "date": case["date"],
            "verdict_date": case["verdict_date"],
            "party": find_party(case),
            "politician": find_politician(case),
        }

        for attribute, value in attributes.items():
            setattr(legal_case, attribute, value)

        legal_case.save()
        create_sources(legal_case, case["sources"])


def find_politician(case):
    [politician, _] = Politician.objects.get_or_create(
        external_id=case["politician"]["external_id"],
        full_name=case["politician"]["full_name"],
    )

    return politician


def find_party(case):
    [party, _] = Party.objects.get_or_create(
        abbreviation=case["party"]["abbreviation"],
        name=case["party"]["name"],
    )

    return party


def create_sources(legal_case, sources):
    for source in sources:
        Source.objects.get_or_create(
            external_id=source["external_id"],
            defaults={
                "url": source["url"],
                "publisher": source["publisher"],
                "type": source["type"],
                "title": source["title"],
                "published_at": source["published_at"],
                "legal_case": legal_case,
            },
        )
