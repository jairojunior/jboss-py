from jboss.operation_request_builder import OperationRequestBuilder


def execute(operation, parameters, path):
    builder = OperationRequestBuilder()
    builder.address_from(path)
    builder.payload(parameters)
    builder.operation(operation)
    return builder.build()


def read(path):
    builder = OperationRequestBuilder()
    builder.address_from(path)
    builder.read()
    return builder.build()


def add(path, attributes):
    builder = OperationRequestBuilder()
    builder.address_from(path)
    builder.add()
    builder.payload(attributes)
    return builder.build()


def remove(path):
    builder = OperationRequestBuilder()
    builder.address_from(path)
    builder.remove()
    return builder.build()


def write_attribute(path, name, value):
    builder = OperationRequestBuilder()
    builder.address_from(path)
    builder.write(name, value)
    return builder.build()


def composite(operations):
    builder = OperationRequestBuilder()
    builder.composite(operations)
    return builder.build()


def deploy(name, src, server_group):
    add_builder = OperationRequestBuilder()
    add_builder.deployment(name)
    add_builder.content(src)
    add_builder.add()
    add_content = add_builder.build()

    deploy_builder = OperationRequestBuilder()
    if server_group:
        deploy_builder.payload({'enabled': True})

    deploy_builder.target(server_group)
    deploy_builder.deploy()
    deploy_builder.deployment(name)
    deploy_operation = deploy_builder.build()

    return [add_content, deploy_operation]


def add_deployment(name, bytes_value, enabled=False):
    builder = OperationRequestBuilder()
    builder.content_reference(bytes_value)
    builder.add()
    builder.deployment(name)
    builder.payload({'enabled': enabled})
    return builder.build()

def assign(name, server_group):
    builder = OperationRequestBuilder()
    builder.target(server_group)
    builder.deploy()
    builder.deployment(name)
    builder.payload({'enabled': True})
    return builder.build()


def undeploy(name, server_group):
    builder = OperationRequestBuilder()
    builder.deployment(name)
    builder.remove()
    remove_content = builder.build()

    builder = OperationRequestBuilder()
    builder.target(server_group)
    builder.undeploy()
    builder.deployment(name)
    undeploy_operation = builder.build()

    return [undeploy_operation, remove_content]
