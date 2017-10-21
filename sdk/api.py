import requests


class API:
    cloud_storage_URL = 'https://api.selcdn.ru/'
    vpc_URL = 'https://api.selectel.ru/vpc/resell/v2/'

    def request(self, url, headers=None, params=None, method='GET', files=None):

        if headers is None:
            headers = {}
        if params is None:
            params = {}

        return requests.request(method, url, headers=headers, params=params, files=files)
