from dateutil import parser
from config import settings


def fetch_data(page, http):
    url = f"{settings.POLIGRAPH_API_URL}/api/affaires?page={page}"
    response = http.get(url)

    data = [map_case(case) for case in response["data"]]

    return {
        "data": data,
        "has_next": response["pagination"]["page"]
        < response["pagination"]["totalPages"],
    }


def map_case(case):
    date = case["factsDate"] or None
    if date:
        date = parser.parse(date)

    verdict_date = case["verdictDate"] or None
    if verdict_date:
        verdict_date = parser.parse(verdict_date)

    return {
        "external_id": case["id"],
        "external_updated_at": parser.parse(case["updatedAt"]),
        "category": case["category"],
        "title": case["title"],
        "description": case["description"],
        "status": case["status"],
        "date": date,
        "verdict_date": verdict_date,
        "party": map_party(case),
        "politician": map_politician(case),
        "sources": map_sources(case),
    }


def map_politician(case):
    return {
        "external_id": case["politician"]["id"],
        "full_name": case["politician"]["fullName"],
    }


def map_party(case):
    if case["partyAtTime"]:
        abbreviation = case["partyAtTime"]["shortName"]
        name = case["partyAtTime"]["name"]
    elif case["politician"]["currentParty"]:
        abbreviation = case["politician"]["currentParty"]["shortName"]
        name = case["politician"]["currentParty"]["name"]
    else:
        abbreviation = "UNKNOWN"
        name = "UNKNOWN"

    return {
        "abbreviation": abbreviation,
        "name": name,
    }


def map_sources(case):
    return [map_sources_attributes(source) for source in case["sources"]]


def map_sources_attributes(source):
    print(source)
    return {
        "external_id": source["id"],
        "url": source["url"],
        "title": source["title"],
        "publisher": source["publisher"],
        "published_at": parser.parse(source["publishedAt"]),
        "type": source["sourceType"],
    }
