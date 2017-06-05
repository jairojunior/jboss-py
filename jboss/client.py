import json
import requests
from requests.auth import HTTPDigestAuth
import jboss.operation_request as op
from jboss.exceptions import OperationError
from jboss.exceptions import AuthError


class Client(object):

    def __init__(self, username, password, host='127.0.0.1', port=9990, timeout=300, headers=None):
        self.url = 'http://{0}:{1}/management'.format(host, port)
        self.auth = HTTPDigestAuth(username, password)
        self.timeout = timeout
        self.headers = {'operation-headers': headers}

    @classmethod
    def from_config(cls, params):
        return cls(params['username'],
                   params['password'],
                   params['host'],
                   params['port'],
                   params['timeout'],
                   params['operation_headers'])

    def _request(self, payload, unsafe=False):
        content_type_header = {'Content-Type': 'application/json'}

        if self.headers['operation-headers'] and not payload['operation'] == 'read-resource':
            payload.update(self.headers)

        response = requests.post(
            self.url,
            data=json.dumps(payload),
            headers=content_type_header,
            auth=self.auth,
            timeout=self.timeout)

        if response.status_code == 401:
            raise AuthError('Invalid credentials.')

        response = response.json()

        if response['outcome'] == 'failed' and not unsafe:
            raise OperationError(response['failure-description'])

        return response

    def _upload(self, src):
        response = requests.post(
            self.url + '/add-content',
            auth=self.auth,
            files=dict(file=open(src)),
            timeout=self.timeout).json()

        if response['outcome'] == 'failed':
            raise OperationError(response['failure-description'])

        return response['result']['BYTES_VALUE']

    def execute(self, operation, parameters, ignore_failed_outcome, path=None):
        payload = op.execute(operation, parameters, path)

        return self._request(payload, ignore_failed_outcome)

    def read(self, path):
        response = self._request(op.read(path), True)

        exists = response['outcome'] == 'success'

        state = response['result'] if exists else {}

        return exists, state

    def add(self, path, attributes):
        return self._request(op.add(path, attributes))

    def remove(self, path):
        return self._request(op.remove(path))

    def update(self, path, attributes):
        operations = []
        for name, value in attributes.items():
            operations.append(op.write_attribute(path, name, value))

        payload = op.composite(operations)

        return self._request(payload)

    def deploy(self, name, src, remote_src, server_group=None):
        if remote_src:
            payload = op.composite(
                op.deploy(name, src, server_group))
        else:
            bytes_value = self._upload(src)
            payload = op.deploy_only(name, bytes_value, server_group)

        return self._request(payload)

    def undeploy(self, name, server_group=None):
        payload = op.composite(
            op.undeploy(name, server_group))

        return self._request(payload)

    def update_deploy(self, name, src, remote_src, server_group=None):
        if remote_src:
            operations = op.undeploy(name, server_group) + op.deploy(name, src, server_group)
            payload = op.composite(operations)

            return self._request(payload)

        self._request(op.remove('/deployment=' + name))
        return self.deploy(name, src, remote_src, server_group)
