from django.test import TestCase
from transparence.tests.factories.party import PartyFactory


class ApiPartyTest(TestCase):
    def test_list_when_there_is_no_data_it_returns_no_data(self):
        response = self.client.get("/api/parties/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data,
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

    def test_list_when_no_pagination_and_less_than_10_parties_returns_all(
        self,
    ):
        party_1 = PartyFactory(name="Liberty Alliance", abbreviation="LA")
        party_2 = PartyFactory(name="Progressive Front", abbreviation="PF")

        response = self.client.get("/api/parties/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data,
            {
                "data": [
                    {
                        "party_id": party_1.id,
                        "name": "Liberty Alliance",
                        "abbreviation": "LA",
                    },
                    {
                        "party_id": party_2.id,
                        "name": "Progressive Front",
                        "abbreviation": "PF",
                    },
                ],
                "pagination": {
                    "page": 1,
                    "page_size": 10,
                    "pages_count": 1,
                    "total": 2,
                },
            },
        )

    def test_list_when_page_number_returns_all_parties_for_given_page(
        self,
    ):
        for i in range(1, 12):
            PartyFactory(id=i, name=f"{i}", abbreviation=f"{i}")

        response = self.client.get("/api/parties/?page=2")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data,
            {
                "data": [
                    {"party_id": 9, "name": "9", "abbreviation": "9"},
                ],
                "pagination": {
                    "page": 2,
                    "page_size": 10,
                    "pages_count": 2,
                    "total": 11,
                },
            },
        )

    def test_list_when_there_is_a_page_size_given_it_returns_the_parties_requested(
        self,
    ):
        for i in range(1, 10):
            PartyFactory(id=i, name=f"{i}", abbreviation=f"{i}")

        response = self.client.get("/api/parties/?pageSize=3")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data,
            {
                "data": [
                    {"party_id": 1, "" "name": "1", "abbreviation": "1"},
                    {"party_id": 2, "name": "2", "abbreviation": "2"},
                    {"party_id": 3, "name": "3", "abbreviation": "3"},
                ],
                "pagination": {
                    "page": 1,
                    "page_size": 3,
                    "pages_count": 3,
                    "total": 9,
                },
            },
        )

    def test_detail_when_there_is_no_party_it_returns_404_not_found(
        self,
    ):

        response = self.client.get("/api/parties/1/")

        self.assertEqual(response.status_code, 404)

        data = response.json()
        self.assertEqual(data, {"message": "Not found"})

    def test_detail_when_the_party_exists_it_returns_the_party(self):
        party = PartyFactory(name="Name", abbreviation="ABR")

        response = self.client.get(f"/api/parties/{party.id}/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data,
            {
                "data": {
                    "name": party.name,
                    "abbreviation": party.abbreviation,
                    "party_id": party.id,
                },
            },
        )
