from .api import API
import json
import requests
import datetime


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
        url = self.VPC_URL + "projects"

        response = self._send_request(url)

        list_projects = response.json()['projects']

        return list_projects

    def get_configuration_about_project(self, project_id):
        url = self.VPC_URL + "projects/" + str(project_id)

        response = self._send_request(url)

        return response.json()

    def get_quotas(self):
        url = self.VPC_URL + "quotas"

        response = self._send_request(url)

        return response.json()

    def get_free_quotas(self):
        url = self.VPC_URL + "quotas/free"

        response = self._send_request(url)

        return response.json()

    def get_quotas_for_all_projects(self):
        url = self.VPC_URL + "quotas/projects"

        response = self._send_request(url)

        return response.json()

    def get_quotas_for_project(self, project_id):
        url = self.VPC_URL + "quotas/projects/" + str(project_id)

        response = self._send_request(url)

        return response.json()

    def get_traffic(self):
        url = self.VPC_URL + "traffic"

        response = self._send_request(url)

        return response.json()

    def get_users(self):
        url = self.VPC_URL + "users"

        response = self._send_request(url)

        return response.json()

    def get_token(self):
        url = self.VPC_URL + 'tokens'

        data = {"token": {"project_id": "969218765ec44cce94e127c49ea64752"}}
        q = requests.post(url, data=json.dumps(data),
                          headers={'X-token': self._token,'Content-type': 'application/json'})

        self._auth_token = q.json()['token']['id']

        return self._auth_token

    def get_list_subnets(self):
        url = self.VPC_URL + "subnets"

        response = self._send_request(url)

        return response.json()

    def get_info_subnet(self, subnet_id):
        url = self.VPC_URL + "subnets/" + str(subnet_id)

        response = self._send_request(url)

        return response.json()

    def _get_statistic(self, server_id, url_paste):

        if not hasattr(self, '_auth_token'):
            self.get_token()

        today = datetime.datetime.now() - datetime.timedelta(hours=3) - datetime.timedelta(minutes=2)
        yesterday = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:00.000Z")
        today = today.strftime("%Y-%m-%dT%H:%M:00.000Z")

        url = "https://api.selvpc.ru/metric/v1/resource/sel_instance/{server_id}/metric/{url_paste}/measures?" \
              "granularity=300&start={start}&stop={stop}".replace(" ", "").format(server_id=server_id,
                                                                                  start=yesterday,
                                                                                  stop=today,
                                                                                  url_paste=url_paste)

        headers = {
            'X-Auth-Token': self._auth_token,
            'Content-Type': 'application/json'
        }

        response = self.request(url, headers=headers, method="GET")

        return response.json()

    def get_cpu_data(self, server_id):

        return self._get_statistic(server_id, "cpu_util")

    def get_mem_data(self, server_id):

        return self._get_statistic(server_id, "memory.usage")
