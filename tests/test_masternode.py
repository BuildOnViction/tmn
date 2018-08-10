from collections import OrderedDict
import pytest
import docker as dockerpy


mn = 'test'


@pytest.fixture
def test_data():
    from tmn import masternode
    masternode.connect()
    masternode.VOLUME = {'name': 'test'}
    masternode.NETWORK = {'name': 'test'}
    masternode.CONTAINERS = OrderedDict()
    masternode.CONTAINERS[mn] = {
        'image': 'alpine:latest',
        'name': mn,
        'command': 'sleep 1000',
        'detach': True
    }
    masternode.connect()
    masternode._compose(mn)
    return masternode


@pytest.fixture
def docker_fail():
    from tmn import masternode
    masternode.connect(url='unix://root')
    return masternode


def test_decorator(capsys, test_data):
    def test():
        print('ok')
    decorated = test_data.apierror(test)
    decorated()
    captured = capsys.readouterr()
    assert captured.out == 'ok\n'


def test_decorator_apierror(capsys, test_data):
    def test():
        raise dockerpy.errors.APIError('test')
    decorated = test_data.apierror(test)
    with pytest.raises(SystemExit):
        decorated()
    captured = capsys.readouterr()
    assert 'something went wrong while doing stuff with docker' in captured.out


def test_ping(test_data):
    assert test_data._ping()


def test_ping_docker_fail(docker_fail):
    assert not docker_fail._ping()


def test_list_labels(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    c_list = test_data._create_containers()
    capsys.readouterr()
    test_data._list_labels(c_list)
    captured = capsys.readouterr()
    assert ('- {}'.format(mn) in captured.out)
    c_list[0].remove(force=True)
    n.remove()


def test_create_volume(capsys, test_data):
    test_data._create_volume()
    captured = capsys.readouterr()
    v = test_data._client.volumes.get(test_data.VOLUME['name'])
    assert v
    assert '- Creating {}... '.format(test_data.VOLUME['name']) in captured.out
    assert 'created' in captured.out
    v.remove(force=True)


def test_create_volume_exist(capsys, test_data):
    test_data._create_volume()
    capsys.readouterr()
    test_data._create_volume()
    captured = capsys.readouterr()
    v = test_data._client.volumes.get(test_data.VOLUME['name'])
    assert v
    assert '- Creating {}... '.format(test_data.VOLUME['name']) in captured.out
    assert 'exists' in captured.out
    v.remove(force=True)


def test_create_volume_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_volume()


def test_create_network(capsys, test_data):
    test_data._create_network()
    captured = capsys.readouterr()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    assert n
    assert '- Creating {}... '.format(
        test_data.NETWORK['name']
    ) in captured.out
    assert 'created' in captured.out
    n.remove()


def test_create_exist(capsys, test_data):
    test_data._create_network()
    capsys.readouterr()
    test_data._create_network()
    captured = capsys.readouterr()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    assert n
    assert '- Creating {}... '.format(
        test_data.NETWORK['name']
    ) in captured.out
    assert 'exists' in captured.out
    n.remove()


def test_create_network_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_network()


def test_create_containers(capsys, test_data):
    c_list = test_data._create_containers()
    captured = capsys.readouterr()
    c = test_data._client.containers.get(c_list[0].name)
    assert c
    assert ('- Creating {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'created' in captured.out
    c.remove(force=True)


def test_create_containers_exist(capsys, test_data):
    test_data._create_containers()
    capsys.readouterr()
    c_list = test_data._create_containers()
    captured = capsys.readouterr()
    c = test_data._client.containers.get(c_list[0].name)
    assert c
    assert ('- Creating {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'exists' in captured.out
    c.remove(force=True)


def test_create_containers_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_containers()


def test_get_containers(test_data):
    test_data._create_containers()
    c_list = test_data._get_containers(name=mn)
    c = test_data._client.containers.get(c_list[0].name)
    assert c
    c.remove(force=True)


def test_get_containers_absent(test_data):
    test_data._create_containers()
    c_list = test_data._get_containers(name=mn)
    assert len(c_list) == 1
    c_list[0].remove(force=True)
    c_list = test_data._get_containers(name=mn)
    assert len(c_list) == 0


def test_get_containers_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._get_containers()


def test_start_containers(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    capsys.readouterr()
    c_list = test_data._create_containers()
    test_data._start_containers(c_list)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_list[0].name
    )
    assert c.status == 'running'
    assert ('- Starting {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'running' in captured.out
    c.remove(force=True)
    n.remove()


def test_start_containers_running(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    c_list = test_data._create_containers()
    test_data._start_containers(c_list)
    capsys.readouterr()
    c_list[0].reload()
    test_data._start_containers(c_list)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_list[0].name
    )
    assert c.status == 'running'
    assert ('- Starting {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'running' in captured.out
    c.remove(force=True)
    n.remove()


def test_start_containers_paused(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    c_list = test_data._create_containers()
    test_data._start_containers(c_list)
    capsys.readouterr()
    c_list[0].pause()
    c_list[0].reload()
    assert c_list[0].status == 'paused'
    test_data._start_containers(c_list)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_list[0].name
    )
    assert c.status == 'running'
    assert ('- Starting {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'running' in captured.out
    c.remove(force=True)
    n.remove()


def test_stop_containers(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    c_list = test_data._create_containers()
    test_data._start_containers(c_list)
    capsys.readouterr()
    test_data._stop_containers(c_list)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_list[0].name
    )
    assert c.status == 'exited'
    assert ('- Stopping {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'exited' in captured.out
    c.remove(force=True)
    n.remove()


def test_stop_containers_created(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    c_list = test_data._create_containers()
    capsys.readouterr()
    test_data._stop_containers(c_list)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_list[0].name
    )
    assert c.status == 'created'
    assert ('- Stopping {}... '.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
    assert 'created' in captured.out
    c.remove(force=True)
    n.remove()


def test_status_containers(capsys, test_data):
    test_data._create_network()
    n = test_data._client.networks.get(test_data.NETWORK['name'])
    c_list = test_data._create_containers()
    test_data._start_containers(c_list)
    capsys.readouterr()
    test_data._status_containers(c_list)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_list[0].name
    )
    assert c.status == 'running'
    assert ('{} running({})'.format(
        test_data.CONTAINERS[mn]['name'],
        c.short_id
    ) in captured.out)
    c.remove(force=True)
    n.remove()


def test_status_containers_absent(capsys, test_data):
    c_list = test_data._get_containers()
    capsys.readouterr()
    test_data._status_containers(c_list)
    captured = capsys.readouterr()
    assert ('{} absent'.format(
        test_data.CONTAINERS[mn]['name']
    ) in captured.out)
