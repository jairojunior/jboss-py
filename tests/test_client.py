from jboss.client import Client


def test_read():
    client = Client('python', 'python')
    response = client.read('/subsystem=datasources/data-source=ExampleDS')

    assert response['outcome'] == 'success'


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


def test_deploy():
    client = Client('python', 'python')
    response = client.deploy('hawtio.war', '/tmp/hawtio.war')

    assert response['outcome'] == 'success'
