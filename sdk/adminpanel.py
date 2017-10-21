from .api import API


class AdminPanel(API):

    def __init__(self, token):
        self._token = token

    def _send_request(self, url):
        headers = {
            'X-token': self._token
        }

        response = self.request(url, headers=headers)

        return response

    def get_balance(self):
        url = self.AP_URL + 'billing/balance'

        response = self._send_request(url)

        return response.json()

    def get_user_info(self):
        url = self.AP_URL + "internal/info"

        response = self._send_request(url)

        return response.json()