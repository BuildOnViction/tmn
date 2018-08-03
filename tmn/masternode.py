import sys
import docker as dockerpy
from tmn import display

VOLUMES = ['blockchain_data']
NETWORKS = ['masternode']
CONTAINERS = {
    'telegraf': {
        'image': 'tomochain/infra-telegraf:devnet',
        'hostname': 'test',
        'name': 'telegraf',
        'network': NETWORKS[0],
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
    },
    'tomochain': {
        'image': 'tomochain/infra-tomochain:devnet',
        'name': 'tomochain',
        'network': NETWORKS[0],
        'volumes': {
            VOLUMES[0]: {
                'bind': '/tomochain/data', 'mode': 'rw'
            }
        },
        'detach': True
    },
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


def _create_volumes():
    """
    Try to get the volumes defined in `VOLUMES`. If it fails, create them.
    """
    for volume in VOLUMES:
        display.step_create_masternode_volume(volume)
        try:
            _client.volumes.get(volume)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.volumes.create(volume)
            display.step_close_created()
    display.newline()


def _create_networks():
    """
    Try to get the networks defined in `NETWORKS`. If it fails, create them.
    """
    for network in NETWORKS:
        display.step_create_masternode_network(network)
        try:
            _client.networks.get(network)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.networks.create(network)
            display.step_close_created()
    display.newline()


def _create_containers():
    """
    Try to get the containers defined in `CONTAINERS`.
    If it fails, create them.

    :returns: The created or existing `docker.Container`
    :rtype: list
    """
    containers = []
    for container, config in CONTAINERS.items():
        display.step_create_masternode_container(config['name'])
        try:
            container = _client.containers.get(config['name'])
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            # temporary, see https://github.com/docker/docker-py/issues/2101
            _client.images.pull(config['image'])
            container = _client.containers.create(**config)
            display.step_close_created()
        containers.append(container)
    return containers


def _start_containers(containers):
    """
    Verify the container status. If it's not restarting or running,
    start them.

    :param containers: list of `docker.Container`
    :type containers: list
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


@apierror
def start():
    """
    Start a masternode. Includes:
    - creating volumes
    - creating networks
    - creating containers
    - starting containers
    """
    display.subtitle_create_volumes()
    _create_volumes()
    display.subtitle_create_networks()
    _create_networks()
    display.subtitle_create_containers()
    containers = _create_containers()
    display.newline()
    _start_containers(containers)


# @apierror
# def stop():
#     """
#     Stop a masternode. Includes:
#     - stoping containers
#     """
#     display.subtitle_create_containers()
#     containers = _get_containers()
#     _stop_containers(containers)
