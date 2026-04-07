from transparence.outbound.http.http import Http


class HttpDouble(Http):
    def __init__(self, url, response):
        self._url = url
        self._response = response

    def get(self, url):
        if url != self._url:
            return {}
        return self._response
