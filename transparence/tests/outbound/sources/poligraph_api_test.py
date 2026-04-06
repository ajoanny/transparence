from datetime import date, datetime
from django.test import TestCase
from assertpy import assert_that

from config import settings
from transparence.outbound.sources.poligraph_api import fetch_data
from transparence.tests.doubles.http_double import HttpDouble


class PoligraphApiTest(TestCase):

    def test_when_no_data_returns_empty_array(self):
        response = {
            "data": [],
            "pagination": {"page": 1, "limit": 20, "total": 0, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        assert_that(results["data"]).is_equal_to([])

    def test_it_returns_data_from_api(self):
        response = {
            "data": [
                {
                    "id": "case.id",
                    "factsDate": f"{date(2026,1,1)}",
                    "verdictDate": f"{date(2026,1,2)}",
                    "updatedAt": f"{date(2026,1,3)}",
                    "category": "case.category",
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "partyAtTime": {
                        "shortName": "party.shortName",
                        "name": "party.name",
                    },
                    "politician": {
                        "id": "politician.id",
                        "fullName": "politician.fullName",
                        "currentParty": None,
                    },
                    "sources": [
                        {
                            "id": "source.id1",
                            "url": "source.url1",
                            "title": "source.title1",
                            "publisher": "source.publisher1",
                            "publishedAt": f"{date(2026,1,4)}",
                            "sourceType": "source.type1",
                        },
                        {
                            "id": "source.id2",
                            "url": "source.url2",
                            "title": "source.title2",
                            "publisher": "source.publisher2",
                            "publishedAt": f"{date(2026,1,5)}",
                            "sourceType": "source.type2",
                        },
                    ],
                }
            ],
            "pagination": {"page": 1, "limit": 20, "total": 1, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        expected = [
            {
                "external_id": "case.id",
                "category": "case.category",
                "external_updated_at": datetime(2026, 1, 3),
                "title": "case.title",
                "description": "case.description",
                "status": "case.status",
                "date": datetime(2026, 1, 1),
                "verdict_date": datetime(2026, 1, 2),
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
                        "external_id": "source.id1",
                        "url": "source.url1",
                        "title": "source.title1",
                        "publisher": "source.publisher1",
                        "published_at": datetime(2026, 1, 4),
                        "type": "source.type1",
                    },
                    {
                        "external_id": "source.id2",
                        "url": "source.url2",
                        "title": "source.title2",
                        "publisher": "source.publisher2",
                        "published_at": datetime(2026, 1, 5),
                        "type": "source.type2",
                    },
                ],
            }
        ]
        assert_that(results["data"]).is_equal_to(expected)

    def test_when_party_at_not_present_returns_current_party(self):
        response = {
            "data": [
                {
                    "id": "case.id",
                    "factsDate": f"{date(2026,1,1)}",
                    "verdictDate": f"{date(2026,1,2)}",
                    "updatedAt": f"{date(2026,1,3)}",
                    "category": "case.category",
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "partyAtTime": None,
                    "politician": {
                        "id": "politician.id",
                        "fullName": "politician.fullName",
                        "currentParty": {
                            "shortName": "politician.currentParty.shortName",
                            "name": "politician.currentParty.name",
                        },
                    },
                    "sources": [],
                }
            ],
            "pagination": {"page": 1, "limit": 20, "total": 1, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        expected = [
            {
                "external_id": "case.id",
                "category": "case.category",
                "external_updated_at": datetime(2026, 1, 3),
                "title": "case.title",
                "description": "case.description",
                "status": "case.status",
                "date": datetime(2026, 1, 1),
                "verdict_date": datetime(2026, 1, 2),
                "party": {
                    "abbreviation": "politician.currentParty.shortName",
                    "name": "politician.currentParty.name",
                },
                "politician": {
                    "external_id": "politician.id",
                    "full_name": "politician.fullName",
                },
                "sources": [],
            }
        ]
        assert_that(results["data"]).is_equal_to(expected)

    def test_when_current_party_not_present_returns_current_party(self):
        response = {
            "data": [
                {
                    "id": "case.id",
                    "factsDate": f"{date(2026,1,1)}",
                    "verdictDate": f"{date(2026,1,2)}",
                    "updatedAt": f"{date(2026,1,3)}",
                    "category": "case.category",
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "partyAtTime": None,
                    "politician": {
                        "id": "politician.id",
                        "fullName": "politician.fullName",
                        "currentParty": None,
                    },
                    "sources": [],
                }
            ],
            "pagination": {"page": 1, "limit": 20, "total": 1, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        expected = [
            {
                "external_id": "case.id",
                "category": "case.category",
                "external_updated_at": datetime(2026, 1, 3),
                "title": "case.title",
                "description": "case.description",
                "status": "case.status",
                "date": datetime(2026, 1, 1),
                "verdict_date": datetime(2026, 1, 2),
                "party": {
                    "abbreviation": "UNKNOWN",
                    "name": "UNKNOWN",
                },
                "politician": {
                    "external_id": "politician.id",
                    "full_name": "politician.fullName",
                },
                "sources": [],
            }
        ]
        assert_that(results["data"]).is_equal_to(expected)

    def test_when_verdict_date_missing(self):
        response = {
            "data": [
                {
                    "id": "case.id",
                    "factsDate": f"{date(2026,1,1)}",
                    "verdictDate": None,
                    "updatedAt": f"{date(2026,1,3)}",
                    "category": "case.category",
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "partyAtTime": None,
                    "politician": {
                        "id": "politician.id",
                        "fullName": "politician.fullName",
                        "currentParty": None,
                    },
                    "sources": [],
                },
            ],
            "pagination": {"page": 1, "limit": 20, "total": 1, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        expected = [
            {
                "external_id": "case.id",
                "category": "case.category",
                "external_updated_at": datetime(2026, 1, 3),
                "title": "case.title",
                "description": "case.description",
                "status": "case.status",
                "date": datetime(2026, 1, 1),
                "verdict_date": None,
                "party": {
                    "abbreviation": "UNKNOWN",
                    "name": "UNKNOWN",
                },
                "politician": {
                    "external_id": "politician.id",
                    "full_name": "politician.fullName",
                },
                "sources": [],
            }
        ]
        assert_that(results["data"]).is_equal_to(expected)

    def test_when_facts_date_missing(self):
        response = {
            "data": [
                {
                    "id": "case.id",
                    "factsDate": None,
                    "verdictDate": f"{date(2026,1,2)}",
                    "updatedAt": f"{date(2026,1,3)}",
                    "category": "case.category",
                    "title": "case.title",
                    "description": "case.description",
                    "status": "case.status",
                    "partyAtTime": None,
                    "politician": {
                        "id": "politician.id",
                        "fullName": "politician.fullName",
                        "currentParty": None,
                    },
                    "sources": [],
                }
            ],
            "pagination": {"page": 1, "limit": 20, "total": 1, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        expected = [
            {
                "external_id": "case.id",
                "category": "case.category",
                "external_updated_at": datetime(2026, 1, 3),
                "title": "case.title",
                "description": "case.description",
                "status": "case.status",
                "date": None,
                "verdict_date": datetime(2026, 1, 2),
                "party": {
                    "abbreviation": "UNKNOWN",
                    "name": "UNKNOWN",
                },
                "politician": {
                    "external_id": "politician.id",
                    "full_name": "politician.fullName",
                },
                "sources": [],
            }
        ]
        assert_that(results["data"]).is_equal_to(expected)

    def test_when_several_cases(self):
        response = {
            "data": [
                {
                    "id": "case.id1",
                    "factsDate": f"{date(2026,2,1)}",
                    "verdictDate": f"{date(2026,2,2)}",
                    "updatedAt": f"{date(2026,2,3)}",
                    "category": "case.category1",
                    "title": "case.title1",
                    "description": "case.description1",
                    "status": "case.status1",
                    "partyAtTime": {
                        "shortName": "party.shortName1",
                        "name": "party.name1",
                    },
                    "politician": {
                        "id": "politician.id1",
                        "fullName": "politician.fullName1",
                        "currentParty": None,
                    },
                    "sources": [
                        {
                            "id": "case1.source.id",
                            "url": "case1.source.url",
                            "title": "case1.source.title",
                            "publisher": "case1.source.publisher",
                            "publishedAt": f"{date(2026,2,4)}",
                            "sourceType": "case1.source.type",
                        },
                    ],
                },
                {
                    "id": "case.id2",
                    "factsDate": f"{date(2025,1,1)}",
                    "verdictDate": f"{date(2025,1,2)}",
                    "updatedAt": f"{date(2025,1,3)}",
                    "category": "case.category2",
                    "title": "case.title2",
                    "description": "case.description2",
                    "status": "case.status2",
                    "partyAtTime": {
                        "shortName": "party.shortName2",
                        "name": "party.name2",
                    },
                    "politician": {
                        "id": "politician.id2",
                        "fullName": "politician.fullName2",
                        "currentParty": None,
                    },
                    "sources": [
                        {
                            "id": "case2.source.id",
                            "url": "case2.source.url",
                            "title": "case2.source.title",
                            "publisher": "case2.source.publisher",
                            "publishedAt": f"{date(2025,1,4)}",
                            "sourceType": "case2.source.type",
                        }
                    ],
                },
            ],
            "pagination": {"page": 1, "limit": 20, "total": 1, "totalPages": 1},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)
        expected = [
            {
                "external_id": "case.id1",
                "category": "case.category1",
                "external_updated_at": datetime(2026, 2, 3),
                "title": "case.title1",
                "description": "case.description1",
                "status": "case.status1",
                "date": datetime(2026, 2, 1),
                "verdict_date": datetime(2026, 2, 2),
                "party": {
                    "abbreviation": "party.shortName1",
                    "name": "party.name1",
                },
                "politician": {
                    "external_id": "politician.id1",
                    "full_name": "politician.fullName1",
                },
                "sources": [
                    {
                        "external_id": "case1.source.id",
                        "url": "case1.source.url",
                        "title": "case1.source.title",
                        "publisher": "case1.source.publisher",
                        "published_at": datetime(2026, 2, 4),
                        "type": "case1.source.type",
                    },
                ],
            },
            {
                "external_id": "case.id2",
                "category": "case.category2",
                "external_updated_at": datetime(2025, 1, 3),
                "title": "case.title2",
                "description": "case.description2",
                "status": "case.status2",
                "date": datetime(2025, 1, 1),
                "verdict_date": datetime(2025, 1, 2),
                "party": {
                    "abbreviation": "party.shortName2",
                    "name": "party.name2",
                },
                "politician": {
                    "external_id": "politician.id2",
                    "full_name": "politician.fullName2",
                },
                "sources": [
                    {
                        "external_id": "case2.source.id",
                        "url": "case2.source.url",
                        "title": "case2.source.title",
                        "publisher": "case2.source.publisher",
                        "published_at": datetime(2025, 1, 4),
                        "type": "case2.source.type",
                    },
                ],
            },
        ]
        assert_that(results["data"]).is_equal_to(expected)

    def test_when_page_number_is_less_than_total_pages(self):
        response = {
            "data": [],
            "pagination": {"page": 1, "limit": 20, "total": 0, "totalPages": 2},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)

        assert_that(results["has_next"]).is_equal_to(True)

    def test_when_page_number_is_total_pages(self):
        response = {
            "data": [],
            "pagination": {"page": 3, "limit": 20, "total": 0, "totalPages": 3},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)

        assert_that(results["has_next"]).is_equal_to(False)

    def test_when_page_number_is_over_total_pages(self):
        response = {
            "data": [],
            "pagination": {"page": 3, "limit": 20, "total": 0, "totalPages": 2},
        }
        url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page=1"
        http = HttpDouble(url, response)

        results = fetch_data(1, http)

        assert_that(results["has_next"]).is_equal_to(False)
