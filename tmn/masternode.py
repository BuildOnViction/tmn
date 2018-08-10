import sys
from collections import OrderedDict
import docker as dockerpy
from tmn import display

LABEL = 'tmn'
VOLUME = {'name': 'data'}
BIND = {'bind': '/tomochain/data', 'mode': 'rw'}
NETWORK = {'name': 'network'}
CONTAINERS = OrderedDict()
CONTAINERS['tomochain'] = {
    'image': 'tomochain/infra-tomochain:devnet',
    'name': 'tomochain',
    'volumes': {
    },
    'detach': True
}
CONTAINERS['metrics'] = {
    'image': 'tomochain/infra-telegraf:devnet',
    'hostname': 'test',
    'name': 'metrics',
    'volumes': {
        '/var/run/docker.sock': {
            'bind': '/var/run/docker.sock', 'mode': 'ro'
        },
        '/sys': {
            'bind': '/rootfs/sys', 'mode': 'ro'
        },
        '/proc': {
            'bind': '/rootfs/proc', 'mode': 'ro'
        },
        '/etc': {
            'bind': '/rootfs/etc', 'mode': 'ro'
        }
    },
    'detach': True
}

_client = None
connected = False


def apierror(function):
    """
    Decorator to catch `docker.errors.APIerror` Exception

    :param function: function to decorate
    :type function: function
    :returns: decorated function
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except dockerpy.errors.APIError:
            display.error_docker_api()
            sys.exit()
    return wrapper


def connect(url=None):
    """
    Create the docker client. Try to ping the docker server to establish if
    the connexion in successful

    :param url: url to the docker deamon
    :type url: str
    """
    global _client
    global connected
    if not url:
        _client = dockerpy.from_env()
    else:
        _client = dockerpy.DockerClient(base_url=url)
    if _ping():
        connected = True


def _ping():
    """
    Try to ping the Docker daemon. Check if accessible.

    :returns: is Docker running
    :rtype: bool
    """
    try:
        return _client.ping()
    except Exception:
        return False


def _list_labels(containers):
    """
    List labels value from a list of containers
    """
    values = []
    for container in containers:
        values.append(container.labels['tmn'])
    values = list(set(values))
    for value in values:
        display.item(value)


def _compose(name):
    NETWORK['name'] = '{}_{}'.format(name, NETWORK['name'])
    NETWORK['labels'] = {LABEL: name}
    VOLUME['name'] = '{}_{}'.format(name, VOLUME['name'])
    VOLUME['labels'] = {LABEL: name}
    for key, value in CONTAINERS.items():
        CONTAINERS[key]['network'] = NETWORK['name']
        try:
            CONTAINERS[key]['volumes'][VOLUME['name']] = BIND
        except KeyError:
            pass
        CONTAINERS[key]['labels'] = {LABEL: name}
        CONTAINERS[key]['name'] = '{}_{}'.format(name, CONTAINERS[key]['name'])


def _create_volume():
    """
    Try to get the VOLUME defined in `VOLUME`. If it fails, create them.
    """
    display.step_create_masternode_volume(VOLUME['name'])
    try:
        _client.volumes.get(VOLUME['name'])
        display.step_close_exists()
    except dockerpy.errors.NotFound:
        _client.volumes.create(**VOLUME)
        display.step_close_created()
    display.newline()


def _create_network():
    """
    Try to get the NETWORK defined in `NETWORK`. If it fails, create them.
    """
    display.step_create_masternode_network(NETWORK['name'])
    try:
        _client.networks.get(NETWORK['name'])
        display.step_close_exists()
    except dockerpy.errors.NotFound:
        _client.networks.create(**NETWORK)
        display.step_close_created()
    display.newline()


def _get_containers(name=None, all=True):
    """
    Get the containers defined in `CONTAINERS`.

    :returns: The existing `docker.Container`
    :rtype: list
    """
    if name:
        return _client.containers.list(
            all=all,
            filters={'label': 'tmn={}'.format(name)}
        )
    else:
        return _client.containers.list(
            all=all,
            filters={'label': 'tmn'}
        )


def _create_containers():
    """
    Try to get the containers defined in `CONTAINERS`.
    If it fails, create them.

    :returns: The created or existing `docker.Container`
    :rtype: list
    """
    containers = []
    for key, value in CONTAINERS.items():
        display.step_create_masternode_container(value['name'])
        try:
            container = _client.containers.get(value['name'])
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            # temporary, see https://github.com/docker/docker-py/issues/2101
            _client.images.pull(value['image'])
            container = _client.containers.create(**value)
            display.step_close_created()
        containers.append(container)
    return containers


def _start_containers(containers):
    """
    Verify the container status. If it's not restarting or running,
    start them.

    :param containers: dict of name:`docker.Container`
    :type containers: dict
    """
    for container in containers:
        display.step_start_masternode_container(container.name)
        container.reload()
        # filtered status are:
        # created|restarting|running|removing|paused|exited|dead
        # might have to add all the status
        if container.status in ['restarting', 'running']:
            pass
        elif container.status in ['paused']:
            container.unpause()
        elif container.status in ['created', 'exited', 'dead']:
            container.start()
        container.reload()
        display.step_close_status(container.status)


def _stop_containers(containers):
    """
    Stop the given dict of `docker.Container`

    :param containers: dict of name:`docker.Container`
    :type containers: dict
    """
    for container in containers:
        display.step_stop_masternode_container(container.name)
        container.reload()
        # filtered status are:
        # created|restarting|running|removing|paused|exited|dead
        # might have to add all the status
        if container.status in ['restarting', 'running', 'paused']:
            container.stop()
        elif container.status in ['created', 'exited', 'dead']:
            pass
        container.reload()
        display.step_close_status(container.status)


def _status_containers(containers):
    """
    Display the status of `CONTAINERS` w/ the passed list of `docker.Container`

    :param containers: dict of `docker.Container`
    :type containers: dict
    """
    names = [value['name'] for key, value in CONTAINERS.items()]
    for name in names:
        display_kwargs = {}
        display_kwargs.update({'name': name})
        for container in containers:
            if container.name == name:
                container.reload()
                if container.status in ['running']:
                    display_kwargs.update({'status_color': 'green'})
                display_kwargs.update({'status': container.status})
                display_kwargs.update({'id': container.short_id})
        display.status(**display_kwargs)


@apierror
def list_masternodes():
    """
    List masternodes. Includes:
    - retrieving tmn labeled containers
    - display label values
    """
    containers = _get_containers()
    _list_labels(containers)


@apierror
def start(name):
    """
    Start a masternode. Includes:
    - compose node name into config
    - creating VOLUME
    - creating NETWORK
    - creating containers
    - starting containers
    """
    _compose(name)
    display.subtitle_create_volume()
    _create_volume()
    display.subtitle_create_network()
    _create_network()
    display.subtitle_create_containers()
    containers = _create_containers()
    display.newline()
    _start_containers(containers)


@apierror
def stop(name):
    """
    Stop a masternode. Includes:
    - getting the list of containers
    - stoping them
    """
    _compose(name)
    containers = _get_containers(name)
    _stop_containers(containers)


@apierror
def status(name):
    """
    Retrieve masternode status. Includes:
    - getting the list of containers
    - displaying their status
    """
    _compose(name)
    containers = _get_containers(name)
    _status_containers(containers)
