from datetime import date
from django.test import TestCase
from transparence.models import Party, Politician, LegalCase, Source
from assertpy import assert_that

from transparence.tests.factories.legal_case import LegalCaseFactory
from transparence.tests.factories.party import PartyFactory


class ApiLegalCaseTest(TestCase):
    def test_list_when_there_is_no_data_it_returns_no_data(self):
        response = self.client.get("/api/legal-cases/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert_that(data).is_equal_to(
            {
                "data": [],
                "pagination": {
                    "page": 1,
                    "page_size": 10,
                    "pages_count": 1,
                    "total": 0,
                },
            },
        )

    def test_list_when_there_is_one_legal_case_it_returns_data_about_legal_case(
        self,
    ):
        politician = Politician.objects.create(
            first_name="John", last_name="Doe", civility="M.", external_id="1"
        )
        party = Party.objects.create(name="Liberty Alliance", abbreviation="LA")

        case = LegalCase.objects.create(
            external_id="CASE-001",
            category="FINANCEMENT_ILLEGAL_CAMPAGNE",
            title="Financement Illegal",
            description="Financement Illegal",
            date=date(2025, 2, 1),
            status="MISE_EN_EXAMEN",
            verdict_date=date(2025, 9, 1),
            party=party,
            politician=politician,
        )

        response = self.client.get("/api/legal-cases/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert_that(data).is_equal_to(
            {
                "data": [
                    {
                        "category": case.category,
                        "title": case.title,
                        "status": case.status,
                        "date": str(case.date),
                        "verdict_date": str(case.verdict_date),
                        "party": {
                            "id": party.id,
                            "name": party.name,
                        },
                        "politician": {
                            "id": politician.id,
                            "first_name": politician.first_name,
                            "last_name": politician.last_name,
                        },
                        "sources": [],
                    },
                ],
                "pagination": {
                    "page": 1,
                    "page_size": 10,
                    "pages_count": 1,
                    "total": 1,
                },
            }
        )

    def test_list_when_there_is_one_legal_case_it_returns_source_of_legal_case(
        self,
    ):
        politician = Politician.objects.create(
            first_name="John", last_name="Doe", civility="M.", external_id="1"
        )
        party = Party.objects.create(name="Liberty Alliance", abbreviation="LA")

        case = LegalCase.objects.create(
            external_id="CASE-001",
            category="FINANCEMENT_ILLEGAL_CAMPAGNE",
            title="Financement Illegal",
            description="Financement Illegal",
            date=date(2025, 2, 1),
            status="MISE_EN_EXAMEN",
            verdict_date=date(2025, 9, 1),
            party=party,
            politician=politician,
        )
        Source.objects.create(
            external_id="SOURCE-001",
            url="http://localhost:8000",
            publisher="1",
            type="PRESSE",
            title="Titre 1",
            description="Description 1",
            published_at=date(2025, 1, 1),
            legal_case=case,
        )
        Source.objects.create(
            external_id="SOURCE-002",
            url="http://localhost:8001",
            publisher="2",
            type="AUTRE",
            title="Titre 2",
            description="Description 2",
            published_at=date(2026, 1, 1),
            legal_case=case,
        )

        response = self.client.get("/api/legal-cases/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        assert_that(data["data"][0]["sources"]).is_equal_to(
            [
                {
                    "url": "http://localhost:8000",
                    "publisher": "1",
                    "type": "PRESSE",
                    "title": "Titre 1",
                    "description": "Description 1",
                    "published_at": str(date(2025, 1, 1)),
                },
                {
                    "url": "http://localhost:8001",
                    "publisher": "2",
                    "type": "AUTRE",
                    "title": "Titre 2",
                    "description": "Description 2",
                    "published_at": str(date(2026, 1, 1)),
                },
            ]
        )

    def test_list_when_no_pagination_and_less_than_10_cases_it_returns_all_cases(
        self,
    ):
        case_1 = LegalCaseFactory(title="Case 1", date=date(2025, 1, 2))
        case_2 = LegalCaseFactory(title="Case 2", date=date(2025, 1, 1))

        response = self.client.get("/api/legal-cases/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        legal_case_names = [case["title"] for case in data["data"]]
        assert_that(legal_case_names).is_equal_to([case_1.title, case_2.title])

    def test_list_when_there_is_pagination_given_it_returns_the_matching_page(
        self,
    ):
        case_1 = LegalCaseFactory(title="Case 1", date=date(2025, 1, 1))
        LegalCaseFactory(title="Case 2", date=date(2025, 3, 1))
        case_3 = LegalCaseFactory(title="Case 3", date=date(2025, 1, 2))
        LegalCaseFactory(title="Case 4", date=date(2025, 4, 1))

        response = self.client.get("/api/legal-cases/?pageSize=2&page=2")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        legal_case_names = [case["title"] for case in data["data"]]
        assert_that(legal_case_names).is_equal_to([case_3.title, case_1.title])

    def test_list_when_there_is_a_filter_party_it_returns_the_matching_page(
        self,
    ):
        party_1 = PartyFactory(abbreviation="A1")
        party_2 = PartyFactory(abbreviation="B1")
        case_1 = LegalCaseFactory(title="Case 1", party=party_1)
        LegalCaseFactory(title="Case 2", party=party_2)

        response = self.client.get(f"/api/legal-cases/?party_id={party_1.id}")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        legal_case_names = [case["title"] for case in data["data"]]
        assert_that(legal_case_names).is_equal_to([case_1.title])
