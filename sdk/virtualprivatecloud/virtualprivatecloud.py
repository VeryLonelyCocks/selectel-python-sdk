from sdk.virtualprivatecloud.api import API


class VirtualPrivateCloud(API):
    def __init__(self, token):
        self._token = token

    def _send_request(self, url):
        headers = {
            'X-token': self._token
        }

        response = self.request(url, headers=headers)

        return response

    def get_list_projects(self):
        url = self.URL + "projects"

        response = self._send_request(url)

        list_projects = response.json()['projects']

        return list_projects

    def get_configuration_about_project(self, project_id):
        url = self.URL + "projects/" + str(project_id)

        response = self._send_request(url)

        return response.json()

    def get_quotas(self):
        url = self.URL + "quotas"

        response = self._send_request(url)

        return response.json()

    def get_free_quotas(self):
        url = self.URL + "quotas/free"

        response = self._send_request(url)

        return response.json()

    def get_quotas_for_all_projects(self):
        url = self.URL + "quotas/projects"

        response = self._send_request(url)

        return response.json()

    def get_quotas_for_project(self, project_id):
        url = self.URL + "quotas/projects/" + str(project_id)

        response = self._send_request(url)

        return response.json()

    def get_traffic(self):
        url = self.URL + "traffic"

        response = self._send_request(url)

        return response.json()

    def get_users(self):
        url = self.URL + "users"

        response = self._send_request(url)

        return response.json()
