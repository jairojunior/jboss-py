class OperationRequestBuilder(object):

    def __init__(self):
        self.detyped_request = dict(address=[])

    def read(self):
        self.detyped_request['operation'] = 'read-resource'

    def add(self):
        self.detyped_request['operation'] = 'add'

    def remove(self):
        self.detyped_request['operation'] = 'remove'

    def write(self, attribute, value):
        self.detyped_request['operation'] = 'write-attribute'
        self.detyped_request['name'] = attribute
        self.detyped_request['value'] = value

    def _no_target(self):
        return self.detyped_request['address'] == []

    def operation(self, name):
        self.detyped_request['operation'] = name

    def deploy(self):
        self.operation('deploy' if self._no_target() else 'add')

    def undeploy(self):
        self.operation('undeploy' if self._no_target() else 'remove')

    def composite(self, operations):
        self.detyped_request['operation'] = 'composite'
        self.detyped_request['steps'] = operations

    def content(self, src):
        self.detyped_request['content'] = [dict(url='file:' + src)]

    def content_reference(self, bytes_value):
        self.detyped_request['content'] = [
            {'hash': {'BYTES_VALUE': bytes_value}}]

    def address_from(self, path):
        if path is not None:
            # Use regex: /node-type=node-name (/node-type=node-name)*
            tokens = path.split('/')

            address = []

            for token in tokens[1:]:
                node_type, node_name = token.split('=')
                address.append({node_type: node_name})

            self.detyped_request['address'] = address

    def deployment(self, name):
        self.detyped_request['address'].append(dict(deployment=name))

    def target(self, server_group):
        if server_group is not None:
            self.detyped_request['address'].append(
                {'server-group': server_group})

    def payload(self, attributes):
        self.detyped_request.update(attributes)

    def build(self):
        return self.detyped_request
