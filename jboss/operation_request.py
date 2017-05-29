from jboss.operation_request_builder import OperationRequestBuilder


def read(path):
    return OperationRequestBuilder() \
                .address_from(path) \
                .read() \
                .build()


def add(path, attributes):
    return OperationRequestBuilder() \
                .address_from(path) \
                .add() \
                .payload(attributes) \
                .build()


def remove(path):
    return OperationRequestBuilder() \
                .address_from(path) \
                .remove() \
                .build()


def write_attribute(path, name, value):
    return OperationRequestBuilder() \
                .address_from(path) \
                .write(name, value) \
                .build()


def composite(operations):
    return OperationRequestBuilder().composite(operations).build()


def deploy(name, src, server_group):
    add_content = OperationRequestBuilder() \
        .deployment(name) \
        .content(src) \
        .add() \
        .build()

    deploy_operation = OperationRequestBuilder() \
        .target(server_group) \
        .deploy() \
        .deployment(name) \
        .build()

    return [add_content, deploy_operation]


def deploy_only(name, bytes_value, server_group):
    return OperationRequestBuilder() \
            .content_reference(bytes_value) \
            .target(server_group) \
            .add() \
            .payload({'enabled': True}) \
            .deployment(name) \
            .build()


def undeploy(name, server_group):
    remove_content = OperationRequestBuilder() \
        .deployment(name) \
        .remove() \
        .build()

    undeploy_operation = OperationRequestBuilder() \
        .target(server_group) \
        .undeploy() \
        .deployment(name) \
        .build()

    return [undeploy_operation, remove_content]
