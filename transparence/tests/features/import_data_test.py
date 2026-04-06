from datetime import date, datetime, timezone
from django.test import TestCase
from assertpy import assert_that

from transparence.features.import_data import ImportData
from transparence.models import LegalCase, Politician, Party, Source
from transparence.tests.factories.legal_case import LegalCaseFactory
from transparence.tests.factories.party import PartyFactory
from transparence.tests.factories.politician import PoliticianFactory


class TestImportData(TestCase):

    def test_when_legal_case_does_not_exists_create_legal_case(self):
        cases = [
            case_data(
                {
                    "external_id": "case.id",
                    "category": "case.category",
                    "external_updated_at": datetime(
                        year=2026, month=1, day=3, tzinfo=timezone.utc
                    ),
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "date": datetime(year=2026, month=1, day=1, tzinfo=timezone.utc),
                    "verdict_date": datetime(
                        year=2026, month=1, day=2, tzinfo=timezone.utc
                    ),
                }
            )
        ]

        ImportData().perform(cases)

        legal_case_db = LegalCase.objects.get(external_id="case.id")
        attributes = {
            "external_id": "case.id",
            "category": "case.category",
            "external_updated_at": datetime(
                year=2026, month=1, day=3, tzinfo=timezone.utc
            ),
            "title": "case.title",
            "status": "case.status",
            "date": date(2026, 1, 1),
            "verdict_date": date(2026, 1, 2),
        }
        for key, value in attributes.items():
            assert_that(getattr(legal_case_db, key)).is_equal_to(value)

    def test_when_politician_does_not_exists_create_politician(self):
        cases = [
            case_data(
                {
                    "politician": {
                        "external_id": "politician.id",
                        "full_name": "politician.full_name",
                    },
                }
            )
        ]

        ImportData().perform(cases)

        politician_db = Politician.objects.get(external_id="politician.id")
        attributes = {
            "external_id": "politician.id",
            "full_name": "politician.full_name",
        }
        for key, value in attributes.items():
            assert_that(getattr(politician_db, key)).is_equal_to(value)

    def test_when_party_does_not_exists_create_party(self):
        cases = [
            case_data(
                {
                    "party": {
                        "abbreviation": "party.short_name",
                        "name": "party.name",
                    },
                }
            )
        ]

        ImportData().perform(cases)

        party = Party.objects.get(abbreviation="party.short_name")
        attributes = {
            "abbreviation": "party.short_name",
            "name": "party.name",
        }
        for key, value in attributes.items():
            assert_that(getattr(party, key)).is_equal_to(value)

    def test_when_party_exists_do_not_create_party(self):
        cases = [
            case_data(
                {
                    "party": {
                        "abbreviation": "party.short_name",
                        "name": "party.name",
                    },
                }
            )
        ]

        PartyFactory.create(abbreviation="party.short_name", name="party.name")

        ImportData().perform(cases)

        parties = Party.objects.filter(abbreviation="party.short_name")
        assert_that(parties).is_length(1)

    def test_when_politician_exists_do_not_create_politician(self):
        cases = [
            case_data(
                {
                    "politician": {
                        "external_id": "politician.id",
                        "full_name": "politician.full_name",
                    },
                }
            )
        ]

        PoliticianFactory.create(
            external_id="politician.id", full_name="politician.full_name"
        )

        ImportData().perform(cases)

        politicians = Politician.objects.filter(external_id="politician.id")
        assert_that(politicians).is_length(1)

    def test_when_sources_do_not_exist_create_sources(self):
        cases = [
            case_data(
                {
                    "sources": [
                        {
                            "external_id": "case.source.id",
                            "url": "https://example.com",
                            "title": "case.source.title",
                            "publisher": "case.source.publisher",
                            "published_at": datetime(
                                year=2026, month=1, day=4, tzinfo=timezone.utc
                            ),
                            "type": "case.source.type",
                        }
                    ],
                }
            )
        ]

        ImportData().perform(cases)

        sources = Source.objects.filter(external_id="case.source.id")
        source = sources.first()
        assert_that(sources).is_length(1)
        attributes = {
            "external_id": "case.source.id",
            "url": "https://example.com",
            "title": "case.source.title",
            "publisher": "case.source.publisher",
            "published_at": date(year=2026, month=1, day=4),
            "type": "case.source.type",
        }
        for key, value in attributes.items():
            assert_that(getattr(source, key)).is_equal_to(value)

    def test_when_legal_case_exists_and_has_been_updated_then_update_case(self):
        party = PartyFactory.create()
        politician = PoliticianFactory.create()
        LegalCase.objects.create(
            external_id="case.id",
            category="old.category",
            external_updated_at=datetime(
                year=2000, month=1, day=3, tzinfo=timezone.utc
            ),
            title="old.title",
            description="old.description",
            status="old.status",
            date=datetime(year=2000, month=1, day=1, tzinfo=timezone.utc),
            verdict_date=datetime(year=2000, month=1, day=2, tzinfo=timezone.utc),
            politician=politician,
            party=party,
        )
        cases = [
            case_data(
                {
                    "external_id": "case.id",
                    "category": "new.category",
                    "external_updated_at": datetime(
                        year=2001, month=1, day=3, tzinfo=timezone.utc
                    ),
                    "title": "new.title",
                    "description": "new.description",
                    "status": "new.status",
                    "date": datetime(year=2026, month=1, day=1, tzinfo=timezone.utc),
                    "verdict_date": datetime(
                        year=2026, month=1, day=2, tzinfo=timezone.utc
                    ),
                }
            )
        ]

        ImportData().perform(cases)

        query = LegalCase.objects.filter(external_id="case.id")
        legal_case_db = query.first()
        attributes = {
            "external_id": "case.id",
            "category": "new.category",
            "external_updated_at": datetime(
                year=2001, month=1, day=3, tzinfo=timezone.utc
            ),
            "title": "new.title",
            "description": "new.description",
            "status": "new.status",
            "date": date(2026, 1, 1),
            "verdict_date": date(2026, 1, 2),
        }
        assert_that(query).is_length(1)
        for key, value in attributes.items():
            assert_that(getattr(legal_case_db, key)).is_equal_to(value)

    def test_when_legal_case_exists_and_has_not_been_updated_does_not_update(self):
        party = PartyFactory.create()
        politician = PoliticianFactory.create()
        LegalCase.objects.create(
            external_id="case.id",
            category="old.category",
            external_updated_at=datetime(
                year=2000, month=1, day=3, tzinfo=timezone.utc
            ),
            title="old.title",
            description="old.description",
            status="old.status",
            date=datetime(year=2000, month=1, day=1, tzinfo=timezone.utc),
            verdict_date=datetime(year=2000, month=1, day=2, tzinfo=timezone.utc),
            politician=politician,
            party=party,
        )
        cases = [
            case_data(
                {
                    "external_id": "case.id",
                    "category": "case.category",
                    "external_updated_at": datetime(
                        year=2000, month=1, day=3, tzinfo=timezone.utc
                    ),
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "date": datetime(year=2026, month=1, day=1, tzinfo=timezone.utc),
                    "verdict_date": datetime(
                        year=2026, month=1, day=2, tzinfo=timezone.utc
                    ),
                }
            )
        ]

        ImportData().perform(cases)

        query = LegalCase.objects.filter(external_id="case.id")
        legal_case_db = query.first()
        attributes = {
            "external_id": "case.id",
            "category": "old.category",
            "external_updated_at": datetime(
                year=2000, month=1, day=3, tzinfo=timezone.utc
            ),
            "title": "old.title",
            "description": "old.description",
            "status": "old.status",
            "date": date(2000, 1, 1),
            "verdict_date": date(2000, 1, 2),
        }
        assert_that(query).is_length(1)
        for key, value in attributes.items():
            assert_that(getattr(legal_case_db, key)).is_equal_to(value)

    def test_when_current_legal_case_is_newer_does_not_update(self):
        party = PartyFactory.create()
        politician = PoliticianFactory.create()
        LegalCase.objects.create(
            external_id="case.id",
            category="old.category",
            external_updated_at=datetime(
                year=2026, month=1, day=3, tzinfo=timezone.utc
            ),
            title="old.title",
            description="old.description",
            status="old.status",
            date=datetime(year=2000, month=1, day=1, tzinfo=timezone.utc),
            verdict_date=datetime(year=2000, month=1, day=2, tzinfo=timezone.utc),
            politician=politician,
            party=party,
        )
        cases = [
            case_data(
                {
                    "external_id": "case.id",
                    "category": "case.category",
                    "external_updated_at": datetime(
                        year=2025, month=1, day=3, tzinfo=timezone.utc
                    ),
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "date": datetime(year=2026, month=1, day=1, tzinfo=timezone.utc),
                    "verdict_date": datetime(
                        year=2026, month=1, day=2, tzinfo=timezone.utc
                    ),
                }
            )
        ]

        ImportData().perform(cases)

        query = LegalCase.objects.filter(external_id="case.id")
        legal_case_db = query.first()
        attributes = {
            "external_id": "case.id",
            "category": "old.category",
            "external_updated_at": datetime(
                year=2026, month=1, day=3, tzinfo=timezone.utc
            ),
            "title": "old.title",
            "description": "old.description",
            "status": "old.status",
            "date": date(2000, 1, 1),
            "verdict_date": date(2000, 1, 2),
        }
        assert_that(query).is_length(1)
        for key, value in attributes.items():
            assert_that(getattr(legal_case_db, key)).is_equal_to(value)

    def test_when_source_already_exists_does_not_update_source(self):
        legal_case = LegalCaseFactory.create()
        Source.objects.create(
            external_id="source.id",
            url="source.url",
            title="source.title",
            publisher="source.publisher",
            published_at=date(year=2025, month=1, day=4),
            type="source.type",
            legal_case=legal_case,
        )
        cases = [
            case_data(
                {
                    "sources": [
                        {
                            "external_id": "source.id",
                            "url": "source.url_1",
                            "title": "source.title_1",
                            "publisher": "source.publisher_1",
                            "published_at": datetime(
                                year=2025, month=1, day=1, tzinfo=timezone.utc
                            ),
                            "type": "source.type_1",
                        }
                    ],
                }
            )
        ]

        ImportData().perform(cases)

        source_db = Source.objects.filter(external_id="source.id").first()
        attributes = {
            "external_id": "source.id",
            "url": "source.url",
            "title": "source.title",
            "publisher": "source.publisher",
            "published_at": date(year=2025, month=1, day=4),
            "type": "source.type",
        }
        assert_that(Source.objects.all()).is_length(1)
        for key, value in attributes.items():
            assert_that(getattr(source_db, key)).is_equal_to(value)

    def test_when_there_are_several_case_create_all_cases(self):
        cases = [
            case_data(
                {
                    "external_id": "case1.id",
                    "category": "case1.category",
                    "external_updated_at": datetime(
                        year=2026, month=2, day=3, tzinfo=timezone.utc
                    ),
                    "title": "case1.title",
                    "description": "case1.description",
                    "status": "case1.status",
                    "date": datetime(year=2026, month=2, day=1, tzinfo=timezone.utc),
                    "verdict_date": datetime(
                        year=2026, month=2, day=2, tzinfo=timezone.utc
                    ),
                }
            ),
            case_data(
                {
                    "external_id": "case2.id",
                    "category": "case2.category",
                    "external_updated_at": datetime(
                        year=2026, month=3, day=3, tzinfo=timezone.utc
                    ),
                    "title": "case2.title",
                    "description": "case2.description",
                    "status": "case2.status",
                    "date": datetime(year=2026, month=3, day=1, tzinfo=timezone.utc),
                    "verdict_date": datetime(
                        year=2026, month=3, day=2, tzinfo=timezone.utc
                    ),
                }
            ),
        ]

        ImportData().perform(cases)

        data_attributes = [
            {
                "external_id": "case1.id",
                "category": "case1.category",
                "external_updated_at": datetime(
                    year=2026, month=2, day=3, tzinfo=timezone.utc
                ),
                "title": "case1.title",
                "description": "case1.description",
                "status": "case1.status",
                "date": date(2026, 2, 1),
                "verdict_date": date(2026, 2, 2),
            },
            {
                "external_id": "case2.id",
                "category": "case2.category",
                "external_updated_at": datetime(
                    year=2026, month=3, day=3, tzinfo=timezone.utc
                ),
                "title": "case2.title",
                "description": "case2.description",
                "status": "case2.status",
                "date": date(2026, 3, 1),
                "verdict_date": date(2026, 3, 2),
            },
        ]

        for attributes in data_attributes:
            legal_case = LegalCase.objects.get(external_id=attributes["external_id"])
            for attribute, value in attributes.items():
                assert_that(getattr(legal_case, attribute)).is_equal_to(value)

    def test_when_there_are_several_case_create_all_party(self):
        cases = [
            case_data(
                {
                    "external_id": "case1.id",
                    "party": {
                        "abbreviation": "case1.party.shortName",
                        "name": "case1.party.name",
                    },
                }
            ),
            case_data(
                {
                    "external_id": "case2.id",
                    "party": {
                        "abbreviation": "case2.party.shortName",
                        "name": "case2.party.name",
                    },
                }
            ),
        ]

        ImportData().perform(cases)

        data_attributes = {
            "case1.id": {
                "abbreviation": "case1.party.shortName",
                "name": "case1.party.name",
            },
            "case2.id": {
                "abbreviation": "case2.party.shortName",
                "name": "case2.party.name",
            },
        }

        for id, attributes in data_attributes.items():
            party = LegalCase.objects.get(external_id=id).party
            for attribute, value in attributes.items():
                assert_that(getattr(party, attribute)).is_equal_to(value)

    def test_when_there_are_several_case_politician_create_all_politician(self):
        cases = [
            case_data(
                {
                    "external_id": "case1.id",
                    "politician": {
                        "external_id": "case1.politician.id",
                        "full_name": "case1.politician.fullName",
                    },
                }
            ),
            case_data(
                {
                    "external_id": "case2.id",
                    "politician": {
                        "external_id": "case2.politician.id",
                        "full_name": "case2.politician.fullName",
                    },
                }
            ),
        ]

        ImportData().perform(cases)

        data_attributes = {
            "case1.id": {
                "external_id": "case1.politician.id",
                "full_name": "case1.politician.fullName",
            },
            "case2.id": {
                "external_id": "case2.politician.id",
                "full_name": "case2.politician.fullName",
            },
        }

        for id, attributes in data_attributes.items():
            politician = LegalCase.objects.get(external_id=id).politician
            for attribute, value in attributes.items():
                assert_that(getattr(politician, attribute)).is_equal_to(value)

    def test_when_there_are_several_sources_create_all_sources(self):
        cases = [
            case_data(
                {
                    "external_id": "case1.id",
                    "sources": [
                        {
                            "external_id": "case1.source.id",
                            "url": "case1.source.url",
                            "title": "case1.source.title",
                            "publisher": "case1.source.publisher",
                            "published_at": date(year=2026, month=3, day=4),
                            "type": "case1.source.type",
                        }
                    ],
                }
            ),
            case_data(
                {
                    "external_id": "case2.id",
                    "sources": [
                        {
                            "external_id": "case2.source.id",
                            "url": "case2.source.url",
                            "title": "case2.source.title",
                            "publisher": "case2.source.publisher",
                            "published_at": date(year=2026, month=2, day=4),
                            "type": "case2.source.type",
                        }
                    ],
                }
            ),
        ]

        ImportData().perform(cases)

        data_attributes = {
            "case1.id": {
                "external_id": "case1.source.id",
                "url": "case1.source.url",
                "title": "case1.source.title",
                "publisher": "case1.source.publisher",
                "published_at": date(year=2026, month=3, day=4),
                "type": "case1.source.type",
            },
            "case2.id": {
                "external_id": "case2.source.id",
                "url": "case2.source.url",
                "title": "case2.source.title",
                "publisher": "case2.source.publisher",
                "published_at": date(year=2026, month=2, day=4),
                "type": "case2.source.type",
            },
        }

        for id, attributes in data_attributes.items():
            source = LegalCase.objects.get(external_id=id).sources.first()
            for attribute, value in attributes.items():
                assert_that(getattr(source, attribute)).is_equal_to(value)


def case_data(data):
    return {
        "external_id": "case.id",
        "category": "case.category",
        "external_updated_at": datetime(year=2026, month=1, day=3, tzinfo=timezone.utc),
        "title": "case.title",
        "description": "case.description",
        "status": "case.status",
        "date": datetime(year=2026, month=1, day=1, tzinfo=timezone.utc),
        "verdict_date": datetime(year=2026, month=1, day=2, tzinfo=timezone.utc),
        "party": {
            "abbreviation": "party.shortName",
            "name": "party.name",
        },
        "politician": {
            "external_id": "politician.id",
            "full_name": "politician.fullName",
        },
        "sources": [
            {
                "external_id": "case2.source.id",
                "url": "case2.source.url",
                "title": "case2.source.title",
                "publisher": "case2.source.publisher",
                "published_at": datetime(
                    year=2026, month=1, day=4, tzinfo=timezone.utc
                ),
                "type": "case2.source.type",
            }
        ],
    } | data
