import pytest
import docker as dockerpy


@pytest.fixture
def test_data():
    from tmn import masternode
    masternode.connect()
    masternode.compose.volumes = ['test']
    masternode.compose.networks = ['test']
    masternode.compose.environment = {'TEST': 'test'}
    masternode.compose.containers = {
        'alpine': {
            'image': 'alpine:latest',
            'name': 'test',
            'command': 'sleep 1000',
            'detach': True
        }
    }
    masternode.connect()
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


def test_create_volumes(capsys, test_data):
    test_data._create_volumes()
    captured = capsys.readouterr()
    v = test_data._client.volumes.get(test_data.compose.volumes[0])
    assert v
    assert ('- Creating {}... '.format(test_data.compose.volumes[0])
            in captured.out)
    assert 'created' in captured.out
    v.remove(force=True)


def test_create_volumes_exist(capsys, test_data):
    test_data._create_volumes()
    capsys.readouterr()
    test_data._create_volumes()
    captured = capsys.readouterr()
    v = test_data._client.volumes.get(test_data.compose.volumes[0])
    assert v
    assert ('- Creating {}... '.format(test_data.compose.volumes[0])
            in captured.out)
    assert 'exists' in captured.out
    v.remove(force=True)


def test_create_volumes_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_volumes()


def test_create_networks(capsys, test_data):
    test_data._create_networks()
    captured = capsys.readouterr()
    n = test_data._client.networks.get(test_data.compose.networks[0])
    assert n
    assert ('- Creating {}... '.format(test_data.compose.networks[0])
            in captured.out)
    assert 'created' in captured.out
    n.remove()


def test_create_exist(capsys, test_data):
    test_data._create_networks()
    capsys.readouterr()
    test_data._create_networks()
    captured = capsys.readouterr()
    n = test_data._client.networks.get(test_data.compose.networks[0])
    assert n
    assert ('- Creating {}... '.format(test_data.compose.networks[0])
            in captured.out)
    assert 'exists' in captured.out
    n.remove()


def test_create_networks_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_networks()


def test_create_containers(capsys, test_data):
    c_dict = test_data._create_containers()
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c
    assert ('- Creating {}... '.format(
            test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'created' in captured.out
    c.remove(force=True)


def test_create_containers_exist(capsys, test_data):
    test_data._create_containers()
    capsys.readouterr()
    c_dict = test_data._create_containers()
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c
    assert ('- Creating {}... '.format(
            test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'exists' in captured.out
    c.remove(force=True)


def test_create_containers_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._create_containers()


def test_get_containers(test_data):
    test_data._create_containers()
    c_dict = test_data._get_existing_containers()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c
    c.remove(force=True)


def test_get_containers_absent(test_data):
    test_data._create_containers()
    c_dict = test_data._get_existing_containers()
    assert len(c_dict) == 1
    c_dict[test_data.compose.containers['alpine']['name']].remove(force=True)
    c_dict = test_data._get_existing_containers()
    assert len(c_dict) == 0


def test_get_containers_docker_fail(docker_fail):
    with pytest.raises(Exception):
        docker_fail._get_existing_containers()


def test_start_containers(capsys, test_data):
    c_dict = test_data._create_containers()
    test_data._start_containers(c_dict)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c.status == 'running'
    assert ('- Starting {}... '
            .format(test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'running' in captured.out
    c.remove(force=True)


def test_start_containers_running(capsys, test_data):
    c_dict = test_data._create_containers()
    test_data._start_containers(c_dict)
    capsys.readouterr()
    c_dict[test_data.compose.containers['alpine']['name']].reload()
    test_data._start_containers(c_dict)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c.status == 'running'
    assert ('- Starting {}... '
            .format(test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'running' in captured.out
    c.remove(force=True)


def test_start_containers_paused(capsys, test_data):
    c_dict = test_data._create_containers()
    test_data._start_containers(c_dict)
    capsys.readouterr()
    c_dict[test_data.compose.containers['alpine']['name']].pause()
    c_dict[test_data.compose.containers['alpine']['name']].reload()
    assert (c_dict[test_data.compose.containers['alpine']['name']]
            .status == 'paused')
    test_data._start_containers(c_dict)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c.status == 'running'
    assert ('- Starting {}... '
            .format(test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'running' in captured.out
    c.remove(force=True)


def test_stop_containers(capsys, test_data):
    c_dict = test_data._create_containers()
    test_data._start_containers(c_dict)
    capsys.readouterr()
    test_data._stop_containers(c_dict)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c.status == 'exited'
    assert ('- Stopping {}... '
            .format(test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'exited' in captured.out
    c.remove(force=True)


def test_stop_containers_created(capsys, test_data):
    c_dict = test_data._create_containers()
    capsys.readouterr()
    test_data._stop_containers(c_dict)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c.status == 'created'
    assert ('- Stopping {}... '
            .format(test_data.compose.containers['alpine']['name'])
            in captured.out)
    assert 'created' in captured.out
    c.remove(force=True)


def test_status_containers(capsys, test_data):
    c_dict = test_data._create_containers()
    test_data._start_containers(c_dict)
    capsys.readouterr()
    test_data._status_containers(c_dict)
    captured = capsys.readouterr()
    c = test_data._client.containers.get(
        c_dict[test_data.compose.containers['alpine']['name']].name
    )
    assert c.status == 'running'
    assert ('{}\trunning({})'.format(
        test_data.compose.containers['alpine']['name'],
        c.short_id
    ) in captured.out)
    c.remove(force=True)


def test_status_containers_absent(capsys, test_data):
    c_dict = test_data._get_existing_containers()
    capsys.readouterr()
    test_data._status_containers(c_dict)
    captured = capsys.readouterr()
    assert ('{}\tabsent'.format(
        test_data.compose.containers['alpine']['name']
    ) in captured.out)
