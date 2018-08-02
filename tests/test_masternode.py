import pytest


@pytest.fixture
def test_data():
    from tmn import masternode
    masternode.connect()
    masternode.VOLUMES = ['test']
    masternode.NETWORKS = ['test']
    masternode.CONTAINERS = {'alpine': {
            'image': 'alpine:latest',
            'name': 'test',
            'command': 'sleep 1000',
            'detach': True
    }}
    masternode.connect()
    return masternode


@pytest.fixture
def docker_fail():
    from tmn import masternode
    masternode.connect(url='unix://root')
    return masternode


def test_ping(test_data):
    assert test_data._ping()


def test_ping_docker_fail(docker_fail):
    assert not docker_fail._ping()


def test_create_volumes(test_data):
    test_data._create_volumes()
    v = test_data._client.volumes.get(test_data.VOLUMES[0])
    assert v
    v.remove(force=True)


def test_create_volumes_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_volumes()


def test_create_networks(test_data):
    test_data._create_networks()
    n = test_data._client.networks.get(test_data.NETWORKS[0])
    assert n
    n.remove()


def test_create_networks_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_networks()


def test_create_containers(test_data):
    c_list = test_data._create_containers()
    c = test_data._client.containers.get(c_list[0].name)
    assert c
    c.remove(force=True)


def test_create_containers_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_containers()


def test_run_containers(test_data):
    c_list = test_data._create_containers()
    test_data._start_containers(c_list)
    c = test_data._client.containers.get(c_list[0].name)
    assert c.status == "running"
    c.remove(force=True)
