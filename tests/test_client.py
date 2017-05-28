import pytest
from jboss.client import Client
from jboss.operation_error import OperationError


def test_read():
    client = Client('python', 'python')
    exists = client.read('/subsystem=datasources/data-source=ExampleDS')

    assert exists


def test_read_non_existent_resource():
    client = Client('python', 'python')
    response = client.read('/subsystem=datasources/data-source=NonExistentDS')

    assert response == (False, {})


def test_add():
    client = Client('python', 'python')
    path = '/subsystem=datasources/data-source=DemoDS'

    attributes = {'driver-name': 'h2',
                  'connection-url': 'jdbc:h2:mem:demo;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE',
                  'jndi-name': "java:jboss/datasources/DemoDS",
                  'user-name': 'sa',
                  'password': 'sa',
                  'min-pool-size': 10,
                  'max-pool-size': 30}

    response = client.add(path, attributes)

    assert response['outcome'] == 'success'


def test_remove():
    client = Client('python', 'python')
    response = client.remove('/subsystem=datasources/data-source=DemoDS')

    assert response['outcome'] == 'success'


def test_remove_non_existent_resource():
    with pytest.raises(OperationError):
        client = Client('python', 'python')
        client.remove('/subsystem=datasources/data-source=NonExistenteDS')


def test_deploy():
    client = Client('python', 'python')
    response = client.deploy('hawtio.war', '/tmp/hawtio.war')

    assert response['outcome'] == 'success'
