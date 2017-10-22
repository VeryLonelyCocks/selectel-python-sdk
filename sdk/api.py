import requests


class API:
    CS_URL = 'https://api.selcdn.ru/'
    VPC_URL = 'https://api.selectel.ru/vpc/resell/v2/'
    AP_URL = 'https://my.selectel.ru/api/'

    def request(self, url, headers=None, params=None, method='GET', files=None, data=None, stream=False):

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if data is None:
            data = {}

        return requests.request(method, url, headers=headers, params=params, files=files, data=data, stream=stream)
