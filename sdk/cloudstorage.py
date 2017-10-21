import uuid

from .api import API


class CloudStorage(API):

    def __init__(self, user, password=None):

        self.authorized = False

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

        if response.status_code == 403:
            self.authorized = False
        else:
            self.authorized = True

        response_headers = response.headers

        result = {
            'storage_token': response_headers.get('x-storage-token', None),
            'auth_token_expire': response_headers.get('x-expire-auth-token', None),
            'auth_token': response_headers.get('x-auth-token', None),
            'storage_url': response_headers.get('x-storage-url', None),
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
        response = self.request(
            url,
            headers={
                'X-Auth-Token': self.auth_token
            },
            params={
                'format': 'json'
            }
        )

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

        import urllib3
        http = urllib3.PoolManager()
        file = http.request('GET', url, headers=headers)

        # name = str(uuid.uuid4()) + '.tmp'
        # handle = open(name, "xb")
        # for chunk in response.iter_content(chunk_size=512):
        #     if chunk:  # filter out keep-alive new chunks
        #         handle.write(chunk)

        return file.data

    def upload(self, container, file_name, file, content_type, content_length, expire_time=None, delete_after=None):

        url = self.storage_url + '/' + container + '/' + file_name

        headers = {
            'X-Auth-Token': self.auth_token,
            'X-Detect-Content-Type': 'true',
            'Content-Type': content_type,
            'Content-Length': str(content_length)
        }

        if expire_time is not None:
            headers['X-Delete-At'] = expire_time
        if expire_time is not None:
            headers['X-Delete-After'] = delete_after

        files = {
            'file': file
        }

        return self.request(url, headers=headers, files=files, method='PUT')

    def delete(self, container, file):

        url = self.storage_url + '/' + container + '/' + file

        headers = {
            'X-Auth-Token': self.auth_token
        }

        return self.request(url, headers=headers, method='DELETE')
