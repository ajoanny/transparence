from django.test import TestCase
from transparence.models import Party


class ApiPartyTest(TestCase):
  def test_when_there_is_no_data_it_returns_no_data(self):
    response = self.client.get('/api/parties/')

    self.assertEqual(response.status_code, 200)

    data = response.json()
    self.assertEqual(data, {
      "data": [],
      "pagination": {
        "page": 1,
        "page_size": 10,
        "pages_count": 1,
        "total": 0,
      }
    })

  def test_when_there_is_no_pagination_parameter_and_there_less_than_10_parties_given_it_returns_all_existing_parties(self):
      Party.objects.create(name="Liberty Alliance", abbreviation="LA")
      Party.objects.create(name="Progressive Front", abbreviation="PF")

      response = self.client.get('/api/parties/')

      self.assertEqual(response.status_code, 200)

      data = response.json()
      self.assertEqual(data, {
        "data": [
          {"name": "Liberty Alliance", "abbreviation": "LA"},
          {"name": "Progressive Front", "abbreviation": "PF"}
        ],
        "pagination": {
          "page": 1,
          "page_size": 10,
          "pages_count": 1,
          "total": 2,
        }
      })

  def test_when_there_is_a_page_number_given_it_returns_all_parties_for_the_given_page(self):
    for i in range(1,12):
      Party.objects.create(name=f"{i}", abbreviation=f"{i}")

    response = self.client.get('/api/parties/?page=2')

    self.assertEqual(response.status_code, 200)

    data = response.json()
    self.assertEqual(data, {
      "data": [
        {"name": "9", "abbreviation": "9"},
      ],
      "pagination": {
        "page": 2,
        "page_size": 10,
        "pages_count": 2,
        "total": 11,
      }
    })

  def test_when_there_is_a_page_size_given_it_returns_the_parties_requested(self):
    for i in range(1,10):
      Party.objects.create(name=f"{i}", abbreviation=f"{i}")

    response = self.client.get('/api/parties/?pageSize=3')

    self.assertEqual(response.status_code, 200)

    data = response.json()
    self.assertEqual(data, {
      "data": [
        {"name": "1", "abbreviation": "1"},
        {"name": "2", "abbreviation": "2"},
        {"name": "3", "abbreviation": "3"},
      ],
      "pagination": {
        "page": 1,
        "page_size": 3,
        "pages_count": 3,
        "total": 9,
      }
    })
