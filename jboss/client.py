import json
from ansible.module_utils.urls import open_url
import jboss.operation_request as op
from ansible.module_utils.six.moves.urllib.error import HTTPError
from jboss.exceptions import AuthError
from jboss.exceptions import OperationError


class Client(object):

    def __init__(self, username, password, host='127.0.0.1', port=9990, timeout=300, headers=None):
        self.url = 'http://{0}:{1}/management'.format(host, port)
        self.username = username
        self.password = password
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

        try:
            response = open_url(
                    self.url,
                    data=json.dumps(payload),
                    headers=content_type_header,
                    method='POST',
                    use_proxy=False,
                    url_username=self.username,
                    url_password=self.password,
                    auth_realm='ManagementRealm',
                    timeout=self.timeout,
                    follow_redirects=True)

        except HTTPError as err:
            if err.getcode() == 401:
                raise AuthError('Invalid credentials')

            if err.getcode() == 500:
                api_response = json.loads(err.read().decode('utf-8'))

                if not unsafe:
                    raise OperationError(api_response['failure-description'])
                else:
                    return api_response

            raise

        return json.loads(response.read().decode('utf-8'))

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

    def deploy(self, name, src, server_group=None):
        payload = op.composite(
            op.deploy(name, src, server_group))

        return self._request(payload)

    def undeploy(self, name, server_group=None):
        payload = op.composite(
            op.undeploy(name, server_group))

        return self._request(payload)

    def update_deploy(self, name, src, server_group=None):
        operations = op.undeploy(name, server_group) + op.deploy(name, src, server_group)
        payload = op.composite(operations)

        return self._request(payload)
