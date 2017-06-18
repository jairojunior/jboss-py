import time
import pytest
import docker
from jboss.client import Client
from jboss.exceptions import AuthError
from jboss.exceptions import OperationError


@pytest.fixture(scope='session', autouse=True)
def wildfly_container():
    docker_client = docker.from_env()
    docker_client.images.build(fileobj=open('Dockerfile'), tag='jboss-py')

    docker_client.containers.run('jboss-py',
                                 ports={9990: 9990},
                                 name='jboss-py-test',
                                 detach=True)
    time.sleep(10)

    yield

    docker_client.containers.get('jboss-py-test').stop()
    docker_client.containers.get('jboss-py-test').remove()


@pytest.fixture
def client():
    return Client('python', 'python0!')


def test_auth_error():
    client = Client('username', 'wrong_password')

    with pytest.raises(AuthError):
        client.read('/subsystem=datasources/data-source=ExampleDS')


def test_execute(client):
    response = client.execute(operation='read-attribute',
                              parameters=dict(name='enabled'),
                              ignore_failed_outcome=False,
                              path='/subsystem=datasources/data-source=ExampleDS')

    assert response['result']


def test_read(client):
    exists, _ = client.read('/subsystem=datasources/data-source=ExampleDS')

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


def test_remove_absent_resource(client):
    with pytest.raises(OperationError):
        client.remove('/subsystem=datasources/data-source=NonExistentDS')


def test_deploy(client):
    response = client.deploy(
        name='hawtio.war',
        src='/tmp/hawtio.war')

    assert response['outcome'] == 'success'


def test_update_deploy(client):
    response = client.update_deploy(
        name='hawtio.war',
        src='/tmp/hawtio.war')

    assert response['outcome'] == 'success'
