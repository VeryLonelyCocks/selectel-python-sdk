import requests


class API:
    URL = 'https://api.selcdn.ru/'

    def request(self, url, headers=None, params=None, method='GET', files=None, stream=False):

        if headers is None:
            headers = {}
        if params is None:
            params = {}

        return requests.request(method, url, headers=headers, params=params, files=files, stream=stream)
