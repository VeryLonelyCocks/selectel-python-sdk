from .api import API


class CloudStorage(API):

    def __init__(self, user, password=None):
        if password is not None:
            self.auth(user, password)
        else:
            self.auth_token = user

    def set_storage_url(self, storage_url):
        self.storage_url = storage_url
        
    def auth(self, user, password):
        url = self.URL + 'auth/v1.0'

        headers = {
            'X-Auth-User': str(user),
            'X-Auth-Key': password
        }

        response = self.request(url, headers=headers)

        response_headers = response.headers

        result = {
            'storage_token': response_headers['x-storage-token'],
            'auth_token_expire': response_headers['x-expire-auth-token'],
            'auth_token': response_headers['x-auth-token'],
            'storage_url': response_headers['x-storage-url']
        }

        self.storage_url = result['storage_url']
        self.storage_token = result['storage_token']
        self.auth_token = result['auth_token']

        return result

    def account_info(self):
        url = self.storage_url
        response = self.request(url, headers={
            'X-Auth-Token': self.auth_token
        }, method='HEAD')

        response_headers = response.headers

        result = {
            'bytes_used': response_headers['x-account-bytes-used'],
            'container_count': response_headers['x-account-container-count'],
            'object_count': response_headers['x-account-object-count']
        }

        return result

    def containers_list(self):
        url = self.storage_url
        response = self.request(url,
                                headers={
                                    'X-Auth-Token': self.auth_token
                                },
                                params={
                                    'format': 'json'
                                })

        return response.json()

    def new_container(self, name, type='private'):
        url = self.storage_url + '/' + name

        return self.request(url, headers={
            'X-Auth-Token': self.auth_token,
            'X-Container-Meta-Type': type
        }, method='PUT')

    def container_info(self, name):
        url = self.storage_url + '/' + name

        response = self.request(url, headers={
            'X-Auth-Token': self.auth_token,
        }, method='HEAD')

        response_headers = response.headers

        result = {
            'object_count': response_headers['x-container-object-count'],
            'bytes_used': response_headers['x-container-bytes-used'],
            'transfered_bytes': response_headers.get('x-transfered-bytes', 0),
            'received_bytes': response_headers.get('x-received-bytes', 0),
            'type': response_headers['x-container-meta-type'],
            'meta': response_headers.get('x-container-meta-some', ''),
            'domains': response_headers['x-container-domains']
        }

        return result

    def update_container(self, name, type='private'):
        url = self.storage_url + '/' + name

        return self.request(url, headers={
            'X-Auth-Token': self.auth_token,
            'X-Container-Meta-Type': type
        }, method='POST')

    def delete_container(self, name, type='private'):
        url = self.storage_url + '/' + name

        return self.request(url, headers={
            'X-Auth-Token': self.auth_token,
            'X-Container-Meta-Type': type
        }, method='DELETE')

    def get_files(self, container, limit=None, marker=None, prefix=None, path=None, delimiter=None, format='json'):
        url = self.storage_url + '/' + container

        params = {}

        if limit is not None:
            params['limit'] = limit
        if marker is not None:
            params['marker'] = marker
        if prefix is not None:
            params['prefix'] = prefix
        if path is not None:
            params['path'] = path
        if delimiter is not None:
            params['delimiter'] = delimiter

        params['format'] = format

        response = self.request(url, headers={
            'X-Auth-Token': self.auth_token
        }, params=params)

        if format == 'json':
            return response.json()
        else:
            return response.text

    def download(self, container, file, type='private'):

        url = self.storage_url + '/' + container + '/' + file

        headers = {}

        if type == 'private':
            headers['X-Auth-Token'] = self.auth_token

        response = self.request(url, headers=headers)

        return response.content

    def upload(self, container, file_name, file, expire_time=None, delete_after=None):

        url = self.storage_url + '/' + container + '/' + file_name

        headers = {
            'X-Auth-Token': self.auth_token
        }

        if expire_time is not None:
            headers['X-Delete-At'] = expire_time
        if expire_time is not None:
            headers['X-Delete-After'] = delete_after

        files = {
            'file': file
        }

        self.request(url, headers=headers, files=files, method='PUT')

    def delete(self, container, file):

        url = self.storage_url + '/' + container + '/' + file

        headers = {
            'X-Auth-Token': self.auth_token
        }

        return self.request(url, headers=headers, method='DELETE')
