import json
import requests
from requests.auth import HTTPDigestAuth
from jboss.operation_request_builder import OperationRequestBuilder


class Client(object):

    def __init__(self, username, password, address='127.0.0.1', port=9990,):
        self.address = address
        self.port = port
        self.username = username
        self.password = password

    def _request(self, payload):
        content_type_header = {'Content-Type': 'application/json'}
        url = 'http://' + self.address + ':' + str(self.port) + '/management'

        return requests.post(
            url,
            data=json.dumps(payload),
            headers=content_type_header,
            auth=HTTPDigestAuth(self.username, self.password))

    def read(self, path):
        payload = OperationRequestBuilder() \
                    .address_from(path) \
                    .read() \
                    .build()

        return self._request(payload).json()

    def add(self, path, attributes):
        payload = OperationRequestBuilder() \
                    .address_from(path) \
                    .add() \
                    .payload(attributes) \
                    .build() \

        return self._request(payload).json()

    def remove(self, path):
        payload = OperationRequestBuilder() \
                    .address_from(path) \
                    .remove() \
                    .build() \

        return self._request(payload).json()

    def update(self, path, attributes):
        operations = []
        for name, value in attributes.items():
            operation = OperationRequestBuilder() \
                        .address_from(path) \
                        .write(name, value) \
                        .build()

            operations.append(operation)

        payload = OperationRequestBuilder().composite(operations).build()

        return self._request(payload).json()

    def deploy(self, name, src, server_group=None):
        add_content = OperationRequestBuilder() \
            .deployment(name) \
            .content(src) \
            .add() \
            .build() \

        deploy = OperationRequestBuilder() \
            .deploy() \
            .deployment(name) \
            .target(server_group) \
            .build() \

        payload = OperationRequestBuilder().composite(
            add_content, deploy).build()

        return self._request(payload).json()

    def undeploy(self, name, server_group=None):
        remove_content = OperationRequestBuilder() \
            .deployment(name) \
            .remove() \
            .build() \

        undeploy = OperationRequestBuilder() \
            .undeploy() \
            .deployment(name) \
            .target(server_group) \
            .build() \

        payload = OperationRequestBuilder().composite(
            undeploy, remove_content).build()

        return self._request(payload).json()

    def update_deploy(self, name, src, server_group=None):
        remove_content = OperationRequestBuilder() \
            .deployment(name) \
            .remove() \
            .build() \

        undeploy = OperationRequestBuilder() \
            .undeploy() \
            .deployment(name) \
            .target(server_group) \
            .build() \

        add_content = OperationRequestBuilder() \
            .deployment(name) \
            .content(src) \
            .add() \
            .build() \

        deploy = OperationRequestBuilder() \
            .deploy() \
            .deployment(name) \
            .target(server_group) \
            .build() \

        payload = OperationRequestBuilder().composite(
            undeploy, remove_content, add_content, deploy).build()

        return self._request(payload).json()