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


def connect(url):
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
    Try to ping the Docker deamon. Check if accessible.

    :returns: is Docker running
    :rtype: bool
    """
    try:
        return _client.ping()
    except Exception:
        return False


def _create_volumes():
    for volume in VOLUMES:
        display.step_create_masternode_volume(volume)
        try:
            _client.volumes.get(volume)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.volumes.create(volume)
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker_api()
            sys.exit()
    display.newline()


def _create_network():
    for network in NETWORKS:
        display.step_create_masternode_network(network)
        try:
            _client.networks.get(network)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.networks.create(network)
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker_api()
            sys.exit()
    display.newline()


def _create_containers():
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
        except dockerpy.errors.APIError:
            display.error_docker_api()
            sys.exit()
        containers.append(container)
    return containers


def _start_containers(containers):
    for container in containers:
        display.step_start_masternode_container(container.name)
        try:
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
            elif container.status in ['removing']:
                display.error_docker_state(container.name, container.status)
                sys.exit()
            container.reload()
            display.step_close_status(container.status)
        except dockerpy.errors.APIError:
            display.error_docker_api()
            sys.exit()


def start():
    display.subtitle_create_volumes()
    _create_volumes()
    display.subtitle_create_networks()
    _create_network()
    display.subtitle_create_containers()
    containers = _create_containers()
    display.newline()
    _start_containers(containers)
