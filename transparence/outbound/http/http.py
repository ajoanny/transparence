import requests


class Http:
    def get(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
