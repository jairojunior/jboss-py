from jboss.operation_request_builder import OperationRequestBuilder


def test_read_operation():
    builder = OperationRequestBuilder()
    builder.read()
    request = builder.build()

    assert request == dict(operation='read-resource', address=[])


def test_add_operation():
    builder = OperationRequestBuilder()
    builder.add()
    request = builder.build()

    assert request == dict(operation='add', address=[])


def test_remove_operation():
    builder = OperationRequestBuilder()
    builder.remove()
    request = builder.build()

    assert request == dict(operation='remove', address=[])


def test_write_attribute_operation():
    builder = OperationRequestBuilder()
    builder.write('min-pool-size', 10)
    request = builder.build()

    assert request == dict(operation='write-attribute',
                           name='min-pool-size',
                           value=10,
                           address=[])


def test_address_from_path():
    builder = OperationRequestBuilder()
    builder.address_from('/subsystem=datasources/data-source=DemoDS')
    request = builder.build()

    assert request == dict(
        address=[{'subsystem': 'datasources'}, {'data-source': 'DemoDS'}])


def test_target_server_group():
    builder = OperationRequestBuilder()
    builder.target('main-server-group')
    request = builder.build()

    assert request == dict(address=[{'server-group': 'main-server-group'}])


def test_content_src():
    builder = OperationRequestBuilder()
    builder.content('/tmp/hawtio.war')
    request = builder.build()

    assert request == dict(
        content=[dict(url='file:/tmp/hawtio.war')], address=[])


def test_deployment_address():
    builder = OperationRequestBuilder()
    builder.deployment('hawtio.war')
    request = builder.build()

    assert request == dict(address=[dict(deployment='hawtio.war')])


def test_deploy_no_server_group():
    builder = OperationRequestBuilder()
    builder.target(None)
    builder.deploy()
    request = builder.build()

    assert request == dict(operation='deploy', address=[])


def test_undeploy_no_server_group():
    builder = OperationRequestBuilder()
    builder.undeploy()
    request = builder.build()

    assert request == dict(operation='undeploy', address=[])


def test_deploy_with_server_group():
    builder = OperationRequestBuilder()
    builder.target('main-server-group')
    builder.deploy()

    request = builder.build()

    assert request == dict(operation='add',
                           address=[{'server-group': 'main-server-group'}])


def test_undeploy_with_server_group():
    builder = OperationRequestBuilder()
    builder.target('main-server-group')
    builder.undeploy()

    request = builder.build()

    assert request == dict(operation='remove',
                           address=[{'server-group': 'main-server-group'}])


def test_composite_operation():
    builder = OperationRequestBuilder()
    builder.add()
    add_operation = builder.build()

    builder = OperationRequestBuilder()
    builder.deploy()
    deploy_operation = builder.build()

    builder = OperationRequestBuilder()
    builder.composite([add_operation, deploy_operation])

    request = builder.build()

    assert request == dict(address=[],
                           operation='composite',
                           steps=[add_operation, deploy_operation])
