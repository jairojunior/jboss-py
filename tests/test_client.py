import pytest
import docker
import time
from jboss.client import Client
from jboss.operation_error import OperationError


@pytest.fixture(scope='session', autouse=True)
def wildfly_container():
    client = docker.from_env()
    client.images.build(fileobj=open('Dockerfile'), tag='jboss-py')

    client.containers.run('jboss-py',
                          ports={9990: 9990},
                          name='jboss-py-test',
                          detach=True)
    time.sleep(10)

    yield

    client.containers.get('jboss-py-test').stop()
    client.containers.get('jboss-py-test').remove()


@pytest.fixture
def client():
    return Client('python', 'python0!')


def test_read(client):
    exists = client.read('/subsystem=datasources/data-source=ExampleDS')

    assert exists


def test_read_non_existent_resource(client):
    response = client.read('/subsystem=datasources/data-source=NonExistentDS')

    assert response == (False, {})


def test_add(client):
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


def test_remove(client):
    response = client.remove('/subsystem=datasources/data-source=DemoDS')

    assert response['outcome'] == 'success'


def test_remove_non_existent_resource(client):
    with pytest.raises(OperationError):
        client.remove('/subsystem=datasources/data-source=NonExistenteDS')


def test_deploy(client):
    response = client.deploy('hawtio.war', '/tmp/hawtio.war')

    assert response['outcome'] == 'success'


@pytest.yield_fixture(scope='session', autouse=True)
def clean_up_container():
    print 'After?'
