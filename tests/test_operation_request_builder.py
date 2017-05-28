from jboss.operation_request_builder import OperationRequestBuilder


def test_read_operation():
    request = OperationRequestBuilder().read().build()

    assert request == dict(operation='read-resource', address=[])


def test_add_operation():
    request = OperationRequestBuilder().add().build()

    assert request == dict(operation='add', address=[])


def test_remove_operation():
    request = OperationRequestBuilder().remove().build()

    assert request == dict(operation='remove', address=[])


def test_write_attribute_operation():
    request = OperationRequestBuilder().write('min-pool-size', 10).build()

    assert request == dict(
        operation='write-attribute',
        name='min-pool-size',
        value=10,
        address=[])


def test_address_from_path():
    request = OperationRequestBuilder().address_from(
        '/subsystem=datasources/data-source=DemoDS').build()

    assert request == dict(
        address=[{'subsystem': 'datasources'}, {'data-source': 'DemoDS'}])


def test_target_server_group():
    request = OperationRequestBuilder().target('main-server-group').build()

    assert request == dict(address=[{'server-group': 'main-server-group'}])


def test_content_src():
    request = OperationRequestBuilder().content('/tmp/hawtio.war').build()

    assert request == dict(content=[dict(
        url='file:/tmp/hawtio.war')], address=[])


def test_deployment_address():
    request = OperationRequestBuilder().deployment('hawtio.war').build()

    assert request == dict(address=[dict(deployment='hawtio.war')])


def test_deploy_without_server_group():
    request = OperationRequestBuilder().target(None).deploy().build()

    assert request == dict(operation='deploy', address=[])


def test_undeploy_without_server_group():
    request = OperationRequestBuilder().undeploy().build()

    assert request == dict(operation='undeploy', address=[])


def test_deploy_with_server_group():
    request = OperationRequestBuilder().target(
        'main-server-group').deploy().build()

    assert request == dict(
        operation='add',
        address=[{'server-group': 'main-server-group'}])


def test_undeploy_with_server_group():
    request = OperationRequestBuilder().target(
        'main-server-group').undeploy().build()

    assert request == dict(
        operation='remove',
        address=[{'server-group': 'main-server-group'}])


def test_composite_operation():
    add_operation = OperationRequestBuilder().add().build()
    deploy_operation = OperationRequestBuilder().deploy().build()

    request = OperationRequestBuilder().composite(
        [add_operation, deploy_operation]).build()

    assert request == dict(
        address=[],
        operation='composite',
        steps=[add_operation, deploy_operation])
