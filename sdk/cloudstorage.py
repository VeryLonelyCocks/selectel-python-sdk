import uuid

import io

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
        url = self.CS_URL + 'auth/v1.0'

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
            'object_count': response_headers['x-account-object-count'],
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

    def delete_container(self, name):
        url = self.storage_url + '/' + name

        return self.request(url, headers={
            'X-Auth-Token': self.auth_token
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

        import pycurl

        url = self.storage_url + '/' + container + '/' + file

        c = pycurl.Curl()

        stream = io.BytesIO()

        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEDATA, stream)

        c.setopt(c.HTTPHEADER, [
            'X-Auth-Token: {}'.format(self.auth_token)
        ])

        c.perform()
        code = c.getinfo(pycurl.HTTP_CODE)
        c.close()

        return stream
        # if type == 'private':
        #     headers['X-Auth-Token'] = self.auth_token

        # response = self.request(url, headers=headers)

        # return response.content

    def upload(self, container, file_name, file, content_type, content_length, expire_time=None, delete_after=None):

        import pycurl

        url = self.storage_url + '/' + container + '/' + file_name

        c = pycurl.Curl()

        stream = io.BytesIO(file)

        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.UPLOAD, 1)
        c.setopt(pycurl.INFILESIZE, content_length)
        c.setopt(pycurl.READDATA, stream)

        c.setopt(c.HTTPHEADER, [
            'X-Auth-Token: {}'.format(self.auth_token),
            'X-Detect-Content-Type: {}'.format('true'),
            'Content-Type: {}'.format(content_type),
            'Content-Length: {}'.format(str(content_length))
        ])

        c.perform()
        code = c.getinfo(pycurl.HTTP_CODE)

        c.close()
        return code

    def delete(self, container, file):

        url = self.storage_url + '/' + container + '/' + file

        headers = {
            'X-Auth-Token': self.auth_token
        }

        return self.request(url, headers=headers, method='DELETE')

    def set_link_key(self, key):

        url = self.storage_url

        headers = {
            'X-Auth-Token': self.auth_token,
            'X-Account-Meta-Temp-URL-Key': key
        }

        return self.request(url, headers=headers, method='POST')