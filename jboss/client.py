import json
import requests
from requests.auth import HTTPDigestAuth
import jboss.operation_request as op
from jboss.operation_error import OperationError


class Client(object):

    def __init__(self, username, password, address='127.0.0.1', port=9990,):
        self.address = address
        self.port = port
        self.username = username
        self.password = password

    def _request(self, payload, unsafe=False):
        content_type_header = {'Content-Type': 'application/json'}
        url = 'http://{}:{}/management'.format(self.address, self.port)

        response = requests.post(
            url,
            data=json.dumps(payload),
            headers=content_type_header,
            auth=HTTPDigestAuth(self.username, self.password)).json()

        if response['outcome'] == 'failed' and not unsafe:
            raise OperationError(response['failure-description'])

        return response

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

    def deploy(self, name, src, server_group=None):
        payload = op.composite(
            op.deploy(name, src, server_group))

        return self._request(payload)

    def undeploy(self, name, server_group=None):
        payload = op.composite(
            op.undeploy(name, server_group))

        return self._request(payload)

    def update_deploy(self, name, src, server_group=None):
        payload = op.composite(
            op.deploy(name, src, server_group) +
            op.undeploy(name, server_group))

        return self._request(payload)
