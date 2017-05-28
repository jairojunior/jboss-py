class OperationRequestBuilder(object):

    def __init__(self):
        self.detyped_request = dict(address=[])

    def read(self):
        self.detyped_request['operation'] = 'read-resource'
        return self

    def add(self):
        self.detyped_request['operation'] = 'add'
        return self

    def remove(self):
        self.detyped_request['operation'] = 'remove'
        return self

    def write(self, attribute, value):
        self.detyped_request['operation'] = 'write-attribute'
        self.detyped_request['name'] = attribute
        self.detyped_request['value'] = value
        return self

    def _no_target(self):
        return self.detyped_request['address'] == []

    def _operation(self, name):
        self.detyped_request['operation'] = name

    def deploy(self):
        self._operation('deploy' if self._no_target() else 'add')
        return self

    def undeploy(self):
        self._operation('undeploy' if self._no_target() else 'remove')
        return self

    def composite(self, operations):
        self.detyped_request['operation'] = 'composite'
        self.detyped_request['steps'] = operations
        return self

    def content(self, src):
        self.detyped_request['content'] = [dict(url='file:' + src)]
        return self

    def address_from(self, path):
        # Use regex: /node-type=node-name (/node-type=node-name)*
        tokens = path.split('/')

        address = []

        for token in tokens[1:]:
            node_type, node_name = token.split('=')
            address.append({node_type: node_name})

        self.detyped_request['address'] = address
        return self

    def deployment(self, name):
        self.detyped_request['address'].append(dict(deployment=name))
        return self

    def target(self, server_group):
        if server_group is not None:
            self.detyped_request['address'].append(
                {'server-group': server_group})
        return self

    def payload(self, attributes):
        self.detyped_request.update(attributes)
        return self

    def build(self):
        return self.detyped_request
